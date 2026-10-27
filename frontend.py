import streamlit as st

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

    #  Ai Agent response
    dummy_response = "Ye active project environment mein installed packages ki list show karega."
    st.session_state.chat_history.append({"role":"assistant", "content":dummy_response}) 

#  Show chat history
for msg in st.session_state.chat_history:
    with st.chat_message(msg['role']):
        st.write(msg['content'])