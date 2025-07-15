#!/usr/bin/env python3
"""Configuration management module for Mistral CLI Wrapper."""

import json
import os
from pathlib import Path
from typing import Optional, Dict, Any


CONFIG_FILENAME = ".mistral_cli_config"
CONFIG_PATH = Path.home() / CONFIG_FILENAME


def read_config() -> Optional[Dict[str, Any]]:
    """Read configuration from ~/.mistral_cli_config file.
    
    Returns:
        Dict containing configuration data, or None if file doesn't exist.
    """
    if not CONFIG_PATH.exists():
        return None
    
    try:
        with open(CONFIG_PATH, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error reading config file: {e}")
        return None


def write_config(config_data: Dict[str, Any]) -> bool:
    """Write configuration to ~/.mistral_cli_config file.
    
    Args:
        config_data: Dictionary containing configuration data.
        
    Returns:
        True if successful, False otherwise.
    """
    try:
        with open(CONFIG_PATH, 'w') as f:
            json.dump(config_data, f, indent=2)
        return True
    except IOError as e:
        print(f"Error writing config file: {e}")
        return False


def validate_model_path(model_path: str) -> bool:
    """Validate that the provided model path is valid.
    
    Args:
        model_path: Path to the model file.
        
    Returns:
        True if path is valid, False otherwise.
    """
    if not model_path:
        return False
    
    path = Path(model_path)
    
    # Must be absolute path
    if not path.is_absolute():
        print("Error: Model path must be an absolute path.")
        return False
    
    # Path must exist
    if not path.exists():
        print(f"Error: Path does not exist: {model_path}")
        return False
    
    # Must point to a file, not a directory
    if not path.is_file():
        print(f"Error: Path must point to a file, not a directory: {model_path}")
        return False
    
    return True


def get_model_path() -> Optional[str]:
    """Get the model path from configuration.
    
    Returns:
        Model path if valid, None otherwise.
    """
    config = read_config()
    if not config:
        return None
    
    model_path = config.get("model_path")
    if not model_path:
        return None
    
    # Validate the stored path is still valid
    if not validate_model_path(model_path):
        return None
    
    return model_path


def save_model_path(model_path: str) -> bool:
    """Save model path to configuration after validation.
    
    Args:
        model_path: Path to the model file.
        
    Returns:
        True if successful, False otherwise.
    """
    if not validate_model_path(model_path):
        return False
    
    config_data = {"model_path": model_path}
    return write_config(config_data)


def get_search_api_key() -> Optional[str]:
    """Get the search API key from configuration.
    
    Returns:
        Search API key if found, None otherwise.
    """
    config = read_config()
    if not config:
        return None
    
    return config.get("search_api_key")


def save_search_api_key(api_key: str) -> bool:
    """Save search API key to configuration.
    
    Args:
        api_key: The search API key to save.
        
    Returns:
        True if successful, False otherwise.
    """
    if not api_key or not api_key.strip():
        return False
    
    # Read existing config or create new one
    config = read_config() or {}
    config["search_api_key"] = api_key.strip()
    
    return write_config(config)


def get_search_engine_id() -> Optional[str]:
    """Get the search engine ID from configuration.
    
    Returns:
        Search engine ID if found, None otherwise.
    """
    config = read_config()
    if not config:
        return None
    
    return config.get("search_engine_id")


def save_search_engine_id(engine_id: str) -> bool:
    """Save search engine ID to configuration.
    
    Args:
        engine_id: The search engine ID to save.
        
    Returns:
        True if successful, False otherwise.
    """
    if not engine_id or not engine_id.strip():
        return False
    
    # Read existing config or create new one
    config = read_config() or {}
    config["search_engine_id"] = engine_id.strip()
    
    return write_config(config)