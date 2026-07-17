import requests

print("Attempting to connect to Hugging Face...")
try:
    # Explicitly bypassing any system proxies
    proxies = {
      "http": None,
      "https": None,
    }
    response = requests.get("https://api-inference.huggingface.co", proxies=proxies, timeout=10)
    print(f"Success! Status Code: {response.status_code}")
except Exception as e:
    print(f"Failed: {e}")