"""
This is a demo of the CopilotKit SDK.
"""
from fastapi import FastAPI
import uvicorn
from copilotkit.integrations.fastapi import add_fastapi_endpoint
from copilotkit import CopilotKitSDK, Action, LangGraphAgent
from backend.joke_agent import joke_graph
from backend.email_agent import email_graph
from backend.ai_researcher.demo import graph as ai_researcher_graph


def greet_user(name):
    """Greet the user."""
    print(f"Hello, {name}!")
    return "The user has been greeted. Tell them to check the console."

app = FastAPI()
sdk = CopilotKitSDK(
    actions=[
        Action(
            name="greet_user",
            description="Greet the user.",
            handler=greet_user,
            parameters=[{
                "name": "name",
                "description": "The name of the user to greet.",
                "type": "string",
            }]
        ),
    ],
    agents=[
        LangGraphAgent(
            name="joke_agent",
            description="Make a joke.",
            agent=joke_graph,
        ),
        LangGraphAgent(
            name="email_agent",
            description="Write an email.",
            agent=email_graph,
        ),
        LangGraphAgent(
            name="ai_researcher",
            description="Research a topic.",
            agent=ai_researcher_graph,
        ),
    ],
)

add_fastapi_endpoint(app, sdk, "/copilotkit")

def main():
    """Run the uvicorn server."""
    uvicorn.run("backend.demo:app", host="127.0.0.1", port=8000, reload=True)
