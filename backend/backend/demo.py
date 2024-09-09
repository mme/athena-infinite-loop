from fastapi import FastAPI
import uvicorn
from copilotkit.integrations.fastapi import add_fastapi_endpoint
from copilotkit import CopilotKitSDK, Action


def greet_user(name):
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
        )
    ],
)

add_fastapi_endpoint(app, sdk, "/copilotkit")

def main():
    """Run the uvicorn server."""
    uvicorn.run("backend.demo:app", host="127.0.0.1", port=8000, reload=True)
