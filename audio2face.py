import requests
import soundfile

from keys import server, usd_scene, a2f_avatar_instance, a2f_url
from text2emotion import generate_emotion
from audio2face_streaming_utils import push_audio_track

def A2F():
    # global a2f_instance
    # payload = {
    #     "file_name": usd_scene
    # }

    # usd = requests.post(f'{server}/A2F/USD/Load', json=payload)

    # print(f"USD scene: {usd.json()['message']}")

    data = {"file_name": usd_scene}
    response = (requests.get(f'{server}/A2F/USD/Load', json=data)).json
    
    print("Loaded!")

    data = {"a2f_instance": a2f_avatar_instance}
    requests.post(f'{server}/A2F/POST/NumKeys', json=data).json()

    a2f_instance = requests.get(f'{server}' + "/A2F/GetInstances").json
    # a2f_instance_d = a2f_instance['result']['fullface_instances'][0]
    print(f'A2F Instance: {a2f_instance}')
    return a2f_instance

def push_emotion(text):
    requests.post(f'{server}/A2F/A2E/SetEmotionByName', json=generate_emotion(text))
    # print(f'A2E parameters: {a2e.json()["message"]}')

def push_audio_file(converted_output_filename):
    data, samplerate = soundfile.read(converted_output_filename, dtype="float32")
    push_audio_track(a2f_url, data, samplerate, a2f_avatar_instance)