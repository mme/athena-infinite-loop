"""
This is a demo of the CopilotKit SDK.
"""
import os
from fastapi import FastAPI
import uvicorn
from copilotkit.integrations.fastapi import add_fastapi_endpoint
from copilotkit import CopilotKitSDK, Action, LangGraphAgent
from backend.joke_agent import joke_graph
from backend.email_agent import email_graph
from backend.ai_researcher.agent import graph as ai_researcher_graph


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
            parameters=[
                {
                    "name": "name",
                    "description": "The name of the user to greet.",
                    "type": "string",
                },               
            ]
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
            description="Search agent.",
            agent=ai_researcher_graph,
        )
    ],

)

add_fastapi_endpoint(app, sdk, "/copilotkit")


# add new route for health check
@app.get("/health")
def health():
    """Health check."""
    return {"status": "ok"}


port = int(os.getenv("PORT", "8000"))
host = "0.0.0.0" if os.getenv("RENDER") else "127.0.0.1" # pylint: disable=C0103

def main():
    """Run the uvicorn server."""
    uvicorn.run("backend.demo:app", host=host, port=port, reload=True)
