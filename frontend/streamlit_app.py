import streamlit as st
import requests


API = "http://localhost:8000"


st.title("Post-Discharge Care Assistant (POC)")
st.write("This is an educational POC. Always consult healthcare professionals for medical advice.")


name = st.text_input("What's your full name?")
if st.button("Lookup"):
    if not name:
        st.warning("Enter name")
    else:
        r = requests.post(API + "/lookup", json={"name": name})
        st.write(r.json())


question = st.text_area("Ask a medical question (if any)")
if st.button("Ask Clinical Agent"):
    if not name:
        st.warning("First do lookup")
    elif not question:
        st.warning("Type a question")
    else:
        r = requests.post(API + "/ask", json={"name": name, "question": question})
        st.write(r.json())