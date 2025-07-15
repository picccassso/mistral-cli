# Mistral CLI

A powerful, modular command-line interface for interacting with Mistral 7B and other Ollama-supported language models. Features intelligent context management, multiple interaction modes, web search integration, and automatic token optimization.

## 🚀 Key Features

- **Multiple Interaction Modes**: Direct answers, planning, code generation, and research
- **Intelligent Context Management**: Automatic token tracking with smart compacting
- **Coding Context Detection**: Specialized handling for programming-related queries  
- **Web Search Integration**: Research mode with real-time web search capabilities
- **Interactive CLI**: Full-featured interactive mode with command support
- **Modular Architecture**: Clean, maintainable codebase with focused modules
- **Ollama Integration**: Seamless integration with Ollama for local model inference

## 🎯 What It Does

**Mistral CLI** transforms how you interact with local language models by providing:

### Four Specialized Modes
- **Direct Mode**: Natural conversation for general questions and explanations
- **Plan Mode**: Structured, step-by-step planning and problem-solving
- **Code Mode**: Clean code generation with minimal explanation
- **Research Mode**: AI-powered responses enhanced with real-time web search

### Smart Context Management
- **Automatic Token Tracking**: Real-time monitoring of context window usage
- **Intelligent Compacting**: Preserves important context while optimizing memory
- **Coding Detection**: Enhanced handling for programming discussions
- **Conversation Flow**: Maintains context across long interactive sessions

### Professional CLI Experience
- **Interactive Mode**: Persistent conversations with command support (`/help`, `/mode`, `/compact`)
- **Single Query Mode**: Direct command-line usage for quick questions
- **Error Handling**: Graceful failures with informative messages
- **Model Flexibility**: Support for various Ollama-compatible models

## 🏗️ Architecture Achievement

**Before**: Monolithic 1,138-line main.py file  
**After**: Modular architecture with 163-line orchestrator (86% reduction)

```
mistral_cli/
├── main.py              # Entry point and orchestration (163 lines)
├── config.py            # Configuration management  
├── constants.py         # Project constants and settings
├── token_manager.py     # Token counting and optimization
├── coding_context.py    # Programming context detection
├── history_manager.py   # Conversation history management
├── ollama_client.py     # Ollama API integration
├── research_engine.py   # Web search and research
├── query_processor.py   # Query validation and mode switching
├── setup_manager.py     # Initial setup and configuration
└── interactive_cli.py   # Interactive mode implementation
```

**Benefits**: Maintainable, testable, scalable, and debuggable codebase with clear separation of concerns.

## 🚀 Quick Start

See **[GUIDE.md](GUIDE.md)** for complete installation and usage instructions.

**Prerequisites**: Python 3.7+, Ollama installed with a language model

**Basic Usage**:
```bash
# Install and setup
pip install -e .
mistral-cli --setup

# Interactive mode
mistral-cli

# Direct queries
mistral-cli "Explain quantum computing"
mistral-cli --mode code "Create a REST API"
mistral-cli --mode research "Latest AI developments"
```

## 📊 Performance & Design


- **Memory Efficient**: Smart context management prevents bloat
- **Local Inference**: No external dependencies for core functionality  
- **Modular Design**: Single-responsibility modules for maintainability
- **Fast Responses**: Optimized token handling and prompt formatting

## 🎨 Example Interactions

**Planning**: "Create a study schedule for learning Python"  
**Coding**: "Write a React component for a todo list"  
**Research**: "Latest developments in AI safety 2024"  
**Direct**: "Explain the difference between lists and tuples"


See [GUIDE.md](GUIDE.md) for development setup instructions.

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

## 🙏 Acknowledgments

- [Ollama](https://ollama.ai/) for local model inference
- [Mistral AI](https://mistral.ai/) for the language models  
- The open-source AI community

---

**A modular, intelligent CLI that makes local AI models more powerful and accessible.**