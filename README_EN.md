<div align="center">

# I-Ching Divination System

[**中文**](./README.md) | [**English**](./README_EN.md)

</div>

An intelligent I-Ching divination system based on traditional Dayan stalks method and Ollama AI.

## Features

- Simulates the traditional Dayan stalks divination process
- Contains complete data for all 64 hexagrams (judgments and line texts)
- Integrates local Ollama AI for intelligent interpretation
- Supports customized questions for divination
- Optimized with asynchronous algorithms for faster AI responses

## Requirements

- Python 3.11
- Ollama (locally deployed)
- requests library

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Model Setup:

The model is hosted on Hugging Face and needs to be downloaded and imported into Ollama manually.

```bash
# 1. Ensure git lfs is installed
git lfs install

# 2. Clone the model repository
git clone https://huggingface.co/Tbata7/FortuneQwen3_4b

# 3. Enter the directory
cd FortuneQwen3_4b

# 4. Create the Ollama model
ollama create FortuneQwen3_q8:4b -f Modelfile

# 5. Verify the model
ollama run FortuneQwen3_q8:4b
```

## Project Structure

```
AI_furtone_tell_IChing/
├── main.py                    # Main program entry
├── dayan_divination.py        # Dayan divination simulator
├── hexagram_interpreter.py    # Hexagram analysis and query
├── ollama_client.py           # Ollama API client
├── prompt_templates.py        # AI prompt templates
├── hexagrams_data.json        # 64 hexagram data
├── Figure_1.png               # Algorithm randomness distribution chart
├── requirements.txt           # Python dependencies
└── README.md                  # Project documentation
```

## Usage

### Basic Usage

```bash
# Run the full divination process
python main.py
```

Follow the prompts to enter your question; the system will automatically cast the hexagram and provide an AI interpretation.

### Code Integration

```python
from main import IChing

# Initialization
iching = IChing(
    ollama_url="http://localhost:11434",
    model="FortuneQwen3_q8:4b",
    verbose=True
)

# Divination
result = iching.divine(question="How is my career development?")
print(result)
```

## Technical Features

### Algorithm Randomness
The `Figure_1.png` file in the project illustrates the numerical distribution of the "Split into Two" step during the casting process. The system uses a normal distribution to simulate the randomness of manual stalk splitting, ensuring the process aligns with traditional logic with natural fluctuations rather than simple uniform randomness.

![Algorithm Randomness Distribution Chart](./Figure_1.png)

### Data Integrity
- Complete 64 Hexagram Data: Includes judgments, Tuan, Xiang, and line texts for every hexagram.
- Intelligent Interpretation: Automatically selects interpretation strategies based on the number of changing lines.
- Scriptural Citations: AI interpretations are based on original I-Ching texts, ensuring accuracy and reliability.

## Notes

- Ensure the Ollama service is running properly.
- First-time use requires downloading/creating the FortuneQwen3_q8:4b model (4G).
- AI models and parameters can be adjusted as needed.

## Changelog

### v1.1 (Current)
- Added support for the fine-tuned model.
- Integrated asynchronous algorithms to optimize response wait time.

### v1.0 (2025-12-28)
- Implemented full Dayan stalks simulation.
- Integrated complete 64 hexagram data.
- Added Ollama AI interpretation functionality.

## License

MIT
