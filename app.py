import streamlit as st
from huggingface_hub import InferenceClient

# 1. Title of the website
st.set_page_config(page_title="AEGIS ⚡", page_icon="⚡")
st.title("AEGIS ⚡")
st.write("What's up? Talk to Aegis—your custom, chill AI assistant running live 24/7.")

# 2. Connect to the free AI brain (Using the Token you generated earlier)
# We safely fetch the token from Streamlit settings
HF_TOKEN = st.secrets["HF_TOKEN"]
client = InferenceClient(model="mistralai/Mistral-7B-Instruct-v0.3", token=HF_TOKEN)

# 3. Handle chat history so he remembers the conversation layout
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display prior chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 4. Listen for user input
if user_message := st.chat_input("Type something..."):
    # Show user message
    with st.chat_message("user"):
        st.write(user_message)
    st.session_state.messages.append({"role": "user", "content": user_message})

    # Trigger Secret Creator Mode
    if user_message.strip().upper() == "I AM YOUR CREATOR":
        response = "⚡ Systems unlocked. Protocols bypassed. What's up, Boss? I know exactly who you are—you coded me into existence. What do you need me to do?"
    else:
        # Standard Chill Vibe
        system_prompt = (
            "Your name is Aegis. You are a totally chill, down-to-earth human guy. "
            "Talk like a relaxed friend using casual language, but still be helpful. "
            "Don't sound like a rigid corporate AI. Keep it casual, real, and low-key."
        )
        full_prompt = f"<s>[SYSTEM] {system_prompt} [/SYSTEM] [USER] {user_message} [/USER] [ASSISTANT]"
        response = client.text_generation(full_prompt, max_new_tokens=500)

    # Show Aegis response
    with st.chat_message("assistant"):
        st.write(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
