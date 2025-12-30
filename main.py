# -*- coding: utf-8 -*-
"""
周易占卜主程序
I-Ching Divination Main Program

整合所有模块，提供完整的周易占卜功能
"""

import sys
import re
from pathlib import Path

# 导入自定义模块
from dayan_divination import DayanDivination
from hexagram_interpreter import HexagramInterpreter
from ollama_client import OllamaClient
from prompt_templates import PromptTemplates


def clean_markdown(text):
    """
    清除文本中的Markdown格式符号
    
    Args:
        text: 原始文本
        
    Returns:
        str: 清除格式后的文本
    """
    # 去除加粗 **text** 或 __text__
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
    text = re.sub(r'__([^_]+)__', r'\1', text)
    
    # 去除斜体 *text* 或 _text_
    text = re.sub(r'\*([^*]+)\*', r'\1', text)
    text = re.sub(r'_([^_]+)_', r'\1', text)
    
    # 去除标题标记 # ## ###
    text = re.sub(r'^#{1,6}\s+', '', text, flags=re.MULTILINE)
    
    # 去除代码块标记 ``` 或 `
    text = re.sub(r'```[^`]*```', '', text)
    text = re.sub(r'`([^`]+)`', r'\1', text)
    
    return text


class IChing:
    """周易占卜系统"""
    
    def __init__(self, ollama_url="http://localhost:11434", 
                 model="FortuneQwen3_q8:4b",
                 data_path="hexagrams_data.json",
                 verbose=True,
                 concise=False):
        """
        初始化周易占卜系统
        
        Args:
            ollama_url: Ollama服务地址
            model: 使用的AI模型
            data_path: 卦象数据文件路径
            verbose: 是否显示详细起卦过程
            concise: 是否使用精简输出模式（默认False）
        """
        self.divination = DayanDivination(verbose=verbose)
        self.interpreter = HexagramInterpreter(data_path=data_path)
        self.ollama = OllamaClient(base_url=ollama_url, model=model)
        self.verbose = verbose
        self.concise = concise
    
    def divine(self, question="", stream=False):
        """
        执行完整的占卜流程 (异步优化版)
        
        Args:
            question: 占卜问题
            stream: 是否流式输出AI响应
            
        Returns:
            str: AI解卦结果 (非流式)
            Generator: 生成器 (流式)
        """
        import threading
        import queue

        # 1. 检查Ollama连接
        if not self.ollama.check_connection():
            return "错误: 无法连接到Ollama服务，请确保Ollama正在运行。"
        
        # 2. 立即计算卦象结果 (不含显示)
        #    利用 refactor 后的 simulate 方法瞬间得到结果
        simulation_data = self.divination.simulate()
        divination_result = simulation_data["hex_result"]

        # 3. 解析卦象
        interpretation = self.interpreter.interpret_divination_result(divination_result)
        
        # 4. 构建卦象信息与 Prompt
        original_hex = interpretation['original_hexagram']
        changed_hex = interpretation['changed_hexagram']
        
        if original_hex is None:
            return f"错误: 无法找到卦象数据。二进制: {divination_result['original_binary']}"
        
        hexagram_info = f"本卦: {original_hex.get('name_cn', '未知')}卦 (第{original_hex.get('number', '?')}卦)"
        if changed_hex:
            hexagram_info += f"\n之卦: {changed_hex.get('name_cn', '未知')}卦 (第{changed_hex.get('number', '?')}卦)"
        if interpretation['changing_lines']:
            hexagram_info += f"\n变爻: 第{interpretation['changing_lines']}爻"
        
        user_prompt, system_prompt = PromptTemplates.build_divination_prompt(
            question=question,
            hexagram_info=hexagram_info,
            interpretation_guide=interpretation['interpretation_guide'],
            original_text=interpretation['original_text'],
            changed_text=interpretation['changed_text'],
            concise=self.concise
        )

        # 5. 启动后台线程请求 AI
        #    使用 Queue 来传递 AI 的响应结果
        ai_response_queue = queue.Queue()
        
        def ai_worker():
            try:
                # 获取完整响应（即使前端要求流式，我们也先在后台获取生成器或完整文本）
                # 这里为了配合前端流式体验，如果是 stream=True，我们将生成器放入 queue
                # 如果是 stream=False，我们将完整字符串放入 queue
                res = self.ollama.generate(
                    prompt=user_prompt,
                    system_prompt=system_prompt,
                    temperature=0.7,
                    stream=stream
                )
                ai_response_queue.put(res)
            except Exception as e:
                ai_response_queue.put(e)

        ai_thread = threading.Thread(target=ai_worker)
        ai_thread.start()

        # 6. 当 AI 在后台思考时，前台播放大衍筮法动画
        if self.verbose:
            print("\n" + "="*60)
            print("开始起卦...")
            print("="*60)
            
            # 播放动画 (耗时过程)
            self.divination.play_process(simulation_data)
            
            print("\n" + "="*60)
            print("正在请AI大师解卦...")
            print("="*60 + "\n")

        # 7. 等待 AI 线程完成 (通常动画播放完，AI也差不多好了)
        ai_thread.join()
        
        # 获取结果
        response = ai_response_queue.get()
        
        if isinstance(response, Exception):
            return f"错误: AI生成失败 - {str(response)}"

        # 8. 处理并返回输出
        if stream:
            # 流式输出
            def stream_wrapper():
                # response 是一个 generator
                for chunk in response:
                    cleaned_chunk = clean_markdown(chunk)
                    if self.verbose:
                        print(cleaned_chunk, end='', flush=True)
                    yield cleaned_chunk
                if self.verbose:
                    print("\n")
            return stream_wrapper()
        else:
            # 一次性输出
            cleaned_response = clean_markdown(response)
            if self.verbose:
                print(cleaned_response)
                print("\n" + "="*60)
            return cleaned_response
    
    def quick_divine(self, question=""):
        """
        快速占卜（不显示详细过程）
        
        Args:
            question: 占卜问题
            
        Returns:
            str: AI解卦结果
        """
        original_verbose = self.verbose
        self.divination.verbose = False
        self.verbose = False
        
        result = self.divine(question=question, stream=False)
        
        self.divination.verbose = original_verbose
        self.verbose = original_verbose
        
        return result


