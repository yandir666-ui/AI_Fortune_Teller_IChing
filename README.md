<div align="center">

# 周易占卜系统

[**中文**](./README.md) | [**English**](./README_EN.md)

</div>

基于传统大衍筮法和Ollama AI的智能周易占卜系统。

## 🌐 在线版本 (Online Version)

我们现在推出了基于 Web 的在线版本，支持通过浏览器直接体验：

- **访问地址**: [**https://askthestalks.com**](https://askthestalks.com)
- **技术说明**: 在线版后端采用 FastAPI 架构，AI 解卦部分调用了 **DeepSeek-V3 API**。


## 功能特点

- 模拟传统大衍筮法起卦过程
- 包含完整的周易64卦卦辞、爻辞数据
- 集成Ollama本地AI进行智能解卦
- 支持自定义问题占卜
- 异步算法优化，解卦响应更迅速

## 环境要求

- Python 3.11
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

# 2. 克隆模型仓库
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
├── Figure_1.png               # 算法随机性分布图
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
```

## 技术特性

### 算法随机性
项目中包含 `Figure_1.png`，该图展示了模拟起卦过程中“分二”步骤的数值分布。系统采用正态分布模拟人手分草的随机性，确保起卦过程符合传统逻辑且具备合理的随机波动，而非简单的均匀随机。

![算法随机性分布图](./Figure_1.png)

### 数据完整性
- 64卦完整数据：包含每卦的卦辞、彖传、象传和六爻爻辞
- 智能解读逻辑：根据变爻数量自动选择解读策略
- 原文引用：AI解卦基于周易原文，准确可靠

## 注意事项

- 请确保Ollama服务正常运行
- 首次使用需下载/创建 FortuneQwen3_q8:4b 模型（4G）
- 可根据需要调整AI模型和参数

## 更新日志

### v1.2 (2026-01-01)
- **上线在线版本**: [askthestalks.com](https://askthestalks.com)
- 后端迁移至 FastAPI，支持高并发。
- AI 模型升级至 **DeepSeek-V3**。
- 增加 SSE 流式输出支持。

### v1.1
- 新增微调后的模型支持
- 增加了异步算法，优化解卦等待体验

### v1.0 (2025-12-28)
- 实现完整的大衍筮法模拟
- 集成64卦完整数据
- Ollama AI解卦功能

## License

MIT
