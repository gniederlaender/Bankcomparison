import requests
import json

def test_erste_api():
    url = "https://shop.sparkasse.at/storeconsumerloan/rest/emilcalculators/198"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        # Disable SSL verification for testing
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()
        
        # Print the response
        print("Status Code:", response.status_code)
        print("\nResponse Body:")
        print(json.dumps(response.json(), indent=2))
        
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {str(e)}")
        if hasattr(e.response, 'text'):
            print("\nResponse text:")
            print(e.response.text)

if __name__ == "__main__":
    # Disable SSL verification warnings
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    test_erste_api() 