from openai import OpenAI
from audio import Audio
import pyaudio

# 百度api
APP_ID = ''
API_KEY = ''
SECRET_KEY = ''

# DeepSeek api
DS_API_KEY = ""


# 录制参数
CHUNK = 1024
FORMAT = pyaudio.paInt16 # 16位深
CHANNELS = 1 #1是单声道，2是双声道。
RATE = 16000 # 采样率，调用API一般为8000或16000
RECORD_SECONDS = 10 # 录制时间10s


def main():

    client = OpenAI(
        base_url="https://api.deepseek.com/",
        api_key="4"
    )

    # 初始化对话历史
    messages = []

    ad = Audio(app_id=APP_ID,
               api_key=API_KEY,
               api_secret=SECRET_KEY,
               format=FORMAT,
               chunk=CHUNK,
               channels=CHANNELS,
               rate=RATE,
               record_seconds=RECORD_SECONDS,
               )
    while True:
        # 获取用户输入
        user_input = ad()

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


if __name__ == "__main__":
    main()