#!/usr/bin/env python3
"""Ollama Client Module - Ollama API integration and model management."""

from typing import Optional
from .constants import MODEL_NAME, OLLAMA_URL
from .token_manager import get_optimal_response_tokens
from .history_manager import format_history_for_prompt

# Import handling for optional dependencies
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False
    requests = None


def check_ollama_connection() -> bool:
    """Check if Ollama is running and accessible.
    
    Returns:
        True if Ollama is accessible, False otherwise.
    """
    if not HAS_REQUESTS:
        print("❌ Requests library not available. Please install requirements:")
        print("pip install -r requirements.txt")
        return False
    
    try:
        print("🔄 Checking Ollama connection...")
        response = requests.get(f"{OLLAMA_URL}/api/tags", timeout=5)
        
        if response.status_code == 200:
            available_models = response.json().get("models", [])
            model_names = [model["name"] for model in available_models]
            
            if MODEL_NAME in model_names or f"{MODEL_NAME}:latest" in model_names:
                print(f"✅ Ollama is running and {MODEL_NAME} model is available!")
                return True
            else:
                print(f"❌ Model '{MODEL_NAME}' not found in Ollama.")
                print(f"Available models: {', '.join(model_names)}")
                print(f"Please run: ollama pull {MODEL_NAME}")
                return False
        else:
            print(f"❌ Ollama API returned status code: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to Ollama. Please make sure:")
        print("1. Ollama is installed and running")
        print("2. Ollama is accessible at http://localhost:11434")
        print("3. Run 'ollama serve' if it's not running")
        return False
    except Exception as e:
        print(f"❌ Error checking Ollama connection: {e}")
        return False


def generate_response(conversation_history, prompt: str, mode: str = "direct") -> Optional[str]:
    """Generate a response using Ollama API.
    
    Args:
        conversation_history: List of conversation exchanges for context.
        prompt: The input prompt.
        mode: Current operating mode for token optimization.
        
    Returns:
        Generated response text or None if generation fails.
    """
    if not HAS_REQUESTS:
        print("❌ Requests library not available. Please install requirements.")
        return None
    
    try:
        # Include conversation history in the prompt
        history_context = format_history_for_prompt(conversation_history)
        full_prompt = history_context + prompt
        
        # Get optimal token limit for current mode
        optimal_tokens = get_optimal_response_tokens(mode)
        
        # Prepare the request payload with mode-optimized token limits
        payload = {
            "model": MODEL_NAME,
            "prompt": full_prompt,
            "stream": False,
            "options": {
                "temperature": 0.7,
                "top_p": 0.9,
                "num_predict": optimal_tokens
            }
        }
        
        # Make the request to Ollama
        response = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json=payload,
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            return result.get("response", "").strip()
        else:
            print(f"❌ Ollama API error: {response.status_code}")
            return None
            
    except requests.exceptions.Timeout:
        print("❌ Request timed out. The model might be taking too long to respond.")
        return None
    except Exception as e:
        print(f"❌ Failed to generate response: {e}")
        return None


def load_model_from_config() -> bool:
    """Check Ollama connection and model availability.
    
    Returns:
        True if Ollama is accessible and model is available, False otherwise.
    """
    print("✅ Using Ollama for model inference")
    
    # Check Ollama connection instead of loading from file
    return check_ollama_connection() 