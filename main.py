import streamlit as st
from groq import Groq

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
    # Set page config with title and layout
    st.set_page_config(page_title="🦙💬 Llama 3 Chatbot", page_icon=":speech_balloon:", layout="wide")

    # Add custom CSS for dark theme styling
    st.markdown("""
        <style>
        .css-1d391kg { 
            background-color: #1e1e1e; /* Dark background */
            color: #f5f5f5; /* Light text color */
        }
        .css-1d391kg p {
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

    # Sidebar for additional customization if needed
    st.sidebar.title("Chatbot Customization")
    st.sidebar.write("Customize your chatbot experience.")

    # Chat input and history management
    user_question = st.text_input("Ask a question:")

    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    if user_question:
        # Prepare the history and add the current user question
        formatted_history = format_history(st.session_state.chat_history)
        formatted_history.append({"role": "user", "content": user_question})

        # Get the response from the model
        response_text = response(formatted_history)

        # Update the session state with the new exchange
        st.session_state.chat_history.append({"human": user_question, "AI": response_text})

        # Display the response
        for message in st.session_state.chat_history:
            if message["human"] == user_question:
                st.markdown(f'<div class="css-ffhzg2">User: {message["human"]}</div>', unsafe_allow_html=True)
            if message["AI"] == response_text:
                st.markdown(f'<div class="css-1l6a57s">AI: {message["AI"]}</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
