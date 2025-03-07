import streamlit as st

st.header('Phishing Websites Detection System')

st.subheader('About')

st.write('Phishing attacks have emerged as a significant cybersecurity threat, exploiting human trust to steal sensitive information'
 'through deceptive websites. These attacks compromise personal data, financial credentials, and corporate security.')

st.write('This project harnesses the power of machine learning to detect and classify phishing websites effectively. By analyzing patterns and characteristics of fraudulent sites, our system aims to minimize online fraud and enhance user security, making digital interactions safer for everyone.')

list= ['Support Vector Machine', 'Decision Tree', 'Random Forest', 'AdaBoost', 'Neural Network']

value = st.selectbox('Select Model',list)

st.write('You Selected:- ',value)

url = st.text_input("Enter Your URL")

if st.button('Submit'):
    
    st.write('Your Given URL:- ',url)