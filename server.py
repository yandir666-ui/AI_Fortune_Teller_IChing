# server.py
import sys
import io
import queue
import threading
import time
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from main import IChing

app = FastAPI()

# 允许跨域请求
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class DivinationRequest(BaseModel):
    question: str = ""

# 初始化占卜系统 (确保 Ollama 已运行)
iching_system = IChing(
    ollama_url="http://localhost:11434",
    model="FortuneQwen3_q8:4b",
    verbose=True,  # 必须开启 verbose 才能看到起卦过程
    concise=True
)

class StreamCapture:
    """
    一个文件流对象，用于捕获 sys.stdout 并将其放入队列中。
    这样我们可以通过生成器读取队列，实现流式输出。
    """
    def __init__(self, q):
        self.q = q

    def write(self, text):
        # 将捕获到的文本放入队列
        self.q.put(text)

    def flush(self):
        pass

def run_divination_thread(question: str, q: queue.Queue):
    """
    在独立线程中运行占卜逻辑，并将标准输出重定向到队列。
    """
    # 1. 保存旧的 stdout
    old_stdout = sys.stdout
    # 2. 重定向 stdout 到我们的捕获器
    sys.stdout = StreamCapture(q)

    try:
        # 3. 运行占卜
        # 注意：这里我们调用的是 main.py 里封装好的 divine 方法
        # 我们开启 stream=True，这样 divine 内部处理 AI 响应时也是流式的
        # 但我们需要 iching_system.divine 的输出（包括 print）都进 stdout
        
        # 在 main.py 的 divine 方法中：
        # - 起卦过程是直接 print 的 -> 会被 StreamCapture 捕获
        # - AI 生成部分：
        #   如果 stream=True，它返回 generator。我们需要手动迭代并打印，
        #   以便让 StreamCapture 捕获到。
        
        generator = iching_system.divine(question=question, stream=True)
        
        # 迭代生成器（AI 的输出部分）
        # 这里的 chunk 是 AI 返回的文本片段
        if generator and hasattr(generator, '__iter__') and not isinstance(generator, str):
            for chunk in generator:
                # 这里的 chunk 仅仅是字符串，我们需要 print 出来，
                # 这样它才会进入 sys.stdout (也就是我们的 queue)
                # 注意：main.py 的 divine 方法在使用 stream 时，
                # 内部已经有 print(cleaned_chunk) 了 (看 main.py 第 136 行)
                # 所以我们这里其实只需要消耗生成器即可，不需要重复 print，
                # 否则会打印两遍。
                pass
        
    except Exception as e:
        print(f"\n[Error] 占卜过程中发生错误: {e}")
    finally:
        # 4. 恢复 stdout
        sys.stdout = old_stdout
        # 5. 放入结束标记
        q.put(None) 

@app.post("/api/divine-stream")
def divine_stream(request: DivinationRequest):
    """
    流式接口：实时返回起卦过程的控制台输出 + AI 结果
    """
    # 创建一个线程安全的队列
    q = queue.Queue()

    # 启动后台线程运行占卜
    t = threading.Thread(target=run_divination_thread, args=(request.question, q))
    t.start()

    def event_generator():
        """
        生成器：从队列中读取数据并 yield 给前端
        """
        # 标记是否已经发送过 AI 思考信号
        ai_signal_sent = False
        
        while True:
            # 从队列获取数据 (阻塞等待)
            data = q.get()
            
            # 如果收到 None，说明线程结束
            if data is None:
                break
            
            # 逻辑判断：检测是否要插入“假进度条”的触发信号
            # main.py 中有一句 print("正在请AI大师解卦...")
            # 我们检测这句话，并在其后发送特殊标记
            
            yield data
            
            if "正在请AI大师解卦" in data and not ai_signal_sent:
                yield "\n<<<AI_THINKING>>>\n"
                ai_signal_sent = True

    # 返回流式响应
    return StreamingResponse(event_generator(), media_type="text/plain")

if __name__ == "__main__":
    import uvicorn
    # 启动服务器
    print("服务器已启动: http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)