from litellm import completion
import json 
import os

# gemini-2.5-pro-preview-06-05, not open
# gemini-2.5-flash-preview-05-20

## SET PROXY
os.environ["https_proxy"] = "http://host.orb.internal:7890"
os.environ["http_proxy"] = "http://host.orb.internal:7890"
os.environ["all_proxy"] = "socks5://host.orb.internal:7890"

file_path = '/Users/xu/ppio-claude-03.json'
os.environ["VERTEXAI_LOCATION"] =  'global' # 'europe-west1' # us-east5


with open(file_path, 'r') as file:
    vertex_credentials = json.load(file)

vertex_credentials_json = json.dumps(vertex_credentials)

tools = [{"googleSearch": {}}]

response = completion(
  model="vertex_ai/gemini-2.5-pro-preview-06-05",
  messages=[{ "content": "上海天气怎么样？","role": "user"}],
  vertex_credentials=vertex_credentials_json,
  tools=tools,
)

print(json.dumps(response.model_dump(), indent=2, ensure_ascii=False))