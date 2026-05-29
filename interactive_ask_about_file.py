import anthropic
import sys

def ask_about_file(filepath):
    with open(filepath, "r") as f:
        file_contents = f.read()

    client = anthropic.Anthropic()
    
    print(f"Loaded {filepath}. Ask questions about it (type 'quit' to exit).\n")

    while True:
        question = input("Question: ").strip()
        
        if question.lower() in ("quit", "exit", "q"):
            break

        if question.lower() in ("help", "h"):
            print("Ask any question about the code in the file. Type 'help' to repeat this message or 'quit' to exit.")
            continue
            
        if not question:
            continue

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

        print("\n" + message.content[0].text + "\n")


if __name__ == "__main__":
    filepath = sys.argv[1]
    ask_about_file(filepath)