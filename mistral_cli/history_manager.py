#!/usr/bin/env python3
"""History Management Module - Conversation history operations and context management."""

from typing import List, Dict, Any, Optional
from .constants import (
    MAX_CONTEXT_TOKENS_FOR_PROMPT, MAX_CODING_EXCHANGES_TO_PRESERVE,
    MAX_GENERAL_EXCHANGES_TO_PRESERVE, COMPACT_SYSTEM_PROMPT
)
from .token_manager import estimate_tokens, get_current_token_count
from .coding_context import is_coding_related, extract_coding_context


def add_to_history(conversation_history: List[Dict[str, str]], user_query: str, response: str) -> None:
    """Add a user query and response to conversation history.
    
    Args:
        conversation_history: List of conversation exchanges to modify.
        user_query: The user's query.
        response: The model's response.
    """
    conversation_history.append({
        "user": user_query,
        "assistant": response
    })


def format_conversation_history(conversation_history: List[Dict[str, str]]) -> str:
    """Format conversation history as a string for summarization.
    
    Args:
        conversation_history: List of conversation exchanges.
        
    Returns:
        Formatted conversation history string.
    """
    formatted = []
    for item in conversation_history:
        formatted.append(f"User: {item['user']}")
        formatted.append(f"Assistant: {item['assistant']}")
    return "\n\n".join(formatted)


def prioritize_context_for_prompt(conversation_history: List[Dict[str, str]], max_tokens: int = 1000) -> str:
    """Prioritize and format context for prompt inclusion within token limit.
    
    Args:
        conversation_history: List of conversation exchanges.
        max_tokens: Maximum tokens to allocate for context.
        
    Returns:
        Formatted context string optimized for token usage.
    """
    if not conversation_history:
        return ""
    
    # Separate coding and non-coding exchanges
    coding_exchanges = []
    general_exchanges = []
    
    for item in conversation_history:
        if is_coding_related(item['user']) or is_coding_related(item['assistant']):
            coding_exchanges.append(item)
        else:
            general_exchanges.append(item)
    
    # Prioritize recent coding exchanges
    priority_context = []
    current_tokens = 0
    
    # Add recent coding exchanges first (highest priority)
    for item in coding_exchanges[-MAX_CODING_EXCHANGES_TO_PRESERVE:]:  # Last N coding exchanges
        user_query = item['user']
        assistant_context = extract_coding_context(item['assistant'])
        
        context_item = f"User: {user_query}\nAssistant: {assistant_context}"
        item_tokens = estimate_tokens(context_item)
        
        if current_tokens + item_tokens <= max_tokens:
            priority_context.append(context_item)
            current_tokens += item_tokens
        else:
            break
    
    # Add general context if space remains
    for item in general_exchanges[-MAX_GENERAL_EXCHANGES_TO_PRESERVE:]:  # Last N general exchanges
        user_brief = item['user'][:80] + '...' if len(item['user']) > 80 else item['user']
        assistant_brief = item['assistant'][:80] + '...' if len(item['assistant']) > 80 else item['assistant']
        
        context_item = f"User: {user_brief}\nAssistant: {assistant_brief}"
        item_tokens = estimate_tokens(context_item)
        
        if current_tokens + item_tokens <= max_tokens:
            priority_context.append(context_item)
            current_tokens += item_tokens
        else:
            break
    
    if priority_context:
        history_text = "\n\n".join(priority_context)
        return f"Previous conversation:\n{history_text}\n\nCurrent query:\n"
    else:
        return ""


def format_history_for_prompt(conversation_history: List[Dict[str, str]]) -> str:
    """Format conversation history for inclusion in prompts.
    
    Args:
        conversation_history: List of conversation exchanges.
        
    Returns:
        Formatted conversation history string for prompt inclusion.
    """
    # Use prioritized context formatting for better token efficiency
    return prioritize_context_for_prompt(conversation_history, max_tokens=MAX_CONTEXT_TOKENS_FOR_PROMPT)


def compact_conversation(conversation_history: List[Dict[str, str]], generate_response_func) -> bool:
    """Compact the conversation history by summarizing it with coding context preservation.
    
    Args:
        conversation_history: List of conversation exchanges to modify.
        generate_response_func: Function to call for response generation.
        
    Returns:
        True if compaction was successful, False otherwise.
    """
    if not conversation_history:
        return True
    
    print("🗜️  Context window approaching limit. Compacting conversation history...")
    
    # Separate coding and non-coding content
    coding_context = []
    general_context = []
    
    for item in conversation_history:
        if is_coding_related(item['user']) or is_coding_related(item['assistant']):
            # Preserve important coding context
            user_query = item['user']
            assistant_response = extract_coding_context(item['assistant'])
            coding_context.append(f"User: {user_query}\nAssistant: {assistant_response}")
        else:
            # Summarize general content more aggressively
            user_brief = item['user'][:50] + '...' if len(item['user']) > 50 else item['user']
            assistant_brief = item['assistant'][:50] + '...' if len(item['assistant']) > 50 else item['assistant']
            general_context.append(f"User: {user_brief}\nAssistant: {assistant_brief}")
    
    # Create context-aware summary
    preserved_coding = '\n\n'.join(coding_context[-MAX_CODING_EXCHANGES_TO_PRESERVE:])  # Keep last N coding exchanges
    general_summary = ' | '.join(general_context[-MAX_GENERAL_EXCHANGES_TO_PRESERVE:])   # Brief summary of general content
    
    if preserved_coding and general_summary:
        compact_summary = f"General context: {general_summary}\n\nCoding context:\n{preserved_coding}"
    elif preserved_coding:
        compact_summary = f"Coding context:\n{preserved_coding}"
    elif general_summary:
        compact_summary = f"General context: {general_summary}"
    else:
        # Fallback to original summarization if no content
        history_text = format_conversation_history(conversation_history)
        prompt = COMPACT_SYSTEM_PROMPT.format(history=history_text)
        summary = generate_response_func(prompt, "direct")
        compact_summary = summary if summary else "Previous conversation context preserved."
    
    if compact_summary:
        # Replace conversation history with context-aware summary
        conversation_history.clear()
        conversation_history.append({
            "user": "Previous conversation summary",
            "assistant": compact_summary
        })
        
        new_count = get_current_token_count(conversation_history)
        print(f"✅ Conversation compacted. Token count reduced to ~{new_count}")
        return True
    else:
        print("❌ Failed to compact conversation. Clearing history instead.")
        conversation_history.clear()
        return False 