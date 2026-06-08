import anthropic
import os
import re

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
    },
    {
        "name": "search_files",
        "description": "Search for files with a specific pattern",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "The directory path to search in"
                },
                "pattern": {
                    "type": "string",
                    "description": "The pattern to search for"
                }
            },
            "required": ["path", "pattern"]
        }
    }
]

def read_file(path):
    with open(path, "r") as f:
        return f.read()

def list_directory(path):
    entries = os.listdir(path)
    return "\n".join(sorted(entries))

def search_files(path, pattern):
    results = []
    
    for dirpath, dirs, files in os.walk(path):
        for filename in files:
            filepath = os.path.join(dirpath, filename)
            try:
                with open(filepath, "r") as f:
                    for line_num, line in enumerate(f, start=1):
                        if re.search(pattern, line):
                            results.append(f"{filepath}:{line_num}: {line.rstrip()}")
            except (UnicodeDecodeError, PermissionError):
                continue
    
    if not results:
        return "No matches found."
    
    return "\n".join(results)

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
    if tool_name == "search_files":
        try:
            return search_files(tool_input["path"], tool_input["pattern"])
        except FileNotFoundError:
            return f"Error: file not found: {tool_input['path']}"
        except (SyntaxError, re.PatternError):
            return f"Improper regex syntax: {tool_input['pattern']}"
    raise ValueError(f"Unknown tool: {tool_name}")

def run_agent(messages, tools):
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

messages = [
    {"role": "user", "content": "where in this directory is the Anthropic client created?"}
]

run_agent(messages, tools)