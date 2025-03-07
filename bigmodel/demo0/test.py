from openai import OpenAI

client = OpenAI(
    base_url="https://api.deepseek.com/",
    api_key=""
)

# 初始化对话历史
messages = []

while True:
    # 获取用户输入
    user_input = input("You: ")

    # 输入 exit 或 quit 退出对话
    if user_input.lower() in ["exit", "quit"]:
        print("对话已结束。")
        break

    # 将用户输入添加到对话历史
    messages.append({"role": "user", "content": user_input})

    try:
        # 调用API生成回复
        completion = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages
        )

        # 获取AI回复内容
        ai_response = completion.choices[0].message.content

        # 将AI回复添加到对话历史
        messages.append({"role": "assistant", "content": ai_response})

        # 打印AI回复
        print("AI:", ai_response)

    except Exception as e:
        print("发生错误:", e)
        break