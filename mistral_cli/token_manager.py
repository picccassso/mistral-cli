#!/usr/bin/env python3
"""Token Management Module - Token estimation and context window management."""

from typing import List, Dict, Any
from .constants import (
    COMPACT_THRESHOLD, CODING_SESSION_THRESHOLD, MIXED_SESSION_THRESHOLD,
    MAX_CONTEXT_TOKENS, MODE_TOKEN_LIMITS
)


def estimate_tokens(text: str) -> int:
    """Estimate the number of tokens in a text string with improved accuracy.
    
    Args:
        text: The text to estimate tokens for.
        
    Returns:
        Estimated number of tokens.
    """
    if not text:
        return 0
    
    # More accurate token estimation based on common patterns
    # Split by whitespace first
    words = text.split()
    
    # Count tokens more accurately
    token_count = 0
    for word in words:
        # Common punctuation and symbols count as separate tokens
        punctuation_count = sum(1 for char in word if char in '.,!?;:()[]{}"\'-=+*/<>@#$%^&|\\')
        
        # Word length affects token count
        word_clean = ''.join(char for char in word if char.isalnum())
        
        if len(word_clean) <= 4:
            token_count += 1  # Short words = 1 token
        elif len(word_clean) <= 8:
            token_count += 2  # Medium words = 2 tokens
        else:
            token_count += 3  # Long words = 3 tokens
        
        # Add punctuation tokens
        token_count += punctuation_count
    
    # Add some tokens for whitespace and formatting
    token_count += len(text.split('\n'))  # Newlines
    
    # Minimum 1 token for non-empty text
    return max(1, token_count)


def get_current_token_count(conversation_history: List[Dict[str, str]]) -> int:
    """Get the current token count for the conversation history.
    
    Args:
        conversation_history: List of conversation exchanges.
        
    Returns:
        Estimated number of tokens in the conversation history.
    """
    total = 0
    for item in conversation_history:
        total += estimate_tokens(item["user"])
        total += estimate_tokens(item["assistant"])
    return total


def get_dynamic_compact_threshold(conversation_history: List[Dict[str, str]], is_coding_related_func) -> float:
    """Get dynamic compaction threshold based on conversation context.
    
    Args:
        conversation_history: List of conversation exchanges.
        is_coding_related_func: Function to check if content is coding-related.
        
    Returns:
        Threshold percentage (0.0 to 1.0) for compaction.
    """
    if not conversation_history:
        return COMPACT_THRESHOLD
    
    # Count recent coding exchanges
    recent_coding_exchanges = 0
    for item in conversation_history[-3:]:  # Last 3 exchanges
        if is_coding_related_func(item['user']) or is_coding_related_func(item['assistant']):
            recent_coding_exchanges += 1
    
    # Lower threshold for coding-heavy conversations to preserve more context
    if recent_coding_exchanges >= 2:
        return CODING_SESSION_THRESHOLD  # Compact at 85% for coding sessions
    elif recent_coding_exchanges >= 1:
        return MIXED_SESSION_THRESHOLD   # Compact at 92% for mixed sessions
    else:
        return COMPACT_THRESHOLD  # Default 99% for general conversations


def should_compact(conversation_history: List[Dict[str, str]], is_coding_related_func) -> bool:
    """Check if conversation should be compacted based on token usage.
    
    Args:
        conversation_history: List of conversation exchanges.
        is_coding_related_func: Function to check if content is coding-related.
        
    Returns:
        True if compaction should be triggered, False otherwise.
    """
    current_tokens = get_current_token_count(conversation_history)
    dynamic_threshold = get_dynamic_compact_threshold(conversation_history, is_coding_related_func)
    threshold = int(MAX_CONTEXT_TOKENS * dynamic_threshold)
    return current_tokens >= threshold


def get_optimal_response_tokens(mode: str) -> int:
    """Get optimal token limit based on current mode.
    
    Args:
        mode: Current operating mode.
        
    Returns:
        Optimal token limit for the mode.
    """
    # Use imported mode-specific token limits
    return MODE_TOKEN_LIMITS.get(mode, 320) 