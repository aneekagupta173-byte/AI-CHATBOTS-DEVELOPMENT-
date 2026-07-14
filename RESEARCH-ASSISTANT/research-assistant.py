import os
import streamlit as st
from dotenv import load_dotenv
from google import genai




load_dotenv()

# Create the title shown at the top of the Streamlit page.
st.title("Lets research ")






# Read the Gemini API key from the environment.
api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("api_key")
if not api_key:
    # Stop the app if no API key is available.
    st.error("Add your Gemini API key to the GOOGLE_API_KEY or api_key environment variable before running the chatbot.")
    st.stop()

# Create the Gemini client using the API key.
client = genai.Client(api_key=api_key)

# Keep a small conversation history in the session so recent messages can be displayed.
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Get the user's question from the text input box.
user_message = st.text_input("START THE CONVERSATION HERE:", key="user_message")




# Run this block when the user clicks the SEND button.
if st.button("SEND"):
    if user_message:
        # Build the prompt that tells Gemini how to behave and what question to answer.
        prompt = (
            f"You are a research professor who must repond to user query and guide them in the perfect way to research about their topic and how to start. Be motivating but in a strict tone. always provide reality checks and suggest them tools to make their research better. If the user asks for a specific topic, provide them with a step-by-step guide to research it. If the user asks for general advice, provide them with a list of tips and resources to help them improve their research skills. Always be clear and concise in your responses. \n\n"
            f"User: {user_message}"
            
        )

        # Show a loading spinner while the model is generating a reply.
        with st.spinner(f"Resolving {user_message}..."):
            try:
                # Send the prompt to Gemini and get the response.
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt,
                )
            
            except Exception as exc:
                # Show an error message if the API call fails.
                st.error(f"Failed to get a model response: {exc}")
                st.stop()

        # Display the successful result to the user.
        st.success("Response received!")
        st.write(response.text)

        st.session_state.chat_history.append({"user": user_message, "bot": response.text})
        st.write("Conversation History:")
        st.write(st.session_state.chat_history)
    else:
        # Warn the user if they tried to send an empty message.
        st.warning("Enter a message!")
