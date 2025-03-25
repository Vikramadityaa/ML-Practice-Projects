import streamlit as st
from frontend import ask_and_answer

st.title("ML/DS Question Answering")

tab1, = st.tabs(["DS Questions"])

with tab1:
    ask_and_answer()