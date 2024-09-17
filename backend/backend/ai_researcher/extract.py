"""
The extract node is responsible for extracting information from a tavily search.
"""
import json

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage
from copilotkit.langchain import configure_copilotkit

from langchain_core.runnables import RunnableConfig

from .state import AgentState

async def extract_node(state: AgentState, config: RunnableConfig):
    """
    The extract node is responsible for extracting information from a tavily search.
    """
    config = configure_copilotkit(config, emit_tool_calls=True)
    current_step = next((step for step in state["steps"] if step["status"] == "pending"), None)

    if current_step is None:
        raise ValueError("No current step")

    if current_step["type"] != "search":
        raise ValueError("Current step is not of type search")

    system_message = f"""
This step was just executed: {json.dumps(current_step)}

This is the result of the search:

Please summarize ONLY the result of the search and include all relevant information from the search and reference links.
DO NOT INCLUDE ANY EXTRA INFORMATION. ALL OF THE INFORMATION YOU ARE LOOKING FOR IS IN THE SEARCH RESULTS.

DO NOT answer the user's query yet. Just summarize the search results.

Use markdown formatting and put the references inline and the links at the end.
Like this:
This is a sentence with a reference to a source [source 1][1] and another reference [source 2][2].
[1]: http://example.com/source1 "Title of Source 1"
[2]: http://example.com/source2 "Title of Source 2"
"""
    try: 
        print("Extracting information from the search results...")
        print("Current step: ", current_step)
        print("State: ", state)
        # config = configure_copilotkit(config,emit_messages=True, emit_all=True)

        response = await ChatOpenAI(model="gpt-4o").ainvoke([
            *state["messages"],
                SystemMessage(content=system_message)
            ], config)
        print("Response: ", response)
        print("Response content: ", response.content)

        current_step["result"] = response.content
        current_step["search_result"] = None
        current_step["status"] = "complete"
        current_step["updates"] = [*current_step["updates"], "Done."]

        next_step = next((step for step in state["steps"] if step["status"] == "pending"), None)
        print("next step: ", next_step)
        if next_step:
            next_step["updates"] = ["Searching the web..."]

        return state

    except Exception as e:
        print("Error in extract_node: ", e)
        # raise e
        return "Error in extract_node"  + str(e)
