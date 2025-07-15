#!/usr/bin/env python3
"""Query Processor Module - Query processing and mode handling."""

from typing import List, Dict, Any
from .constants import (
    AVAILABLE_MODES, PLAN_SYSTEM_PROMPT, CODE_SYSTEM_PROMPT, 
    CODE_SYSTEM_PROMPT_NO_COMMENTS, MAX_CONTEXT_TOKENS
)
from .token_manager import should_compact, get_current_token_count
from .coding_context import is_coding_related, build_incremental_code_prompt
from .history_manager import add_to_history, compact_conversation
from .ollama_client import generate_response
from .research_engine import research_query


def validate_mode(mode: str) -> bool:
    """Validate if the given mode is supported.
    
    Args:
        mode: Mode name to validate.
        
    Returns:
        True if mode is valid, False otherwise.
    """
    return mode in AVAILABLE_MODES


def switch_mode(current_mode_container: List[str], mode: str) -> bool:
    """Switch to the specified mode.
    
    Args:
        current_mode_container: List containing current mode (for mutability).
        mode: Mode name to switch to.
        
    Returns:
        True if mode switch successful, False otherwise.
    """
    if not validate_mode(mode):
        print(f"❌ Invalid mode: '{mode}'")
        print(f"Available modes: {', '.join(AVAILABLE_MODES)}")
        return False
    
    current_mode_container[0] = mode
    print(f"✅ Mode switched to '{mode}'")
    return True


def process_query(conversation_history: List[Dict[str, str]], model_loaded: bool, 
                 current_mode: str, query: str, mode: str = None, 
                 no_comments: bool = False) -> None:
    """Process a query in the specified mode.
    
    Args:
        conversation_history: List of conversation exchanges.
        model_loaded: Whether the model is loaded and ready.
        current_mode: Current operating mode.
        query: The query text to process.
        mode: The mode to use (if None, uses current_mode).
        no_comments: Whether to generate code without comments (code mode only).
    """
    if mode is None:
        mode = current_mode
    
    print(f"Processing query in '{mode}' mode...")
    print(f"Query: {query}")
    print()
    
    # Check if model is loaded
    if not model_loaded:
        print("❌ Model not loaded. Please ensure the model was loaded successfully.")
        return
    
    # Check if conversation should be compacted before processing
    if should_compact(conversation_history, is_coding_related):
        compact_conversation(conversation_history, lambda p, m: generate_response(conversation_history, p, m))
    
    response = None
    
    # Mode-specific processing
    if mode == "direct":
        print("🔄 Direct mode: Generating response...")
        response = generate_response(conversation_history, query, mode)
        if response:
            print(response)
        
    elif mode == "plan":
        print("📋 Plan mode: Generating step-by-step plan...")
        prompt = PLAN_SYSTEM_PROMPT + query
        response = generate_response(conversation_history, prompt, mode)
        if response:
            print(response)
            
    elif mode == "code":
        print("💻 Code mode: Generating code...")
        
        # Build context-aware prompt for incremental code building
        enhanced_query = build_incremental_code_prompt(query, mode, conversation_history)
        
        if no_comments:
            print("(without comments)")
            prompt = CODE_SYSTEM_PROMPT_NO_COMMENTS + enhanced_query
        else:
            print("(with inline comments)")
            prompt = CODE_SYSTEM_PROMPT + enhanced_query
        
        response = generate_response(conversation_history, prompt, mode)
        if response:
            print(response)
            
    elif mode == "research":
        print("🔍 Research mode: Searching web and generating response...")
        response = research_query(conversation_history, query)
        if response:
            print(response)
        else:
            print("❌ Research mode failed. Please check your search API configuration.")
        
    else:
        print(f"❌ Unknown mode: {mode}")
        return
    
    # Add to conversation history if response was generated
    if response:
        add_to_history(conversation_history, query, response)
        
        # Show current token usage
        current_tokens = get_current_token_count(conversation_history)
        usage_percent = (current_tokens / MAX_CONTEXT_TOKENS) * 100
        print(f"\n📊 Context usage: ~{current_tokens}/{MAX_CONTEXT_TOKENS} tokens ({usage_percent:.1f}%)") 