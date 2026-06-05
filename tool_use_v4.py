import anthropic
import os

client = anthropic.Anthropic()

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
    },
    {
        "name": "list_directory",
        "description": "List the files in a directory",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "The directory path to list"
                }
            },
            "required": ["path"]
        }
    }
]

def read_file(path):
    with open(path, "r") as f:
        return f.read()

def list_directory(path):
    entries = os.listdir(path)
    return "\n".join(sorted(entries))

def run_tool(tool_name, tool_input):
    if tool_name == "read_file":
        try:
            return read_file(tool_input["path"])
        except FileNotFoundError:
            return f"Error: file not found: {tool_input['path']}"
    if tool_name == "list_directory":
        try:
            return list_directory(tool_input["path"])
        except FileNotFoundError:
            return f"Error: directory not found: {tool_input['path']}"
    raise ValueError(f"Unknown tool: {tool_name}")

messages = [
    {"role": "user", "content": "What Python files are here and what does goodbye_claude.py do?"}
]

# First API call
response = client.messages.create(
    model="claude-opus-4-5",
    max_tokens=1024,
    tools=tools,
    messages=messages
)

# Handle tool use
# Handle tool use loop
while response.stop_reason == "tool_use":
    # Find ALL tool use blocks
    tool_blocks = [b for b in response.content if b.type == "tool_use"]
    
    # Execute all of them and collect results
    tool_results = []
    for tool_block in tool_blocks:
        result = run_tool(tool_block.name, tool_block.input)
        tool_results.append({
            "type": "tool_result",
            "tool_use_id": tool_block.id,
            "content": result
        })
    
    # Add Claude's response and ALL tool results to the conversation
    messages.append({"role": "assistant", "content": response.content})
    messages.append({"role": "user", "content": tool_results})
    
    # Make the next API call
    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1024,
        tools=tools,
        messages=messages
    )

print(response.content[0].text)