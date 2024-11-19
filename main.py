import os
from huggingface_hub import InferenceClient

# Get your HuggingFace Access Token from https://huggingface.co/settings/tokens
# Then run this: export CLIGPTTOKEN="hf_xxxxxxYOUR-KEY-HERExxxxxx"
apiKey = os.getenv('CLIGPTTOKEN')
client = InferenceClient(api_key=apiKey)
msg = ""

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

print("Type \"quit\" to exit the chat.")

running = True
while running:
    msg = input("Me: ")
    if msg == "quit":
        print("System: Exiting")
        quit()
    msgDict = {
        "role": "user",
        "content": str(msg)
    }
    messages.append(msgDict)

    stream = client.chat.completions.create(
        model=aiModel,
        messages=messages,
        max_tokens=5000,
        stream=True
    )

    print("AI: ", end="")
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
    messages.append(msgDict)