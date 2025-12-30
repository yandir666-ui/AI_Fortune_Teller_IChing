# 周易占卜系统

基于传统大衍筮法和Ollama AI的智能周易占卜系统。

## 功能特点

- ✨ 模拟传统大衍筮法起卦过程
- 📖 包含完整的周易64卦卦辞、爻辞数据
- 🤖 集成Ollama本地AI进行智能解卦
- 🎯 支持自定义问题占卜
- 🌍 UTF-8编码，跨平台兼容

## 环境要求

- Python 3.7+
- Ollama (本地部署)
- requests库

## 安装步骤

1. 安装Python依赖：
```bash
pip install -r requirements.txt
```

2. 模型准备 (Model Setup)：

该模型已托管在 Hugging Face，需手动下载并导入 Ollama。

```bash
# 1. 确保已安装 git lfs
git lfs install

# 2. 克隆模型仓库 (包含 Modelfile 和 GGUF 权重)
git clone https://huggingface.co/Tbata7/FortuneQwen3_4b

# 3. 进入目录
cd FortuneQwen3_4b

# 4. 创建 Ollama 模型
ollama create FortuneQwen3_q8:4b -f Modelfile

# 5. 验证模型是否可用
ollama run FortuneQwen3_q8:4b
```

## 项目结构

```
AI_furtone_tell_IChing/
├── main.py                    # 主程序入口
├── dayan_divination.py        # 大衍筮法模拟器
├── hexagram_interpreter.py    # 卦象解析与查询
├── ollama_client.py           # Ollama API客户端
├── prompt_templates.py        # AI提示词模板
├── hexagrams_data.json        # 64卦完整数据
├── test_system.py             # 系统测试脚本
├── requirements.txt           # Python依赖
└── README.md                  # 项目文档
```

## 使用方法

### 基本使用

```bash
# 运行完整占卜流程
python main.py
```

按提示输入您的问题，系统将自动起卦并由AI解卦。

### 系统测试

```bash
# 测试系统各模块
python test_system.py
```

### 代码调用

```python
from main import IChing

# 初始化
iching = IChing(
    ollama_url="http://localhost:11434",
    model="FortuneQwen3_q8:4b",
    verbose=True
)

# 占卜
result = iching.divine(question="我的事业发展如何？")
print(result)

# 快速占卜（不显示过程）
result = iching.quick_divine(question="今日运势？")
print(result)
```

## 技术特性

### UTF-8编码
所有Python文件均使用UTF-8编码（`# -*- coding: utf-8 -*-`），确保：
- 中文字符正确处理
- 跨平台兼容性（Windows/Linux/macOS）
- 避免编码错误

### 数据完整性
- **64卦完整数据**：包含每卦的卦辞、彖传、象传和六爻爻辞
- **智能解读逻辑**：根据变爻数量自动选择解读策略
- **原文引用**：AI解卦基于周易原文，准确可靠

### 模块化设计
- **起卦模块**：模拟传统大衍筮法全过程
- **解析模块**：二进制卦象映射与文本提取
- **AI模块**：Ollama API集成与prompt工程
- **主程序**：流程编排与用户交互

## 注意事项

- 请确保Ollama服务正常运行
- 首次使用需下载/创建 FortuneQwen3_q8:4b 模型（约2-4GB）
- 可根据需要调整AI模型和参数

## 更新日志

### v1.0 (2025-12-28)
- ✅ 实现完整的大衍筮法模拟
- ✅ 集成64卦完整数据
- ✅ Ollama AI解卦功能
- ✅ UTF-8编码优化
- ✅ 模块化代码结构

## License

MIT
