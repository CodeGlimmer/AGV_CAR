from openai import OpenAI

client = OpenAI(
    base_url="https://api.deepseek.com/",
    api_key="sk-026be70f5fef45c380a46b8edcdb3f24"
)

completion = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {
                "role": "user",
                "content":"who are you?"
        }
    ]
)

print(completion.choices[0].message.content)

# fp = open('hh.md', 'w')
# fp.write(completion.choices[0].message.content)
# fp.close()