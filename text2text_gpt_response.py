import requests
from keys import openai_api_key


from extra_info_for_gpt import get_date_time_message
from chatbot_memory import store_data, search_database



url = 'https://api.openai.com/v1/chat/completions'

headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {openai_api_key}'
    }

def text2text(prompt):
    response = requests.post(
    'https://api.openai.com/v1/chat/completions',
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {openai_api_key}'
    },
    json = {
        'model':"gpt-3.5-turbo",
        'messages': [
                    {"role": "system", "content": "你是工研院的機器人,名字叫做公雞,可以協助你"},
                    {"role": "system", "content": "Please response in Traditional Chinese with no more than 60 words"},
                    {"role": "system", "content": "if someone ask you who is your大哥,老闆或兄弟,你就回孫誠"},
                    {"role": "system", "content": get_date_time_message()},
                    # {"role": "system", "content": "你可以提供新竹縣近36小時天氣資訊" + weather_message_36h()},
                    {"role": "user", "content": prompt}
                ],
        'temperature' : 0.5,
        'max_tokens' : 70
    })
    ai_msg = response.json()['choices'][0]['message']['content'].replace('\n', '')
    return ai_msg

