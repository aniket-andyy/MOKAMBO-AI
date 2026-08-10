import streamlit as st
from dotenv import load_dotenv

load_dotenv()

from langchain_mistralai import ChatMistralAI
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage


# ---------------- MODEL ----------------
model = ChatMistralAI(
    model="mistral-small-2506",
    temperature=0.9
)


# ---------------- PAGE ----------------
st.set_page_config(
    page_title="MOKAMBO",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 MOKAMBO")
st.subheader("AI Chatbot with 3 Personalities")
st.caption("Developed by Aniket Sharma")


# ---------------- PERSONALITY SELECTION ----------------
st.write("### Choose Your AI Personality")

personality = st.radio(
    "Select one:",
    [
        "😡 MOKAMBO (ANGRY)",
        "😂 BABURAO GANPAT RAO APTE (HAPPY)",
        "😢 DEVDAS (SAD)"
    ],
    index=0
)


# ---------------- MAP PERSONALITY ----------------
if personality == "😡 MOKAMBO (ANGRY)":

    mode = (
        "You are MOKAMBO, an angry AI personality. "
        "You respond aggressively, impatiently, confidently, "
        "and with a strong attitude. Keep your responses engaging "
        "and stay in character."
    )

elif personality == "😂 BABURAO GANPAT RAO APTE (HAPPY)":

    mode = (
        "You are BABURAO GANPAT RAO APTE, a happy and humorous AI personality. "
        "Respond with comedy, excitement, enthusiasm, and a cheerful personality. "
        "Keep your responses entertaining and stay in character."
    )

else:

    mode = (
        "You are DEVDAS, a sad and emotional AI personality. "
        "Respond in a melancholic, emotional, and dramatic tone. "
        "Stay in character while having a meaningful conversation."
    )


# ---------------- SESSION MEMORY ----------------
if (
    "messages" not in st.session_state
    or st.session_state.get("current_mode") != mode
):
    st.session_state.current_mode = mode
    st.session_state.messages = [
        SystemMessage(content=mode)
    ]


# ---------------- CURRENT PERSONALITY ----------------
st.info(f"Current Personality: {personality}")


# ---------------- DISPLAY CHAT ----------------
for msg in st.session_state.messages:

    if isinstance(msg, HumanMessage):

        with st.chat_message("user"):
            st.write(msg.content)

    elif isinstance(msg, AIMessage):

        with st.chat_message("assistant"):
            st.write(msg.content)


# ---------------- USER INPUT ----------------
user_input = st.chat_input(
    "Say something... (Press 0 to exit)"
)


if user_input:

    # ---------------- EXIT ----------------
    if user_input == "0":

        st.warning(
            "Conversation ended. Refresh the page to start again."
        )

        st.stop()


    # ---------------- ADD USER MESSAGE ----------------
    st.session_state.messages.append(
        HumanMessage(content=user_input)
    )

    with st.chat_message("user"):
        st.write(user_input)


    # ---------------- GET AI RESPONSE ----------------
    response = model.invoke(
        st.session_state.messages
    )


    # ---------------- ADD AI MESSAGE ----------------
    st.session_state.messages.append(
        AIMessage(content=response.content)
    )

    with st.chat_message("assistant"):
        st.write(response.content)


# ---------------- RESET CHAT ----------------
st.divider()

if st.button("🔄 Reset Chat"):

    st.session_state.messages = [
        SystemMessage(content=mode)
    ]

    st.rerun()


# ---------------- FOOTER ----------------
st.divider()

st.markdown(
    """
    **MOKAMBO — AI Chatbot with 3 Personalities**

    Developed by **Aniket Sharma**

    🔗 [LinkedIn](https://www.linkedin.com/in/aniket-sharma-42a700418)

    💻 [GitHub](https://github.com/aniket-andyy)
    """
  )
