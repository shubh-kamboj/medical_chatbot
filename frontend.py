import streamlit as st
import requests

backend_url = "http://127.0.0.1:8000/ask"

st.set_page_config(page_title="Medical Chatbot", layout="wide")
st.title(" 🧠 StaySafe | AI Medical Health Support..")

#  Initialize the session history in session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# chat input
user_input = st.chat_input("What's on your mind ? ")
if user_input:
    # append user message
    st.session_state.chat_history.append({'role':'user', 'content': user_input})
    # send request to backend
    response = requests.post(backend_url, json={"message":user_input})

    #  Ai Agent response
    # res = "Ye active project environment mein installed packages ki list show karega."
    st.session_state.chat_history.append({"role": "assistant", "content": f'{response.json()["response"]} WITH TOOL: [{response.json()["tool_called"]}]'})


#  Show chat history
for msg in st.session_state.chat_history:
    with st.chat_message(msg['role']):
        st.write(msg['content'])