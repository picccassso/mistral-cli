#!/usr/bin/env python3
"""Research Engine Module - Web search and research functionality."""

from typing import Optional, List, Dict, Any
from .constants import RESEARCH_SYSTEM_PROMPT
from .config import get_search_api_key, get_search_engine_id
from .ollama_client import generate_response

# Import handling for optional dependencies
try:
    import requests
    from bs4 import BeautifulSoup
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False
    requests = None
    BeautifulSoup = None


def search_web(query: str, num_results: int = 5) -> Optional[list]:
    """Search the web using Google Custom Search API.
    
    Args:
        query: The search query.
        num_results: Number of results to return (max 10).
        
    Returns:
        List of search results or None if search fails.
    """
    if not HAS_REQUESTS:
        print("❌ Requests library not available. Please install requirements.")
        return None
    
    api_key = get_search_api_key()
    engine_id = get_search_engine_id()
    
    if not api_key or not engine_id:
        print("❌ Search API credentials not configured.")
        print("Please run 'mistral-cli --setup' to configure search API.")
        return None
    
    try:
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            "key": api_key,
            "cx": engine_id,
            "q": query,
            "num": min(num_results, 10)
        }
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            items = data.get("items", [])
            
            results = []
            for item in items:
                results.append({
                    "title": item.get("title", ""),
                    "link": item.get("link", ""),
                    "snippet": item.get("snippet", "")
                })
            
            return results
        else:
            print(f"❌ Search API error: {response.status_code}")
            if response.status_code == 403:
                print("This might be due to API key issues or quota exceeded.")
            return None
            
    except Exception as e:
        print(f"❌ Search failed: {e}")
        return None


def extract_text_from_url(url: str) -> Optional[str]:
    """Extract main text content from a webpage.
    
    Args:
        url: The URL to extract text from.
        
    Returns:
        Extracted text or None if extraction fails.
    """
    if not HAS_REQUESTS:
        print("❌ Requests library not available. Please install requirements.")
        return None
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style", "nav", "header", "footer"]):
                script.decompose()
            
            # Get text from main content areas
            main_content = soup.find('main') or soup.find('article') or soup.find('body')
            
            if main_content:
                text = main_content.get_text()
                # Clean up the text
                lines = (line.strip() for line in text.splitlines())
                chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                text = ' '.join(chunk for chunk in chunks if chunk)
                
                # Limit text length to avoid too much content
                if len(text) > 2000:
                    text = text[:2000] + "..."
                
                return text
        
        return None
        
    except Exception as e:
        print(f"⚠️  Failed to extract text from {url}: {e}")
        return None


def research_query(conversation_history: List[Dict[str, str]], query: str) -> Optional[str]:
    """Perform research by searching web and extracting content.
    
    Args:
        conversation_history: List of conversation exchanges for context.
        query: The research query.
        
    Returns:
        Generated response based on web search or None if failed.
    """
    print("🔍 Searching the web...")
    search_results = search_web(query)
    
    if not search_results:
        return None
    
    print(f"📄 Found {len(search_results)} results, extracting content...")
    
    context_parts = []
    
    for i, result in enumerate(search_results):
        url = result["link"]
        title = result["title"]
        snippet = result["snippet"]
        
        print(f"  Processing: {title}")
        
        # Extract text from the webpage
        extracted_text = extract_text_from_url(url)
        
        if extracted_text:
            context_parts.append(f"Source {i+1}: {title}\n{extracted_text}\n")
        else:
            # Fallback to snippet if text extraction fails
            context_parts.append(f"Source {i+1}: {title}\n{snippet}\n")
    
    if not context_parts:
        print("❌ No content could be extracted from search results.")
        return None
    
    # Combine all context
    context = "\n".join(context_parts)
    
    # Generate response using the research prompt
    prompt = RESEARCH_SYSTEM_PROMPT.format(context=context, question=query)
    
    print("🤖 Generating response based on search results...")
    return generate_response(conversation_history, prompt, "research") 