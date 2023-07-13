import threading, sys
from pydub import AudioSegment

import pythonosc
from pythonosc import udp_client
from pythonosc.udp_client import SimpleUDPClient

from record_audio_from_user import record_audio
from speech2text_whisper import speech2text
from text2text_gpt_response import text2text 
from azure_text2speech import text2speech
from audio2face import A2F, push_emotion, push_audio_file
from run_unreal import open_unreal_exe

from keys import female_voice, female_unreal_exe, male_voice, male_unreal_exe


def cut_response(text):
    global left
    
    index_list = [text.rfind('。'), text.rfind(';'), text.rfind('!'), text.rfind('?'), text.rfind('，')]
    out_index = max(index_list)
    
    out = text[:out_index:]
    out_text = left + out
    
    left = text[out_index+1::]
    return out_text

def get_text():
    global run
    global text_list
    global messages
    global count
    global left
    while run:
        ai_msg = text2text(messages)

        messages = f'{messages}\n{ai_msg}\n\n'  # 合併 AI 回應的話
        messages = messages.replace('END', 'TEMP_HOLD',1)
        count +=1
        if (messages.rfind('END') != -1):
            text = left+ai_msg
            text = text.replace('END','')
            text_list.append(text)
            left =''
            run = False
        else:
            msg = '繼續'
            messages = messages.replace('TEMP_HOLD', 'END',1)
            messages = f'{messages}{msg}\n'
            text = cut_response(ai_msg)
            text_list.append(text)
        print(text)

def play_audio():
    global run_count
    global count
    global text_list
    global run
    run_count = 0
    while (run or run_count!=count):
        try:
            text = text_list[run_count]
            text2speech(text, voice_name)
            print("converted")

            converted_output_filename = 'processed'+ str(run_count) +'.wav'
            sound = AudioSegment.from_file("temp_output.wav", format="wav")
            sound.export(converted_output_filename, format="wav")

            run_count+=1

        except IndexError:
            pass

def push_audio():
    play_count = 0
    global count
    global run
    global run_count
    global text_list
    while (run or play_count!=count):
        try:
            if (play_count<run_count):
                converted_output_filename = 'processed'+ str(play_count) +'.wav'
                text = text_list[play_count]

                # push_emotion(text)
                
                client.send_message("/FaceIdle", float(1))
                
                push_audio_file(converted_output_filename)
                client.send_message("/FaceIdle", float(0))
                play_count+=1
            else:
                pass
        except IndexError:
            pass

def please_wait():
    global wait_response
    wait_response = False  
    while wait_response:
        client.send_message("/FaceIdle", float(1))
        push_audio_file("./please_wait.wav")
        client.send_message("/FaceIdle", float(0))
        wait_response = False
  
#global variables
messages = ''
count = 0
run_count = 0
left = ''
run = True
text_list = []
emo_list = []
voice_name=''


a2f_instance = A2F()
client = udp_client.SimpleUDPClient('127.0.0.1', 5008)
client.send_message("/FaceIdle", float(0))


def main():
    global voice_name
    if len(sys.argv) < 2:
        print("Format: python testing.py m/f")
        return
    

    voice = sys.argv[1]
    
    if voice == 'm':
        voice_name = male_voice
        exe_path = male_unreal_exe

    elif voice == 'f':
        voice_name = female_voice
        exe_path = female_unreal_exe


    else:
        print("Format: python testing.py m/f")
        return

    print("gender chosen")

    open_unreal_exe(exe_path)



    while True:
        input_file = "recorded_audio.wav"
        record_audio(input_file)

        input_text = speech2text(input_file)

        global messages
        messages = ''
        default = ' (請注意: 如果你回答完畢這個問題，請你在本次回答的句子的最後加上"END")'
        messages = input_text + default
        print(input_text)

        global text_list
        text_list = []

        global run
        run = True

        global count
        count = 0


        if "結束" in messages:
            client.send_message("/FaceIdle", float(2))
            break

        thread1 = threading.Thread(target=get_text)
        thread2 = threading.Thread(target=play_audio)
        thread3 = threading.Thread(target=push_audio)

        # Start the threads
        thread1.start()
        thread2.start()
        thread3.start()

        thread1.join()
        thread2.join()
        thread3.join()


        

        key = input("Press q and Enter to quit or any other key to continue...")
        if key.lower() == 'q':
            client.send_message("/FaceIdle", float(2))
            break
        
if __name__ == "__main__":
    main()