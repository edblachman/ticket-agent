import anthropic
import os

client = anthropic.Anthropic()

# Define a tool that reads a file
tools = [
    {
        "name": "read_file",
        "description": "Read the contents of a file at the given path",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "The path to the file to read"
                }
            },
            "required": ["path"]
        }
    }
]

def read_file(path):
    with open(path, "r") as f:
        return f.read()

messages = [
    {"role": "user", "content": "Read the file hello_claude.py and tell me what it does."}
]

response = client.messages.create(
    model="claude-opus-4-5",
    max_tokens=1024,
    tools=tools,
    messages=messages
)

print("Stop reason:", response.stop_reason)
print("Response:", response.content)