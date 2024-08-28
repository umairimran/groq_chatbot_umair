from speech_to_speech_functions import *
try:
    frames = []
    while True:
        # Read audio data
        audio_data = stream.read(FRAME_SIZE)
        audio_data = np.frombuffer(audio_data, dtype=np.int16)
        # Check if the audio data contains speech
        is_speech = vad.is_speech(audio_data.tobytes(), SAMPLE_RATE)
        if is_speech:
            print("Speech detected")
            frames.append(audio_data.tobytes())
        else:
            print("Silence detected")
            if frames:
                # Save the collected frames to the file
                wav_file.writeframes(b''.join(frames))
                frames = []
                wav_file.close()
                # Extract speech segments from the recorded file
                extract_speech_segments(temp_wav_file)
                # Re-open WAV file for new recording
                wav_file = wave.open(temp_wav_file, "wb")
                wav_file.setnchannels(1)
                wav_file.setsampwidth(pyaudio.PyAudio().get_sample_size(pyaudio.paInt16))
                wav_file.setframerate(SAMPLE_RATE)
                check_file_and_process("combined_speechh.mp3")
except KeyboardInterrupt:
    print("Stopping...")
finally:
    # Save any remaining frames to the file
    if frames:
        wav_file.writeframes(b''.join(frames))
    stream.stop_stream()
    stream.close()
    p.terminate()
    wav_file.close()

