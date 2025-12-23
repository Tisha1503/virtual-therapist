import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="Virtual Therapist", page_icon="🌱")
st.title("🌱 Virtual Therapist")
st.markdown("Providing mental health support anytime and anywhere.") # [cite: 9]

api_key = st.sidebar.text_input("Enter OpenAI API Key", type="password")
client = OpenAI(api_key=api_key) if api_key else None

def load_knowledge():
    try:
        with open("knowledge.txt", "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        return "Focus on active listening and empathy."

additional_context = load_knowledge()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("How can I assist you today?"):
    if not api_key:
        st.error("Please enter your API key in the sidebar.")
    else:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": f"You are a Virtual Therapist. Use this info to help: {additional_context}"},
                    *st.session_state.messages
                ]
            )
            answer = response.choices[0].message.content
            st.markdown(answer)
        
        st.session_state.messages.append({"role": "assistant", "content": answer})