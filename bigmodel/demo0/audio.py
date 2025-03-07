import wave
import pyaudio
from aip import AipSpeech


class Audio:

    def __init__(self, app_id, api_key, api_secret, format,
                 channels, rate, record_seconds, chunk, file_path='temp.wav'):
        self.client = AipSpeech(app_id, api_key, api_secret)
        self.format = format
        self.channels = channels
        self.rate = rate
        self.record_seconds = record_seconds
        self.chunk = chunk
        self.file_path = file_path

    def get_audio(self):
        isstart = input("是否开始录音？(0为退出 1为开始)")
        if isstart == "1":
            pa = pyaudio.PyAudio()
            stream = pa.open(format=self.format,
                             channels=self.channels,
                             rate=self.rate,
                             input=True,
                             frames_per_buffer=self.chunk)
            print("*" * 10, f"开始录音：请在{self.record_seconds}秒内输入语音")

            frames = []
            for i in range(0, int(self.rate / self.chunk * self.record_seconds)):
                data = stream.read(self.chunk)  # 读取chunk个字节 保存到data中
                frames.append(data)  # 向列表frames中添加数据data
            print("*" * 10, "录音结束\n")
            stream.stop_stream()
            stream.close()  # 停止数据流
            pa.terminate()  # 关闭PyAudio

            # 写入录音文件
            self.save_wave_file(pa, frames)
        elif isstart == "0":
            exit()
        else:
            print("无效输入，请重新选择")
            self.get_audio()


    def save_wave_file(self, pa, data):
        wf = wave.open(self.file_path, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(pa.get_sample_size(self.format))
        wf.setframerate(self.rate)
        wf.writeframes(b"".join(data))
        wf.close()


    def get_file_content(self):
        with open(self.file_path, 'rb') as fp:
            return fp.read()

    def get_result(self) -> str:
        result = self.client.asr(self.get_file_content(), 'wav',16000,{'dev_pid': 1537,})
        return result['result'][0]

    def __call__(self):
        self.get_audio()
        return self.get_result()