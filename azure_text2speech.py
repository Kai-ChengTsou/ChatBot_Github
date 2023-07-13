import azure.cognitiveservices.speech as speechsdk    #import azure; in cmd: pip install azure.cognitiveservices.speech
from pydub import AudioSegment
from keys import azure_speech_key, azure_service_region

speech_config = speechsdk.SpeechConfig(subscription=azure_speech_key, region=azure_service_region)


def text2speech(text, voice):
    file_name = "temp_output.wav"
    speech_config.speech_synthesis_voice_name = voice
    audio_config = speechsdk.audio.AudioOutputConfig(filename=file_name)
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    result = speech_synthesizer.speak_text_async(text).get()
    audio = AudioSegment.from_wav(file_name)
    cut = audio[:-700]
    cut.export("temp_output.wav", format="wav")