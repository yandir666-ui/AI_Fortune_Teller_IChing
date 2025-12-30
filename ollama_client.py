# -*- coding: utf-8 -*-
"""
Ollama客户端模块
Ollama Client

负责与本地部署的Ollama服务通信，发送prompt并获取AI生成的算命结果
"""

import requests
import json
from typing import Optional, Generator


class OllamaClient:
    """Ollama API客户端"""
    
    def __init__(self, base_url="http://localhost:11434", model="FortuneQwen3_q8:4b"):
        """
        初始化Ollama客户端
        
        Args:
            base_url: Ollama服务地址
            model: 使用的模型名称
        """
        self.base_url = base_url.rstrip('/')
        self.model = model
        self.api_url = f"{self.base_url}/api/generate"
    
    def generate(self, prompt, system_prompt="", temperature=0.7, stream=False):
        """
        生成AI响应
        
        Args:
            prompt: 用户提示词
            system_prompt: 系统提示词
            temperature: 温度参数，控制随机性 (0-1)
            stream: 是否流式输出
            
        Returns:
            str: AI生成的文本 (非流式)
            Generator: 生成器对象 (流式)
        """
        payload = {
            "model": self.model,
            "prompt": prompt,
            "system": system_prompt,
            "temperature": temperature,
            "stream": stream
        }
        
        try:
            if stream:
                return self._stream_generate(payload)
            else:
                return self._sync_generate(payload)
        except requests.exceptions.ConnectionError:
            return f"错误: 无法连接到Ollama服务 ({self.base_url})，请确保Ollama正在运行。"
        except Exception as e:
            return f"错误: {str(e)}"
    
    def _sync_generate(self, payload):
        """同步生成"""
        response = requests.post(self.api_url, json=payload, timeout=120)
        response.raise_for_status()
        
        result = response.json()
        return result.get('response', '')
    
    def _stream_generate(self, payload):
        """流式生成"""
        response = requests.post(self.api_url, json=payload, stream=True, timeout=120)
        response.raise_for_status()
        
        for line in response.iter_lines():
            if line:
                try:
                    chunk = json.loads(line.decode('utf-8'))
                    if 'response' in chunk:
                        yield chunk['response']
                    if chunk.get('done', False):
                        break
                except json.JSONDecodeError:
                    continue
    
    def check_connection(self):
        """
        检查Ollama服务是否可用
        
        Returns:
            bool: 是否连接成功
        """
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def list_models(self):
        """
        列出可用的模型
        
        Returns:
            list: 模型名称列表
        """
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            response.raise_for_status()
            data = response.json()
            return [model['name'] for model in data.get('models', [])]
        except:
            return []


if __name__ == "__main__":
    # 测试代码
    client = OllamaClient(model="FortuneQwen3_q8:4b")
    
    # 检查连接
    if client.check_connection():
        print("✓ 已连接到Ollama服务")
        print(f"可用模型: {client.list_models()}")
        
        # 测试生成
        test_prompt = "请用一句话解释什么是周易。"
        print(f"\n测试提示: {test_prompt}")
        print("响应:", client.generate(test_prompt))
    else:
        print("✗ 无法连接到Ollama服务")
