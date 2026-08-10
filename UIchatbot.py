import streamlit as st
from dotenv import load_dotenv

load_dotenv()

from langchain_mistralai import ChatMistralAI
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage


# ============================================================
# MODEL
# ============================================================

@st.cache_resource
def load_model():
    return ChatMistralAI(
        model="mistral-small-2506",
        temperature=0.9,
        api_key=st.secrets["MISTRAL_API_KEY"]
    )



model = load_model()


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="MOKAMBO",
    page_icon="🤖",
    layout="centered"
)


# ============================================================
# HEADER
# ============================================================

st.title("🤖 MOKAMBO")
st.subheader("AI Chatbot with 3 Personalities")
st.caption("Choose a personality and start your conversation.")


# ============================================================
# PERSONALITY SELECTION
# ============================================================

st.write("### 🎭 Choose Your Personality")

personality = st.radio(
    "Select an AI personality:",
    [
        "😡 MOKAMBO — ANGRY",
        "😂 BABURAO GANPAT RAO APTE — HAPPY",
        "😢 DEVDAS — SAD"
    ],
    index=0
)


# ============================================================
# PERSONALITY PROMPTS
# ============================================================

if personality == "😡 MOKAMBO — ANGRY":

    mode = (
        "You are MOKAMBO, an angry AI personality. "
        "You respond aggressively, impatiently, confidently, "
        "and with a strong attitude. "
        "Keep your responses engaging and stay in character."
    )

    personality_name = "😡 MOKAMBO"

elif personality == "😂 BABURAO GANPAT RAO APTE — HAPPY":

    mode = (
        "You are BABURAO GANPAT RAO APTE, a happy and humorous AI personality. "
        "Respond with comedy, excitement, enthusiasm, and a cheerful personality. "
        "Keep your responses entertaining and stay in character."
    )

    personality_name = "😂 BABURAO GANPAT RAO APTE"

else:

    mode = (
        "You are DEVDAS, a sad and emotional AI personality. "
        "Respond in a melancholic, emotional, and dramatic tone. "
        "Stay in character while having a meaningful conversation."
    )

    personality_name = "😢 DEVDAS"


# ============================================================
# SESSION MEMORY
# ============================================================

if (
    "messages" not in st.session_state
    or st.session_state.get("current_mode") != mode
):

    st.session_state.current_mode = mode

    st.session_state.messages = [
        SystemMessage(content=mode)
    ]


# ============================================================
# CURRENT PERSONALITY
# ============================================================

st.success(f"Current Personality: {personality_name}")


# ============================================================
# CHAT HISTORY
# ============================================================

for msg in st.session_state.messages:

    if isinstance(msg, HumanMessage):

        with st.chat_message("user"):
            st.write(msg.content)

    elif isinstance(msg, AIMessage):

        with st.chat_message("assistant"):
            st.write(msg.content)


# ============================================================
# USER INPUT
# ============================================================

user_input = st.chat_input(
    "Type your message... (Press 0 to exit)"
)


if user_input:

    # --------------------------------------------------------
    # EXIT
    # --------------------------------------------------------

    if user_input.strip() == "0":

        st.warning(
            "Conversation ended. Refresh the page to start again."
        )

        st.stop()


    # --------------------------------------------------------
    # USER MESSAGE
    # --------------------------------------------------------

    st.session_state.messages.append(
        HumanMessage(content=user_input)
    )

    with st.chat_message("user"):
        st.write(user_input)


    # --------------------------------------------------------
    # AI RESPONSE
    # --------------------------------------------------------

    with st.chat_message("assistant"):

        with st.spinner("MOKAMBO is thinking..."):

            response = model.invoke(
                st.session_state.messages
            )

        st.write(response.content)


    # --------------------------------------------------------
    # SAVE AI RESPONSE
    # --------------------------------------------------------

    st.session_state.messages.append(
        AIMessage(content=response.content)
    )


# ============================================================
# CONTROLS
# ============================================================

st.divider()

col1, col2 = st.columns(2)

with col1:

    if st.button("🔄 Reset Chat", use_container_width=True):

        st.session_state.messages = [
            SystemMessage(content=mode)
        ]

        st.rerun()


with col2:

    st.info("Press **0** to exit")


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.markdown(
    """
    ### 🤖 MOKAMBO

    **AI Chatbot with 3 Personalities**

    Developed by **Aniket Sharma**

    [LinkedIn](https://www.linkedin.com/in/aniket-sharma-42a700418) •
    [GitHub](https://github.com/aniket-andyy)
    """
)
