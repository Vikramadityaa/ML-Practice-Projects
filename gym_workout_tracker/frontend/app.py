import streamlit as st
from frontend import update_and_plot

st.title("Workout Tracker")

tab1, tab2 = st.tabs(["Workout Tracker", "Protein Tracker"])

with tab1:
    update_and_plot()