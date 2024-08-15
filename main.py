import streamlit as st
from groq import Groq
from audio import record_audio, play_audio
from text_speech import *
import time
from jarvis import *

api = "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"

def response(history):
    client = Groq(api_key=api)
    chat_completion = client.chat.completions.create(
        messages=history,
        model="llama3-70b-8192"
    )
    return chat_completion.choices[0].message.content

def format_history(history):
    messages = []
    for message in history:
        messages.append({"role": "user", "content": message["human"]})
        messages.append({"role": "assistant", "content": message["AI"]})
    return messages

def main():
    st.set_page_config(page_title="🦙💬 Llama 3 Chatbot", page_icon=":speech_balloon:", layout="wide")

    st.markdown("""
        <style>
        .css-1d391kg { 
            background-color: #1e1e1e; /* Dark background */
            color: #f5f5f5; /* Light text color */
        }
        .css-ffhzg2 { 
            background-color: #007acc; /* Dark blue for user messages */
            color: white; 
            padding: 10px; 
            border-radius: 10px;
            margin-bottom: 10px;
        }
        .css-1l6a57s { 
            background-color: #333; /* Dark gray for AI messages */
            color: #f5f5f5; /* Light text color */
            padding: 10px; 
            border-radius: 10px;
            margin-bottom: 10px;
        }
        .css-16m1qwe { 
            padding: 10px; 
            border-radius: 10px;
            background-color: #2e2e2e; /* Slightly lighter dark background */
            color: #f5f5f5; /* Light text color */
        }
        </style>
        """, unsafe_allow_html=True)

    st.write('This chatbot is created using the open-source Llama 3 LLM model from Meta.')

    st.sidebar.title("Chatbot Customization")
    st.sidebar.write("Customize your chatbot experience.")
    actor=st.sidebar.selectbox("Select a model", ["aura-asteria-en", "aura-orpheus-en", "aura-angus-en", "aura-arcas-en", "aura-athena-en", "aura-helios-en", "aura-hera-en", "aura-luna-en", "aura-orion-en", "aura-perseus-en",
                                            "aura-stella-en","aura-zeus-e"
                                            ])

    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    # Button to start recording and processing
    if st.button("Record"):
        with st.spinner("Recording and processing..."):
            record_audio("recorded_audio.wav")

            transcribed_text = transcribe("recorded_audio.wav")

            formatted_history = format_history(st.session_state.chat_history)
            formatted_history.append({"role": "user", "content": transcribed_text})

            response_text = response(formatted_history)

            create_audio(response_text,actor)

            st.session_state.chat_history.append({"human": transcribed_text, "AI": response_text})

            for message in st.session_state.chat_history:
                st.markdown(f'<div class="css-ffhzg2">User: {message["human"]}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="css-1l6a57s">AI: {message["AI"]}</div>', unsafe_allow_html=True)

            play_audio("audio.mp3")
            time.sleep(1)
            

if __name__ == "__main__":
    main()
