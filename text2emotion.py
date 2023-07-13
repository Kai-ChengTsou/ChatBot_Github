import requests, uuid, json
from pysentimiento import create_analyzer
from keys import ms_translator_key, ms_translator_location, fullface_core


def translate(text):
    request = requests.post(
        "https://api.cognitive.microsofttranslator.com/translate", 
        params = {
            'api-version': '3.0',
            'from': 'zh-Hans',
            'to': 'en'
        }, 
        headers = {
            'Ocp-Apim-Subscription-Key': ms_translator_key,
            # location required if you're using a multi-service or regional (not global) resource.
            'Ocp-Apim-Subscription-Region': ms_translator_location,
            'Content-type': 'application/json',
            'X-ClientTraceId': str(uuid.uuid4())
        }, 
        json=[{'text': text}])
    response = request.json()
    return response[0]['translations'][0]['text']

def generate_emotion(text):
    emotion_analyzer = create_analyzer(task="emotion", lang="en")
    emo = emotion_analyzer.predict(translate(text))
    payload = {
        "a2f_instance": fullface_core,
        "emotions": {
            "neutral": 0,
            "amazement": emo.probas['surprise'],
            "anger": emo.probas['anger'],
            "cheekiness": 0,
            "disgust": emo.probas['disgust'],
            "fear": emo.probas['fear'],
            "grief": 0,
            "joy": emo.probas['joy'],
            "outofbreath": 0,
            "pain": 0,
            "sadness": emo.probas['sadness'],
        }
    }
    return payload