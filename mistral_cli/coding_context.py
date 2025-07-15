#!/usr/bin/env python3
"""Coding Context Module - Coding content analysis and context building."""

from typing import List, Dict, Any
from .constants import (
    CODING_KEYWORDS, CODE_PATTERNS, TEMPLATE_PATTERNS, INCREMENTAL_KEYWORDS
)


def is_coding_related(text: str) -> bool:
    """Check if text contains coding-related content.
    
    Args:
        text: Text to analyze.
        
    Returns:
        True if text appears to be coding-related, False otherwise.
    """
    # Use imported constants
    coding_keywords = CODING_KEYWORDS
    code_patterns = CODE_PATTERNS
    
    text_lower = text.lower()
    
    # Check for coding keywords
    for keyword in coding_keywords:
        if keyword in text_lower:
            return True
    
    # Check for code patterns
    for pattern in code_patterns:
        if pattern in text:
            return True
    
    return False


def extract_coding_context(text: str) -> str:
    """Extract important coding context from text.
    
    Args:
        text: Text to extract context from.
        
    Returns:
        Extracted coding context or original text if no specific context found.
    """
    lines = text.split('\n')
    important_lines = []
    
    for line in lines:
        line_strip = line.strip()
        
        # Skip empty lines and comments for context extraction
        if not line_strip or line_strip.startswith('#') or line_strip.startswith('//'):
            continue
        
        # Keep function definitions, class definitions, imports, and variable declarations
        if any(keyword in line_strip for keyword in ['def ', 'class ', 'import ', 'from ', 'function ', 'var ', 'let ', 'const ']):
            important_lines.append(line_strip)
        
        # Keep error messages and key statements
        elif any(keyword in line_strip.lower() for keyword in ['error', 'exception', 'failed', 'return', 'print']):
            important_lines.append(line_strip)
    
    # If we found specific context, return it; otherwise return original (truncated if too long)
    if important_lines:
        context = '\n'.join(important_lines)
        return context[:500] + '...' if len(context) > 500 else context
    else:
        return text[:300] + '...' if len(text) > 300 else text


def extract_code_definitions(text: str) -> dict:
    """Extract function definitions, classes, and variables from code text.
    
    Args:
        text: Code text to analyze.
        
    Returns:
        Dictionary with extracted definitions categorized by type.
    """
    definitions = {
        'functions': [],
        'classes': [],
        'variables': [],
        'imports': []
    }
    
    lines = text.split('\n')
    
    for line in lines:
        line_strip = line.strip()
        
        # Extract function definitions
        if line_strip.startswith('def ') or 'function ' in line_strip:
            # Extract function name
            if 'def ' in line_strip:
                func_match = line_strip.split('def ')[1].split('(')[0]
                definitions['functions'].append(func_match)
            elif 'function ' in line_strip:
                func_match = line_strip.split('function ')[1].split('(')[0]
                definitions['functions'].append(func_match)
        
        # Extract class definitions
        elif line_strip.startswith('class '):
            class_match = line_strip.split('class ')[1].split('(')[0].split(':')[0]
            definitions['classes'].append(class_match)
        
        # Extract imports
        elif line_strip.startswith('import ') or line_strip.startswith('from '):
            definitions['imports'].append(line_strip)
        
        # Extract variable declarations (basic patterns)
        elif any(pattern in line_strip for pattern in ['= ', 'var ', 'let ', 'const ']):
            # Simple variable extraction (first word before =)
            if '=' in line_strip:
                var_part = line_strip.split('=')[0].strip()
                # Remove type annotations and keywords
                var_part = var_part.replace('var ', '').replace('let ', '').replace('const ', '')
                if var_part and var_part.replace('_', '').isalnum():
                    definitions['variables'].append(var_part)
    
    return definitions


def get_coding_context_summary(conversation_history: List[Dict[str, str]]) -> str:
    """Get a summary of coding context from recent conversation history.
    
    Args:
        conversation_history: List of conversation exchanges.
        
    Returns:
        Compact summary of coding context for inclusion in prompts.
    """
    if not conversation_history:
        return ""
    
    all_definitions = {
        'functions': [],
        'classes': [],
        'variables': [],
        'imports': []
    }
    
    # Extract definitions from recent coding exchanges
    for item in conversation_history[-5:]:  # Last 5 exchanges
        if is_coding_related(item['assistant']):
            definitions = extract_code_definitions(item['assistant'])
            for key in all_definitions:
                all_definitions[key].extend(definitions[key])
    
    # Remove duplicates and create summary
    summary_parts = []
    
    if all_definitions['functions']:
        unique_functions = list(set(all_definitions['functions']))[:3]  # Keep top 3
        summary_parts.append(f"Functions: {', '.join(unique_functions)}")
    
    if all_definitions['classes']:
        unique_classes = list(set(all_definitions['classes']))[:2]  # Keep top 2
        summary_parts.append(f"Classes: {', '.join(unique_classes)}")
    
    if all_definitions['variables']:
        unique_variables = list(set(all_definitions['variables']))[:4]  # Keep top 4
        summary_parts.append(f"Variables: {', '.join(unique_variables)}")
    
    if all_definitions['imports']:
        unique_imports = list(set(all_definitions['imports']))[:3]  # Keep top 3
        summary_parts.append(f"Imports: {'; '.join(unique_imports)}")
    
    return " | ".join(summary_parts) if summary_parts else ""


def get_code_template_hint(query: str) -> str:
    """Get a concise template hint for common coding patterns.
    
    Args:
        query: User's coding request.
        
    Returns:
        Template hint if pattern is recognized, empty string otherwise.
    """
    query_lower = query.lower()
    
    # Use imported template patterns
    patterns = TEMPLATE_PATTERNS
    
    for pattern, hint in patterns.items():
        if pattern in query_lower:
            return f"Use {hint}. "
    
    return ""


def build_incremental_code_prompt(query: str, mode: str, conversation_history: List[Dict[str, str]]) -> str:
    """Build a context-aware prompt for incremental code building.
    
    Args:
        query: User's coding request.
        mode: Current mode (should be 'code').
        conversation_history: List of conversation exchanges.
        
    Returns:
        Enhanced prompt with coding context.
    """
    if mode != "code":
        return query
    
    # Get coding context summary
    context_summary = get_coding_context_summary(conversation_history)
    
    # Get template hint for common patterns
    template_hint = get_code_template_hint(query)
    
    # Build incremental prompt
    if context_summary:
        # Check if query is asking to build on previous code
        is_incremental = any(keyword in query.lower() for keyword in INCREMENTAL_KEYWORDS)
        
        if is_incremental:
            enhanced_prompt = f"Context: {context_summary}\n{template_hint}Request: {query}\nBuild on existing code:"
        else:
            enhanced_prompt = f"Context: {context_summary}\n{template_hint}Request: {query}"
    else:
        enhanced_prompt = f"{template_hint}Request: {query}"
    
    return enhanced_prompt 