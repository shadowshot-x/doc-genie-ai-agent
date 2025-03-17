from ollama import chat
from ollama import ChatResponse

response: ChatResponse = chat(model='gemma3:1b', messages=[
  {
    'role': 'user',
    'content': '''
Give 5 examples of simple AI Agents to build for learning
''',
  },
])
print(response['message']['content'])
# or access fields directly from the response object