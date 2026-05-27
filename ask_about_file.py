import anthropic
import sys

def ask_about_file(filepath, question):
    with open(filepath, "r") as f:
        file_contents = f.read()

    client = anthropic.Anthropic()

    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1024,
        system="You are a helpful code reviewer. When asked about code, be concise and specific.",
        messages=[
            {
                "role": "user",
                "content": f"Here is the contents of {filepath}:\n\n{file_contents}\n\nQuestion: {question}"
            }
        ]
    )

    return message.content[0].text


if __name__ == "__main__":
    filepath = sys.argv[1]
    question = sys.argv[2]
    print(ask_about_file(filepath, question))