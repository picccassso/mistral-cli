#!/usr/bin/env python3
"""Interactive CLI Module - Interactive mode and command handling."""

from typing import List, Dict, Any
from .constants import MODEL_NAME, AVAILABLE_MODES, MAX_CONTEXT_TOKENS
from .token_manager import get_current_token_count
from .history_manager import compact_conversation
from .ollama_client import generate_response
from .query_processor import switch_mode, process_query


def interactive_mode(conversation_history: List[Dict[str, str]], model_loaded: bool, 
                    current_mode_container: List[str]) -> None:
    """Run the CLI in interactive mode with command loop.
    
    Args:
        conversation_history: List of conversation exchanges.
        model_loaded: Whether the model is loaded and ready.
        current_mode_container: List containing current mode (for mutability).
    """
    current_mode = current_mode_container[0]
    
    print("🚀 Mistral CLI")
    print("=" * 50)
    print(f"✅ Connected to Ollama • Model: {MODEL_NAME}")
    print(f"🔧 Current mode: {current_mode}")
    print()
    print("💡 Quick start:")
    print("  Just type your question or request")
    print("  Type /help for commands and modes")
    print("  Type /exit to quit")
    print()
    
    # Show context status
    current_tokens = get_current_token_count(conversation_history)
    usage_percent = (current_tokens / MAX_CONTEXT_TOKENS) * 100
    print(f"📊 Context: {current_tokens}/{MAX_CONTEXT_TOKENS} tokens ({usage_percent:.1f}%)")
    print()
    
    while True:
        try:
            user_input = input("> ").strip()
            
            if not user_input:
                continue
                
            # Handle slash commands
            if user_input.startswith("/"):
                command_parts = user_input[1:].split()
                if not command_parts:
                    print("❌ Empty command")
                    continue
                    
                command = command_parts[0].lower()
                
                if command in ["exit", "quit"]:
                    print("👋 Goodbye!")
                    break
                elif command == "help":
                    print("📚 Interactive Mode Help")
                    print("=" * 30)
                    print("Available commands:")
                    print("  /mode <n>  - Switch to specified mode")
                    print("    Available modes: research, plan, code, direct")
                    print("  /compact      - Manually compact conversation history")
                    print("  /help         - Show this help message")
                    print("  /exit, /quit  - Exit interactive mode")
                    print()
                    print("Query processing:")
                    print("  Type any text (not starting with /) to process as a query")
                    print(f"  Current mode: {current_mode}")
                    print()
                    print("Context management:")
                    current_tokens = get_current_token_count(conversation_history)
                    usage_percent = (current_tokens / MAX_CONTEXT_TOKENS) * 100
                    print(f"  Current context usage: ~{current_tokens}/{MAX_CONTEXT_TOKENS} tokens ({usage_percent:.1f}%)")
                    print()
                elif command == "mode":
                    if len(command_parts) < 2:
                        print("❌ Usage: /mode <n>")
                        print(f"Available modes: {', '.join(AVAILABLE_MODES)}")
                    else:
                        mode_name = command_parts[1].lower()
                        if switch_mode(current_mode_container, mode_name):
                            current_mode = current_mode_container[0]
                elif command == "compact":
                    if conversation_history:
                        current_tokens = get_current_token_count(conversation_history)
                        print(f"🗜️  Current context usage: ~{current_tokens}/{MAX_CONTEXT_TOKENS} tokens")
                        if compact_conversation(conversation_history, lambda p, m: generate_response(conversation_history, p, m)):
                            print("✅ Conversation history compacted successfully.")
                        else:
                            print("❌ Failed to compact conversation history.")
                    else:
                        print("ℹ️  No conversation history to compact.")
                else:
                    print(f"❌ Unknown command: /{command}")
                    print("Type /help for available commands")
            else:
                # Process as query
                process_query(conversation_history, model_loaded, current_mode, user_input)
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except EOFError:
            print("\n👋 Goodbye!")
            break 