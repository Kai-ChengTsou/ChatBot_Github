import requests
from keys import openai_api_key

def speech2text(file_path):
    response = requests.post(
        'https://api.openai.com/v1/audio/transcriptions',
        headers = {
        'Authorization': f'Bearer {openai_api_key}'
        },
        data = {
            'model': 'whisper-1'
        },
        files = {
            'file': open(file_path, 'rb')
        })
    input_text = response.json()['text']
    return input_text