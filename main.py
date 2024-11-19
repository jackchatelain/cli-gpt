import os
from rich import print
from huggingface_hub import InferenceClient

# Get your HuggingFace Access Token from https://huggingface.co/settings/tokens
# Then run this: export CLIGPTTOKEN="hf_xxxxxxYOUR-KEY-HERExxxxxx"
apiKey = os.getenv('CLIGPTTOKEN')
client = InferenceClient(api_key=apiKey)
msg = ""
latestAImsg = ""

# Prompt given to the AI
prompt = "You are a helpful AI assistant."

# AI model to use (must be on HuggingFace)
aiModel = "mistralai/Mistral-7B-Instruct-v0.2"

if prompt == "":
    messages = []
else:
    messages = [
        {
            "role": "system",
            "content": str(prompt)
        }
    ]

print("Type \"/help\" for commands.")

running = True
while running:
    print("[bold]Me[/bold]: ", end="")
    msg = input("")
    doReply = True
    if msg[0] == "/":
        if msg in ["/quit", "/q", "/exit", "/stop"]:
            print("[bold]System[/bold]: Exiting")
            doReply = True
            quit()
        elif msg in ["/clear", "/c", "/forget", "/new"]:
            os.system("clear")
            print("[bold]System[/bold]: Started new chat")
            doReply = False
            if prompt == "":
                messages = []
            else:
                messages = [
                    {
                        "role": "system",
                        "content": str(prompt)
                    }
                ]
        elif msg == "/echo":
            msg = latestAImsg
            doReply = True
        elif msg == "/prompt":
            prompt = str(input("Enter AI prompt for future chats:\n"))
            doReply = False
        elif msg in ["/regenerate", "/regen", "/re", "/r"]:
            doReply = True
        elif msg == "/help":
            doReply = False
            print("""
                Commands:
                /quit, /q - Exit the program
                /clear, /c - Clear chat history
                /regenerate, /r - Regenerate last message
                /echo - Repeat what the AI said back to it
                /prompt - Set prompt for future chats (does not persist after quit)
                /help - Show this help text
                """)
        else:
            print("[bold red]Error[/bold red]: Unknown command. Run /help for more info. Messages starting with / are not passed to the AI.")
            doReply = False
    if doReply:
        msgDict = {
            "role": "user",
            "content": str(msg)
        }
        messages.append(msgDict)

        stream = client.chat.completions.create(
            model=aiModel,
            messages=messages,
            max_tokens=12000,
            stream=True
        )

        print("[bold]AI[/bold]: ", end="")
        reply = ""
        for chunk in stream:
            replyAppend = chunk.choices[0].delta.content
            print(replyAppend, end="")
            reply += replyAppend

        print()
        msgDict = {
            "role": "assistant",
            "content": str(reply)
        }
        latestAImsg = str(reply)
        messages.append(msgDict)