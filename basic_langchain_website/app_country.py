import streamlit as st
import langchain_helper

st.title("Country Capital Tourist Spot Generator")

places = st.sidebar.selectbox("Pick a Country",("India","China","USA"))

if places:
    response = langchain_helper.generate_places_visit(places)
    st.header(response['Capital'].strip())
    visit_places = response['Places'].strip().split(",")
    st.write("**Places to Visit**")
    for place in visit_places:
        st.write(place.strip())
