import os
import tempfile
import streamlit as st
from embedchain import App

def embedchain_bot(db_path, api_key):
    return App.from_config(
        config={
            "llm": {
                "provider": "openai",
                "config": {
                    "model": "gpt-4o",
                    "temperature": 0.5,
                    "api_key": api_key
                }
            },
            "vectordb": {
                "provider": "chroma",
                "config": {
                    "dir": db_path
                }
            },
            "embedder": {
                "provider": "openai",
                "config": {
                    "api_key": api_key
                }
            }
        }
    )
    
st.title("Chat with any YouTube video!")
st.caption("This app allows you to access the content of any YouTube video and chat with it. You can ask questions, get summaries, and more!")

openai_access_token = st.text_input("OpenAI API Key", type="password")

if openai_access_token:
    db_path = tempfile.mkdtemp()
    app = embedchain_bot(db_path, openai_access_token)
    
    video_url = st.text_input("Enter YouTube video URL", type="default")
    if video_url:
        app.add(video_url, data_type="youtube_video")
        st.success(f"Added video {video_url} to knowledge base!")
        
    prompt = st.text_input("Ask a question or provide a prompt", type="default")

    if prompt:
        response = app.chat(prompt)
        st.write(response)
