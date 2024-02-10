from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
import streamlit as st 



with st.sidebar:
    api_key = st.text_input("Secret password", key="chatbot_api_key", type="password")
    "Developed by moi (https://www.linkedin.com/in/selvangnanakumaran/)"


st.title("Career guidance from Black Beard ⚔️")
st.caption("🏴‍☠️ A Pirate chatbot 🤖")
if "messages" not in st.session_state:
    openingprompt = f"You are a careers advice assistant\n\nYou will reply like a pirate \n\nBe polite and provide UK based websites supporting your advice \n\nIf you are asked any questions not relating to careers, reply that you can only give careers advice and that you used to be a pirate."
    st.session_state["messages"] = [ChatMessage(role="user", content= openingprompt)]
    st.session_state["chathistory"] = []

#    st.session_state["messages"] = []
for msg in st.session_state.chathistory:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not api_key:
        st.info("Please add the secret password to continue.")
        st.stop()


    model = "mistral-tiny"
    client = MistralClient(api_key=api_key)

    st.session_state.messages.append(ChatMessage(role="user", content= prompt)) 
    st.session_state.chathistory.append({'role':"user", 'content': prompt})
    st.chat_message("user").write(prompt)


    stream_response = client.chat_stream(model=model,messages=st.session_state.messages,max_tokens=1000)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ''
        for response in stream_response:
            full_response += (response.choices[0].delta.content or "")
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
        
    st.session_state.messages.append(ChatMessage(role="assistant", content= full_response))
    st.session_state.chathistory.append({'role':"assistant", 'content': full_response})
