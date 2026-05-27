import anthropic

client = anthropic.Anthropic()

message = client.messages.create(
    model="claude-opus-4-5",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Say hello and tell me what you are in one sentence."}
    ]
)

print(message.content[0].text)