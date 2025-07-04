from litellm import completion
import os
import json

## set ENV variables
os.environ["OPENAI_API_KEY"] = "sk-v876bBvpGZIoMWKkq570Gs5CPqtkr5LZA3ax5J8fCQejQD8v"
os.environ["OPENAI_API_BASE"] = "https://ai.burncloud.com/v1"

response = completion(
  model="openai/gpt-4o",
  messages=[{ "content": "Hello, how are you?","role": "user"}]
)

print(json.dumps(response.model_dump(), indent=2))