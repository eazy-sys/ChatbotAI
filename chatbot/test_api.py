import requests
import json

def test_chat(message):
    url = "http://74.177.171.22/chat"  # Using the LoadBalancer external IP
    payload = {"message": message}
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        # Print with better formatting
        print(f"\n{'='*80}\nQuery: {message}\n{'-'*80}")
        response_text = response.json()['response']
        print(f"Response:\n{'-'*80}\n{response_text}\n{'='*80}\n")
        
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON response: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    # Test queries
    test_queries = [
        "What is Azure OpenAI?",
        "Can you explain how containerization works?",
        "What are the benefits of using FastAPI?"
    ]
    
    for query in test_queries:
        test_chat(query) 