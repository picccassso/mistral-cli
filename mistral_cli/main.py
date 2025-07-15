#!/usr/bin/env python3
"""Mistral 7B CLI Wrapper - Main entry point."""

import argparse
import sys
from pathlib import Path
from typing import Optional

from .config import (
    get_model_path, save_model_path, validate_model_path,
    get_search_api_key, save_search_api_key, 
    get_search_engine_id, save_search_engine_id
)
from .constants import (
    AVAILABLE_MODES, MODEL_NAME, OLLAMA_URL, MAX_CONTEXT_TOKENS,
    PLAN_SYSTEM_PROMPT, CODE_SYSTEM_PROMPT, CODE_SYSTEM_PROMPT_NO_COMMENTS,
    RESEARCH_SYSTEM_PROMPT, COMPACT_SYSTEM_PROMPT,
    MAX_CONTEXT_TOKENS_FOR_PROMPT,
    MAX_CODING_EXCHANGES_TO_PRESERVE, MAX_GENERAL_EXCHANGES_TO_PRESERVE
)
from .token_manager import (
    estimate_tokens, get_current_token_count, get_dynamic_compact_threshold,
    should_compact, get_optimal_response_tokens
)
from .coding_context import (
    is_coding_related, extract_coding_context, extract_code_definitions,
    get_coding_context_summary, get_code_template_hint, build_incremental_code_prompt
)
from .history_manager import (
    add_to_history, format_conversation_history, prioritize_context_for_prompt,
    format_history_for_prompt, compact_conversation
)
from .ollama_client import (
    check_ollama_connection, generate_response, load_model_from_config
)
from .research_engine import (
    search_web, extract_text_from_url, research_query
)
from .query_processor import (
    validate_mode, switch_mode, process_query
)
from .setup_manager import (
    setup_ollama
)
from .interactive_cli import (
    interactive_mode
)

# Phase 3 imports for AI functionality
try:
    import requests
    import json
    from bs4 import BeautifulSoup
    from urllib.parse import urljoin, urlparse
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False
    requests = None
    json = None
    BeautifulSoup = None
    urljoin = None
    urlparse = None

# Global state
current_mode = "direct"
model_loaded = False
conversation_history = []


def main():
    """Main entry point for the Mistral CLI application."""
    parser = argparse.ArgumentParser(
        description="Mistral CLI - A command-line interface for Mistral 7B model",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  mistral-cli                           Launch interactive mode (default)
  mistral-cli --setup                   Configure search API (one-time setup)
  mistral-cli "Hello, how are you?"     Run single query in direct mode
  mistral-cli --mode plan "Create a plan to learn Python"
  mistral-cli --mode code "Write a hello world function"
  mistral-cli --mode research "Latest AI developments"
  mistral-cli --help                    Show this help message

Features:
- Direct Mode: Natural conversation
- Plan Mode: Step-by-step planning
- Code Mode: Code generation with/without comments
- Research Mode: Web search + AI responses
- Context Management: Automatic conversation summarization
- Interactive Commands: /help, /mode, /compact, /exit
        """
    )
    
    parser.add_argument(
        "--setup",
        action="store_true",
        help="Run one-time setup to configure model path"
    )
    
    parser.add_argument(
        "--mode",
        choices=["research", "plan", "code"],
        help="Specify operating mode: research (web search + AI), plan (reasoning), or code (code generation)"
    )
    
    parser.add_argument(
        "--no-comments",
        action="store_true",
        help="For code mode: generate code without inline comments"
    )
    
    parser.add_argument(
        "query",
        nargs="?",
        help="Query text to process (if omitted, launches interactive mode)"
    )
    
    args = parser.parse_args()
    
    # Handle setup command
    if args.setup:
        if setup_ollama():
            print("\n🎉 Setup completed successfully!")
            print("You can now run 'mistral-cli' to use the application.")
        else:
            print("\n❌ Setup failed. Please try again.")
            sys.exit(1)
        return
    
    # Normal application startup - streamlined
    print("🔄 Connecting to Ollama...")
    
    # Check Ollama connection
    global model_loaded
    model_loaded = load_model_from_config()
    if not model_loaded:
        print("⚠️  Ollama connection failed.")
        print("Please ensure:")
        print("1. Ollama is installed and running (ollama serve)")
        print(f"2. {MODEL_NAME} model is available (ollama pull {MODEL_NAME})")
        print()
        print("Run 'mistral-cli --setup' for guided setup.")
        sys.exit(1)
    
    # Handle mode and query processing
    global current_mode
    
    # Set mode if specified
    if args.mode:
        current_mode = args.mode
    
    # Process based on arguments
    if args.query:
        # Direct query processing
        process_query(conversation_history, model_loaded, current_mode, args.query, current_mode, args.no_comments)
    else:
        # Launch interactive mode
        current_mode_container = [current_mode]
        interactive_mode(conversation_history, model_loaded, current_mode_container)


if __name__ == "__main__":
    main() 