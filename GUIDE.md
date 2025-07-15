# Mistral CLI Setup Guide

This guide will walk you through setting up and running the Mistral CLI as a proper command-line tool.

## Prerequisites

- **Python 3.8+** installed on your system
- **Git** (optional, for cloning the repository)
- **Internet connection** (for installing dependencies and using Research Mode)

## Step 1: Install Ollama

The Mistral CLI uses Ollama to run AI models locally. Follow these steps:

### For macOS:
```bash
# Download and install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Or using Homebrew
brew install ollama
```

### For Linux:
```bash
# Download and install Ollama
curl -fsSL https://ollama.ai/install.sh | sh
```

### For Windows:
1. Download the installer from https://ollama.ai/download
2. Run the installer and follow the setup wizard

## Step 2: Start Ollama and Download the Model

```bash
# Start the Ollama service
ollama serve

# In a new terminal, download the Mistral model
ollama pull mistral
```

**Note:** The `mistral` model is approximately 4GB and may take some time to download.

## Step 3: Install the Mistral CLI

### Option A: Clone and install from repository
```bash
git clone <repository-url>
cd mistral-cli

# Install the CLI package
pip install -e .
```

### Option B: Install from PyPI (when available)
```bash
pip install mistral-cli
```

## Step 4: Test the Installation

Once installed, you can use the CLI with the `mistral-cli` command:

```bash
# Launch interactive mode (default)
mistral-cli

# Single query
mistral-cli "Hello, how are you?"

# Check help
mistral-cli --help
```

## Step 5: Optional Setup for Research Mode

If you want to use Research Mode, configure the search API:

```bash
mistral-cli --setup
```

This will:
1. Verify Ollama is running and the mistral model is available
2. Optionally set up Google Custom Search API for Research Mode (can be skipped)

## Usage Guide

### Basic Commands

```bash
# Direct query
mistral-cli "Your question here"

# Plan mode - generates step-by-step plans
mistral-cli --mode plan "Create a plan to learn Python"

# Code mode - generates code with comments
mistral-cli --mode code "Write a hello world function"

# Code mode without comments
mistral-cli --mode code --no-comments "Write a hello world function"

# Research mode (requires API setup)
mistral-cli --mode research "Latest developments in AI"

# Interactive mode (default)
mistral-cli
```

### Interactive Mode Commands

When you run `mistral-cli` without arguments, you enter interactive mode:

```
> /help              # Show help information
> /mode plan          # Switch to plan mode
> /mode code          # Switch to code mode
> /mode research      # Switch to research mode
> /mode direct        # Switch to direct mode
> /compact            # Manually compact conversation history
> /exit               # Exit interactive mode
```

### Setting Up Research Mode (Optional)

Research Mode requires Google Custom Search API credentials:

1. **Get API Key:**
   - Go to https://console.cloud.google.com/apis/
   - Create a new project or select an existing one
   - Enable "Custom Search API"
   - Create credentials (API key)

2. **Create Custom Search Engine:**
   - Go to https://cse.google.com/cse/
   - Create a new search engine
   - Configure it to search the entire web
   - Note down the Search Engine ID

3. **Configure the CLI:**
   ```bash
   mistral-cli --setup
   ```
   Choose "y" when asked about search API setup and enter your credentials.

## Features Overview

### 1. **Plan Mode**
Generates structured, step-by-step plans for any task or goal.

**Example:**
```bash
mistral-cli --mode plan "Learn machine learning"
```

### 2. **Code Mode**
Generates clean code with optional inline comments and advanced coding features:

**Key Features:**
- **Context-Aware Code Completion:** Remembers previously defined functions, classes, and variables
- **Incremental Code Building:** Automatically detects when you want to build on existing code
- **Template Hints:** Provides guidance for common patterns (Flask, React, Django, etc.)
- **Optimized Token Usage:** Uses 256 tokens for responses to maximize context preservation

**Examples:**
```bash
# With comments
mistral-cli --mode code "Create a REST API endpoint"

# Without comments
mistral-cli --mode code --no-comments "Create a REST API endpoint"

# Incremental building (automatically detected)
mistral-cli --mode code "Add error handling to the previous function"
```

### 3. **Research Mode**
Searches the web and provides answers based on current information.

**Example:**
```bash
mistral-cli --mode research "What are the latest AI breakthroughs in 2024?"
```

