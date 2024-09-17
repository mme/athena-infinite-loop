"""
The search node is responsible for searching the internet for information.
"""
import json
from datetime import datetime
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage
from langchain_core.runnables import RunnableConfig
from langchain_community.tools.tavily_search import TavilySearchResults
from copilotkit.langchain import configure_copilotkit

from .state import AgentState

async def search_node(state: AgentState, config: RunnableConfig):
    """
    The search node is responsible for searching the internet for information.
    """
    config = configure_copilotkit(config, emit_tool_calls=True)

    tavily_tool = TavilySearchResults(
        max_results=10,
        search_depth="advanced",
        include_answer=True,
        include_raw_content=True,
        include_images=True,
        tavily_api_key="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"
    )
    # config = configure_copilotkit(config, emit_messages=True)
    current_step = next((step for step in state["steps"] if step["status"] == "pending"), None)

    if current_step is None:
        raise ValueError("No step to search for")

    if current_step["type"] != "search":
        raise ValueError("Current step is not a search step")

    system_message = f"""
This is a step in a series of steps that are being executed to answer the user's query.
These are all of the steps: {json.dumps(state["steps"])}

You are responsible for carrying out the step: {json.dumps(current_step)}

The current date is {datetime.now().strftime("%Y-%m-%d")}.

This is what you need to search for, please come up with a good search query: {current_step["description"]}
"""
    model = ChatOpenAI(model="gpt-4o").bind_tools(
        [tavily_tool],
        parallel_tool_calls=False,
        tool_choice=tavily_tool.name
    )
    # config = configure_copilotkit(config, emit_messages=True, emit_all=True)

    response = await model.ainvoke([
        *state["messages"],
        SystemMessage(
            content=system_message
        )
    ], config)
    print("LLM response = ", response)

    tool_msg = tavily_tool.invoke(response.tool_calls[0])
    print("tool_msg = ", tool_msg)

#     system_message = f"""
# This task was just executed: {json.dumps(current_step)}

# This is the result of the search: 

# {tool_msg}

# Please summarize the ONLY the result of the search and include all relevant information from the search and reference links.

# DO NOT INCLUDE ANY EXTRA INFORMATION. ALL OF THE INFORMATION YOU ARE LOOKING FOR IS IN THE SEARCH RESULTS.

# DO NOT answer the user's query yet. Just summarize the search results.

# Use markdown formatting and put the references inline and the links at the end.
# Like this:
# This is a sentence with a reference to a source [source 1][1] and another reference [source 2][2].
# [1]: http://example.com/source1 "Title of Source 1"
# [2]: http://example.com/source2 "Title of Source 2"
# """

#     response = await ChatOpenAI(model="gpt-4o").ainvoke([
#         *state["messages"],
#         SystemMessage(content=system_message)
#     ], config)

    current_step["search_result"] = json.loads(tool_msg.content)
    current_step["updates"] = [*current_step["updates"],"Extracting information..."]

    return state
