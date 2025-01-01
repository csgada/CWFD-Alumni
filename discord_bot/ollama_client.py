import requests
import json

OLLAMA_API_URL = 'http://localhost:11434/api/generate'

headers = {
    'Content-Type': 'application/json'
}

def send_receive_process_message(data):
    response = requests.post(OLLAMA_API_URL, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        data = json.loads(response.text)
        return data['response']
    else:
        raise Exception(f'Failed to fetch response. Status code: {response.status_code}\nResponse: {response.text}')
    
def single_message(user_input):
    data = {
        'model': 'llama3.1:8b',
        'prompt': user_input,
        'stream': False,
    }
    return send_receive_process_message(data)
    
def message_with_history(user_input, history):
    data = {
        'model': 'llama3.1:8b',
        'prompt': user_input,
        'stream': False,
        'history': history,
    }
    return send_receive_process_message(data)

import asyncio
from ollama import AsyncClient

async def chat():
  message = {'role': 'user', 'content': 'Why is the sky blue?'}
  response = await AsyncClient().chat(model='llama3.1:8b', messages=[message])
  print(response)

asyncio.run(chat())