def main():
    """主函数 - 命令行交互"""
    print("\n" + "="*60)
    print("           周 易 占 卜 系 统")
    print("="*60)
    print("基于大衍筮法 + Ollama AI 解卦\n")
    
    # 初始化系统（使用精简模式）
    iching = IChing(
        ollama_url="http://localhost:11434",
        model="FortuneQwen3_q8:4b",
        verbose=True,
        concise=True  # 默认使用精简模式，可改为False使用详细模式
    )
    
    # 检查连接
    if not iching.ollama.check_connection():
        print("错误: 无法连接到Ollama服务")
        print("请确保:")
        print("  1. Ollama已安装并运行")
        print("  2. 服务地址正确 (默认: http://localhost:11434)")
        print("  3. 已下载模型 (如: ollama run FortuneQwen3_q8:4b)")
        return
    
    print(f"✓ 已连接到Ollama服务")
    print(f"✓ 使用模型: {iching.ollama.model}")
    
    # 获取问题
    print("\n" + "-"*60)
    question = input("请输入您的占卜问题（直接回车则不指定问题）: ").strip()
    
    # 执行占卜
    print("\n" + "="*60)
    print("开始占卜...")
    print("="*60)
    
    # 使用流式输出
    result_generator = iching.divine(question=question, stream=True)
    
    # 消费生成器
    for _ in result_generator:
        pass
    
    print("\n" + "="*60)
    print("占卜完成")
    print("="*60)


if __name__ == "__main__":
    main()
