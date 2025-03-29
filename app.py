import streamlit as st
import requests as re
import machine_learning as ml
import feature_extraction as fe
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup


st.header('Phishing Websites Detection System')

st.subheader('About')

st.write('Phishing attacks have emerged as a significant cybersecurity threat, exploiting human trust to steal sensitive information'
 'through deceptive websites. These attacks compromise personal data, financial credentials, and corporate security.')

st.write('This project harnesses the power of machine learning to detect and classify phishing websites effectively. By analyzing patterns and characteristics of fraudulent sites, our system aims to minimize online fraud and enhance user security, making digital interactions safer for everyone.')


st.subheader('Phishing Websites')
st.write('http://www.onlinesbi.digital')
st.write('https://nbmfsd.com/')

st.subheader('Secure Websites')
st.write('https://web.whatsapp.com/')
st.write('https://www.instagram.com/')
st.write('https://www.facebook.com/')


list= ['Neural Network', 'Decision Tree', 'Random Forest', 'AdaBoost', 'Support Vector Machine']


model = ml.nn_model
value = st.selectbox('Select Model',list)

if value == 'Neural Network':

    st.write('You Selected:- ',value)

    url = st.text_input("Enter Your URL")

    if st.button('Submit'):
        st.write('Your Given URL:- ',url)
        try:
            response = re.get(url, verify=False, timeout=4)
            if response.status_code != 200:
                print(". HTTP connection was not successful for the URL: ", url)
                st.write('website band hai')
            else:
                soup = BeautifulSoup(response.content, "html.parser")
                vector = [fe.create_vector(soup)]  # it should be 2d array, so I added []
                result = model.predict(vector)
                st.write(result)
                if result[0] == 0:
                    st.success("This web page seems a legitimate!")
                    st.balloons()
                else:
                    st.warning("Attention! This web page is a potential PHISHING!")
                    st.snow()
        except re.exceptions.RequestException as e:
            print("--> ", e)
else:
    st.write('MODEL UNDER PROCESSING')