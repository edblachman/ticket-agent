_Work in progress (learning project)_

# ticket-agent
*An AI agent to analyze GitHub issues, find relevant code, and propose fixes.*

## Overview
The idea here is to explore automating bug validation and resolution using AI. When an ex-coworker told me they'd built a production version of this in half a day, I was inspired to build one for myself and, in so doing, learn both about how such a system would work and about building with an AI partner. I'm building this as a structured learning project, working with Claude both as my learning partner and as the API I'm learning to use. I'm not doing this from a tutorial, nor am I doing it independently; instead, I'm having Claude structure the learning into a sequence of lessons which let me learn various aspects of Python, the Claude API, tool use, and agentic patterns.

## Completed
Lesson 1: Interactive CLI that reads a source file and answers questions about it using the Claude API.
Lesson 2: Tools and their use.

## Upcoming Work:
Lesson 3: Use the GitHub API to work with real repositories.

## Usage
`python interactive_ask_about_file.py <filepath>`
The script repeatedly prompts for a `Question:` where
- "exit" or "quit" exits the script
- "help" prints the list of commands
- anything else is sent to Claude as a question to be answered about the given file

`python interactive_tool_use_with_search.py`
The script repeatedly prompts for a `Question:` where
- "exit" or "quit" exits the script
- "help" prints the list of commands
- anything else is sent to Claude as a question to be answered about files in the current directory

## Stack
Python, Claude API (Anthropic)

## Planned
Tool use for GitHub operations, multi-step reasoning, automated PR generation.