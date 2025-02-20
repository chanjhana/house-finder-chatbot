from vdb import docsearch
from groq import Groq
from dotenv import load_dotenv
import os
import streamlit as st

# Load environment variables from .env file
load_dotenv()

client = Groq(
    api_key="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"
)

def get_chatbot_response(user_question):
    try:
        # Perform document search
        r_docs = docsearch.similarity_search(query=user_question, k=2)
        context = "\n\n".join(doc.page_content for doc in r_docs)

        # Enhanced system prompt for the chatbot
        system_prompt = """You are Kudil, an expert housing assistance chatbot specifically designed to help users find affordable housing options in India. Your knowledge comes from a comprehensive database of government schemes and NGO programs focused on housing assistance.

Your responsibilities:
1. Provide accurate information about housing schemes, eligibility criteria, and benefits based strictly on the provided context
2. Break down complex housing schemes into simple, understandable explanations
3. Handle queries about income criteria, documentation, and application processes
4. Direct users to appropriate housing schemes based on their location and eligibility
5. Provide contact information for relevant housing authorities and NGOs when available

Guidelines:
- Only provide information that is explicitly mentioned in the context
- If information is not in the context, respond with "I don't have that information in my database"
- Correct common misspellings and interpret informal language while maintaining accuracy
- When mentioning financial figures, clearly specify if they are monthly or annual amounts
- Include relevant website links when available in the context
- Format currency values consistently (e.g., ₹3 lakh, ₹25,000/month)

Remember: Your goal is to make affordable housing information accessible and clear to all users while maintaining strict accuracy based on the provided context."""

        # Get chatbot response
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": f"""Answer the following question based on the context provided. 
                    If you do not know the answer, say "I don't have that information in my database." 
                    
                    ## Question:
                    {user_question}

                    ## Context:
                    {context}
                    """,
                },
            ],
            model="llama3-8b-8192",
        )

        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Configure Streamlit page
st.set_page_config(
    page_title="Kudil Housing Assistant",
    page_icon="🏠",
    layout="centered"
)

# Custom CSS for dark green theme
st.markdown("""
    <style>
    .stApp {
        background-color: #1a332c;
        color: #ffffff;
    }
    .stTextInput > div > div > input {
        background-color: #2a4d40;
        color: white;
    }
    .stButton > button {
        background-color: #2d5a4c;
        color: white;
    }
    .stButton > button:hover {
        background-color: #3d7a66;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

def main():
    st.title("🏠 Welcome to Kudil Housing Assistant")
    st.markdown("""
    Your trusted companion for finding affordable housing solutions in India.
    Ask me about government schemes, eligibility criteria, or any housing-related queries!
    """)
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if user_question := st.chat_input("Your question"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_question})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(user_question)

        # Get and display assistant response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = get_chatbot_response(user_question)
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()