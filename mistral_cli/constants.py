#!/usr/bin/env python3
"""Constants and system prompts for the Mistral CLI."""

# Available modes
AVAILABLE_MODES = ["direct", "research", "plan", "code"]

# Global model configuration
MODEL_NAME = "mistral"
OLLAMA_URL = "http://localhost:11434"

# Context window management
MAX_CONTEXT_TOKENS = 4096  # Conservative estimate for Mistral 7B
COMPACT_THRESHOLD = 0.99  # Trigger compact mode at 99% usage

# System prompts for different modes (optimized for token efficiency)
PLAN_SYSTEM_PROMPT = """Create a numbered step-by-step plan. Be specific and practical.

Request: """

CODE_SYSTEM_PROMPT = """Generate code only. Include inline comments for complex logic.

Request: """

CODE_SYSTEM_PROMPT_NO_COMMENTS = """Generate code only. No comments.

Request: """

RESEARCH_SYSTEM_PROMPT = """Answer based on the provided context. If insufficient information, say so.

Context: {context}

Question: {question}

Answer:"""

COMPACT_SYSTEM_PROMPT = """Summarize conversation: key topics, facts, and user's goal.

History: {history}

Summary:"""

# Mode-specific token limits optimized for 4k context
MODE_TOKEN_LIMITS = {
    "code": 256,      # Code should be concise
    "plan": 384,      # Plans need more space for steps
    "research": 320,  # Research responses need detail
    "direct": 320     # General conversations
}

# Coding keywords for content detection
CODING_KEYWORDS = [
    'function', 'def', 'class', 'import', 'from', 'return', 'if', 'else', 'elif',
    'for', 'while', 'try', 'except', 'with', 'lambda', 'var', 'let', 'const',
    'public', 'private', 'static', 'void', 'int', 'string', 'bool', 'float',
    'array', 'list', 'dict', 'object', 'null', 'undefined', 'true', 'false',
    'print', 'console.log', 'System.out', 'cout', 'printf', 'echo',
    'git', 'npm', 'pip', 'cargo', 'mvn', 'gradle', 'make', 'cmake',
    'bug', 'error', 'exception', 'debug', 'test', 'unit test', 'api',
    'database', 'sql', 'json', 'xml', 'html', 'css', 'javascript', 'python',
    'java', 'c++', 'rust', 'go', 'ruby', 'php', 'typescript', 'react', 'vue'
]

# Code patterns for content detection
CODE_PATTERNS = [
    '()', '{}', '[]', ';', '->', '=>', '==', '!=', '<=', '>=', '&&', '||',
    '++', '--', '+=', '-=', '*=', '/=', '.', '::', ':::', '</', '/>', '<!--'
]

# Template patterns for common coding frameworks
TEMPLATE_PATTERNS = {
    'flask': 'Flask app template',
    'fastapi': 'FastAPI app template',
    'django': 'Django view template',
    'react': 'React component template',
    'vue': 'Vue component template',
    'express': 'Express.js server template',
    'class': 'Class definition template',
    'function': 'Function definition template',
    'api': 'API endpoint template',
    'crud': 'CRUD operations template',
    'database': 'Database connection template',
    'authentication': 'Auth middleware template',
    'test': 'Unit test template',
    'error handling': 'Error handling template',
    'async': 'Async function template'
}

# Incremental building trigger words
INCREMENTAL_KEYWORDS = [
    'add', 'modify', 'update', 'extend', 'improve', 'fix', 'change', 'enhance'
]

# Dynamic compaction thresholds
CODING_SESSION_THRESHOLD = 0.85  # Compact at 85% for coding sessions
MIXED_SESSION_THRESHOLD = 0.92   # Compact at 92% for mixed sessions

# Context prioritization settings
MAX_CONTEXT_TOKENS_FOR_PROMPT = 800
MAX_CODING_EXCHANGES_TO_PRESERVE = 3
MAX_GENERAL_EXCHANGES_TO_PRESERVE = 2