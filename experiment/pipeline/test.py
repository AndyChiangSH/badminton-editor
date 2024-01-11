from openai import OpenAI
import os

print("OPENAI_API_KEY:", os.getenv("OPENAI_API_KEY", default=None))

client = OpenAI()

completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
        {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
    ]
)

print("message:", completion.choices[0].message)
print("content:", completion.choices[0].message.content)
