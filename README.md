# 🧠 RAT (Retrieval Augmented Thinking) With UI

> *Enhancing AI responses through structured reasoning and knowledge retrieval*

RAT is a powerful tool that improves AI responses by leveraging DeepSeek's reasoning capabilities to guide other models through a structured thinking process.

## 💡 Origin & Ideation

The idea for RAT was taken from [Doriandarko's RAT project](https://github.com/Doriandarko/RAT-retrieval-augmented-thinking), which emerged from an interesting discovery about DeepSeek-R1 API capabilities. By setting the final response token to 1 while retrieving the thinking process, it became possible to separate the reasoning stage from the final response generation. This insight led to the development of a two-stage approach that combines DeepSeek's exceptional reasoning abilities with various response models.

## How It Works

RAT employs a two-stage approach in both its implementations:

1. **Reasoning Stage** (DeepSeek): 
   - Uses DeepSeek-Reasoner to generate detailed reasoning and analysis for each query
   - This stage is consistent across both implementations

2. **Response Stage** (Two Options):
   - **Standard Version** (OpenRouter): Uses OpenRouter models to generate responses
   - **Claude Version** (Optional): Uses Claude models with message prefilling capabilities

This dual-stage approach ensures thoughtful, contextually aware, and reliable responses regardless of which response model you choose to use.

## 🎯 Features

- 🤖 **Model Selection**: Flexibility to choose from various OpenRouter models
- 🧠 **Reasoning Visibility**: Toggle visibility of the AI's thinking
- 🔄 **Context Awareness**: Maintains conversation context for more coherent interactions

## ⚙️ Requirements

• Python 3.11 or higher  
• A .env file containing:
  ```plaintext
  # Required for both implementations
  DEEPSEEK_API_KEY=your_deepseek_api_key_here
  
  # Required for standard version (OpenRouter)
  OPENROUTER_API_KEY=your_openrouter_api_key_here
  
  # Optional - only needed if using Claude version
  ANTHROPIC_API_KEY=your_anthropic_api_key_here
  ```

## 🚀 Installation
Standalone installation

1. Clone the repository:
   ```bash
   git clone https://github.com/LeonMelamud/COT-DeepSeek-Claude-RAG.git
   cd COT-DeepSeek-Claude-RAG
   ```


2. Install as a local package:
   ```bash
   pip install -e .
   ```

This will install RAT as a command-line tool, allowing you to run it from anywhere by simply typing `rat`!

## 🐳 Docker Usage

Requirements:
- Docker 20.10.0 or higher
- Docker Compose V2

You can run RAT using Docker in three different modes:

1. CLI Mode:
   ```bash
   docker compose up rat-cli
   ```
   This runs the interactive CLI version of RAT.

2. Web Interface:
   ```bash
   docker compose up rat-web
   ```
   This starts the web server at http://localhost:5000.

3. Test Mode:
   ```bash
   docker compose up test
   ```
   This runs the test suite.

Each mode will automatically build the Docker image if it doesn't exist.

## 🌐 Web Interface

RAT includes a web interface that provides:
- File upload and analysis capabilities (files are temporarily stored in an 'uploads' directory)
- API key management
- Support for both OpenRouter and Claude modes
- Visual display of AI reasoning and responses

To use the web interface:

1. Start the web server:
   ```bash
   # Either using Python directly:
   python -m flask --app web.app run --debug

   # Or using Docker:
   docker compose up rat-web
   ```

2. Open http://localhost:5000 in your browser
3. Configure your API keys if not already set
4. Upload a file for analysis
5. View the AI's reasoning and response

## 📖 Usage

1. Ensure your .env file is configured with the necessary API keys:
   ```plaintext
   # Required for both implementations
   DEEPSEEK_API_KEY=your_deepseek_api_key_here
   
   # Required for standard version (OpenRouter)
   OPENROUTER_API_KEY=your_openrouter_api_key_here
   
   # Optional - only needed if using Claude version
   ANTHROPIC_API_KEY=your_anthropic_api_key_here 
   ```

2. Run RAT from anywhere:
   ```bash
   rat
   ```

3. Available commands:
   - Enter your question to get a reasoned response
   - Use "model <name>" to switch OpenRouter models
   - Type "reasoning" to show/hide the thinking process
   - Type "quit" to exit



## 🚀 Versions
You can also run each script on its own:

### Standard Version (rat.py)
The default implementation using DeepSeek for reasoning and OpenRouter for responses.
Run it using:
```bash
uv run rat.py
```

### Claude-Specific Version (rat-claude.py)
A specialized implementation designed for Claude models that leverages Anthropic's message prefilling capabilities. This version makes Claude believe the reasoning process is its own internal thought process, leading to more coherent and contextually aware responses.
Run it using:
```bash
uv run rat-claude.py
```


## 🤝 Contributing

Interested in improving RAT?

1. Fork the repository
2. Create your feature branch
3. Make your improvements
4. Submit a Pull Request

## 📜 License

This project is available under the MIT License. See the [LICENSE](LICENSE) file for details.

If you use this codebase in your projects, please include appropriate credits:

```plaintext
This project uses RAT (Retrieval Augmented Thinking)
GitHub: https://github.com/LeonMelamud/COT-DeepSeek-Claude-RAG
```
---

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=LeonMelamud/COT-DeepSeek-Claude-RAG&type=Date)](https://star-history.com/#LeonMelamud/COT-DeepSeek-Claude-RAG&Date)
