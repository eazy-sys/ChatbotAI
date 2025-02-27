from openai import AzureOpenAI

# Set your API key and endpoint
api_key = "BNF10GhIkIM5G3Zf1pkqF4OVy3XNh5ihALbxHNzZjGYPlGFxW5gKJQQJ99BBACHYHv6XJ3w3AAAAACOGzp5z"
endpoint = "https://junio-m7nldf0u-eastus2.cognitiveservices.azure.com/"  # Simplified to base URL

deployment_name = "gpt-4"

# Function to test the API key
def test_openai_api():
    try:
        client = AzureOpenAI(
            api_key=api_key,
            api_version="2023-05-15",
            azure_endpoint=endpoint
        )

        response = client.chat.completions.create(
            model=deployment_name,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Hello, how are you?"}
            ]
        )
        print("API Key is working! Response:", response.choices[0].message.content)
    except Exception as e:
        print("Error:", e)

# Run the test
test_openai_api()