### 4. **Context Window Management**
Automatically manages conversation history to prevent token overflow with coding-optimized features:

- **Smart Compaction:** Triggers at 85% for coding sessions, 92% for mixed sessions, 99% for general conversations
- **Coding Context Preservation:** Maintains function definitions, variable names, and imports during compaction
- **Manual Compaction:** Use `/compact` command in interactive mode
- **Token Tracking:** Shows current usage after each response
- **Priority Context:** Preserves coding information over general conversation

## Troubleshooting

### Common Issues

**1. "Ollama connection failed"**
- Make sure Ollama is running: `ollama serve`
- Check if the mistral model is installed: `ollama list`
- If model is missing: `ollama pull mistral`

**2. "Model not loaded"**
- Restart Ollama: Stop the service and run `ollama serve` again
- Verify model availability: `ollama list`

**3. "Search API credentials not configured"**
- Run setup again: `mistral-cli --setup`
- Follow the Google Custom Search API setup instructions

**4. "Failed to generate response"**
- Check if Ollama is running: `ollama serve`
- Try restarting the CLI application
- Verify your internet connection

**5. Context window issues**
- Use `/compact` command to manually reduce context
- The system auto-compacts at 85% for coding sessions, 92% for mixed sessions, 99% for general conversations
- Check token usage with `/help` in interactive mode
- Coding context is automatically preserved during compaction

### Performance Tips

1. **GPU Acceleration:** Ollama automatically uses GPU if available
2. **Model Size:** The `mistral` model provides a good balance of speed and quality
3. **Context Management:** Use `/compact` for long conversations to maintain performance
4. **Coding Optimization:** The CLI is now optimized for coding tasks with 33-50% more usable context
5. **Token Efficiency:** System prompts and context management have been optimized for better token usage
6. **Incremental Building:** Use phrases like "add", "modify", "extend" to trigger incremental code building

## Coding Optimization Features

### Context-Aware Code Completion
The CLI now remembers code elements from previous exchanges:
- **Functions:** Remembers function names and signatures
- **Classes:** Keeps track of class definitions
- **Variables:** Maintains variable names and types
- **Imports:** Preserves import statements

### Incremental Code Building
Automatically detects when you want to build on existing code:
- **Trigger words:** "add", "modify", "update", "extend", "improve", "fix", "change", "enhance"
- **Context preservation:** Maintains relevant code context when building incrementally
- **Smart prompting:** Provides previous code context for seamless continuation

### Template System
Provides hints for common coding patterns:
- **Flask:** Flask app template guidance
- **React:** React component template
- **Django:** Django view template
- **FastAPI:** FastAPI app template
- **Express:** Express.js server template
- **Database:** Database connection patterns
- **Authentication:** Auth middleware patterns

### Token Optimization
- **System prompts:** Compressed by 66-82% for better token efficiency
- **Context management:** Prioritizes coding information over general conversation
- **Smart compaction:** Preserves function definitions and imports during history compression
- **Mode-specific limits:** Optimized response lengths for each mode

## Advanced Configuration

### Custom Model
To use a different model:
```bash
# Pull a different model
ollama pull codellama

# The CLI will need to be modified to use the new model
# Edit mistral_cli.py and change the model_name variable
```

### Configuration File
The CLI stores settings in `~/.mistral_cli_config`:
```json
{
  "search_api_key": "your-api-key",
  "search_engine_id": "your-engine-id"
}
```

### Environment Variables
You can also set up environment variables:
```bash
export MISTRAL_CLI_API_KEY="your-api-key"
export MISTRAL_CLI_ENGINE_ID="your-engine-id"
```

## Getting Help

If you encounter issues:

1. Check the troubleshooting section above
2. Verify all prerequisites are installed
3. Make sure Ollama is running with the mistral model
4. Check your internet connection for Research Mode

## Security Notes

- API keys are stored locally in `~/.mistral_cli_config`
- Never share your Google API credentials
- The CLI does not send data to external servers except for Research Mode
- All AI processing happens locally through Ollama

## What's Next?

Once you have the CLI running:
1. Try different modes to see which works best for your needs
2. Experiment with the interactive mode for ongoing conversations
3. Set up Research Mode for current information queries
4. Use the `/compact` command to manage long conversations

Enjoy using the Mistral CLI! 🚀