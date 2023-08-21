import openai
import streamlit as st
import os
from moviepy.editor import *
import whisper
import torch
from os import path
from pydub import AudioSegment
from pytube import YouTube

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    # "[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"
    # "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

def chat_function(complete_prompt):                
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]
    
    # for msg in st.session_state.messages:
    #     st.chat_message(msg["role"]).write(msg["content"])
    # st.text(st.session_state.messages)
    # st.text(complete_prompt)
    if prompts := st.chat_input():
        if not openai_api_key:
            st.info("Please add your OpenAI API key to continue.")
            st.stop()
        # st.text(complete_prompt)
        prompt = complete_prompt + prompts
        openai.api_key = openai_api_key
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompts)
        response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
        msg = response.choices[0].message
        st.session_state.messages.append(msg)
        st.chat_message("assistant").write(msg.content)
    # if st.sidebar.button("clear chat"):
    #     st.session_state.messages.clear()
    #     st.stop()   



st.title("_Welcome to your own 💬Chatbot_ :sunglasses:")
Input_model = st.sidebar.selectbox("Slect the source of information", ("Data Load","Chat"))
# complete_prompt = ""
if Input_model == "Data Load":
    source_input = st.selectbox("Select the source of information", ("Video","PDF","Document"))
    if source_input == 'Video':
        url = st.text_input("Enter Youtube Video Link")
        if url:
            yt=YouTube(url)
            t=yt.streams.filter(res="144p").all()
            path = t[0].download()
            video = VideoFileClip(path)
            video.audio.write_audiofile("output.mp3")
            # src = "output.mp3"
            # dst = "test.wav"

            # sound = AudioSegment.from_mp3(src)
            # sound.export(dst, format="wav")
            # import torch
            # DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
            # model = whisper.load_model("tiny.en").to(DEVICE)
            # transcription = model.transcribe(dst, language="en")
            # extracted_text = transcription['text']
            # # if st.sidebar.button('Click To Chat'):
            # complete_prompt = extracted_text + """ This marks the end of text provided,
            #                 now you are best text explainer, use this above text to answer my below question :
            #                 question is : """

            # f = open("myfile.txt", "w")
            # f.write(complete_prompt)
            # f.close()
            
if Input_model == "Chat":
    f = open("myfile.txt", "r")
    f = f.read()
    st.text(f)
    f = open("myfile.txt", "w")
    f.write("hello")
    f.close()
    f = open("myfile.txt", "r")
    f = f.read()
    st.text(f)
    if  len(list(f))!=0:
        complete_prompt = str(f)
        chat_function(complete_prompt)
    else:
        st.error("load data")
        st.stop()
