import threading
import pyaudio
import wave

def record_audio(output_file):
    # Set the sample rate and channels
    sample_rate = 44100
    channels = 2

    # Initialize PyAudio
    audio = pyaudio.PyAudio()

    # Set the audio stream parameters
    stream = audio.open(format=pyaudio.paInt16,
                        channels=channels,
                        rate=sample_rate,
                        input=True,
                        frames_per_buffer=1024)

    # Wait for user to start recording
    input("Press Enter to start recording...")

    # Start recording in a separate thread
    print("Recording audio... Press Enter to stop.")
    frames = []
    stop_event = threading.Event()
    recording_thread = threading.Thread(target=record_frames, args=(stream, frames, stop_event))
    recording_thread.start()

    # Wait for user to stop recording
    input()

    # Stop recording
    stop_event.set()
    recording_thread.join()

    # Stop the audio stream and terminate PyAudio
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Save the recorded audio to a WAV file
    save_audio(output_file, frames, sample_rate, channels)

    print(f"Audio saved to {output_file}")


def record_frames(stream, frames, stop_event):
    while not stop_event.is_set():
        data = stream.read(1024)
        frames.append(data)


def save_audio(output_file, frames, sample_rate, channels):
    wave_file = wave.open(output_file, 'wb')
    wave_file.setnchannels(channels)
    wave_file.setsampwidth(pyaudio.PyAudio().get_sample_size(pyaudio.paInt16))
    wave_file.setframerate(sample_rate)
    wave_file.writeframes(b''.join(frames))
    wave_file.close()