from openai import OpenAI

client = OpenAI(
    base_url="https://api.deepseek.com/", 
    api_key="" #api key
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