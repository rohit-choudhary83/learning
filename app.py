import streamlit as st
import requests
import machine_learning as ml
import feature_extraction as fe
from bs4 import BeautifulSoup
import base64
import pandas as pd

st.header('🔎 PHISHING WEBSITES DETECTION SYSTEM')

# Function to encode image in base64
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        return None

image_path = "C:/Users/smrit/Downloads/learning/learning/image/pwds.png"
image_base64 = get_base64_image(image_path)

if image_base64:
    page_bg_img = f'''
    <style>
    [data-testid="stAppViewContainer"] {{
        background-image: url("data:image/png;base64,{image_base64}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
        color: black;
    }}
    </style>
    '''
    st.markdown(page_bg_img, unsafe_allow_html=True)
else:
    st.warning("⚠️ Background image not found!")

# About Section
st.subheader('📌 About')
st.write(
    "Phishing attacks trick users into entering sensitive information on fake websites. Our system analyzes site structure and content "
    "to detect possible phishing attempts using machine learning."
)

# Example URLs
st.subheader('🚨 Phishing Websites')
st.write('http://www.onlinesbi.digital')

st.subheader('✅ Secure Websites')
st.write('https://web.whatsapp.com/')
st.write('https://www.instagram.com/')
st.write('https://www.facebook.com/')

# Model selection
model_list = ['Neural Network', 'Decision Tree', 'Random Forest', 'AdaBoost', 'Support Vector Machine']
value = st.selectbox('📊 Select Model', model_list)

if value == 'Neural Network':
    st.write(f'✅ You Selected: {value}')

    url = st.text_input("🌍 Enter Website URL")

    if st.button('🔍 Analyze'):
        st.write(f'🔗 Analyzing: {url}...')

        try:
            response = requests.get(url,verify=False, timeout=4)
            if response.status_code != 200:
                st.error('❌ Website is not accessible!')
            else:
                soup = BeautifulSoup(response.content, "html.parser")
                feature_vector = fe.create_vector(soup)

                if not isinstance(feature_vector, list):
                    st.error("⚠️ Feature extraction failed.")
                else:
                    st.write(f"🛠️ Extracted Features: {feature_vector}")

                    model = ml.nn_model  # Load trained model
                    result = model.predict([feature_vector])  # Needs 2D input
                    prediction = "Legitimate ✅" if result[0] == 0 else "⚠️ Potential Phishing"

                    st.subheader(f'🔍 Prediction: {prediction}')

                    if result[0] == 0:
                        st.success("This web page seems **legitimate!** 🟢")
                        st.balloons()
                    else:
                        st.warning("⚠️ **This web page might be a phishing site!**")
                        st.snow()

                        # Detailed Analysis
                        st.subheader("⚠️ Why is this site suspicious?")
                        feature_labels = [
                            "Has Title", "Has Input", "Has Button", "Has Image", "Has Submit", "Has Link",
                            "Has Password Field", "Has Email Input", "Has Hidden Elements", "Has Audio", "Has Video",
                            "Number of Inputs", "Number of Buttons", "Number of Images", "Number of Options",
                            "Number of Links", "Number of Scripts", "Length of Title", "Has H1", "Has H2",
                            "Has H3", "Length of Text", "Number of Meta Tags", "Has Iframe", "Has Object",
                            "Has Picture", "Number of Spans", "Number of Tables", "Has Form"
                        ]
                        # Ensure feature vector and labels have the same length
                        min_length = min(len(feature_labels), len(feature_vector))
                        df = pd.DataFrame({"Feature": feature_labels[:min_length], "Value": feature_vector[:min_length]})

                        # Highlight risky features
                        def highlight_risk(val):
                            if isinstance(val, int) and val > 10:
                                return 'background-color: red; color: white'
                            elif isinstance(val, int) and val > 5:
                                return 'background-color: yellow;'
                            return ''

                        st.dataframe(df.style.applymap(highlight_risk, subset=['Value']))


                        # Explanation of key risk factors
                        explanations = {
                            "Has Password Field": "⚠️ A login form without SSL is risky.",
                            "Has Hidden Elements": "⚠️ Hidden elements can be used to steal data.",
                            "Has Iframe": "⚠️ Iframes can embed malicious content.",
                            "Number of Links": "⚠️ Too many links may indicate phishing.",
                            "Number of Inputs": "⚠️ Phishing sites often have multiple input fields to steal data."
                        }

                        for feature, explanation in explanations.items():
                            if feature in df["Feature"].values:
                                feature_value = df[df["Feature"] == feature]["Value"].values[0]
                                if feature_value > 0:
                                    st.write(f"🔴 **{feature}**: {explanation}")

        except requests.exceptions.RequestException as e:
            st.error(f"❌ Error fetching URL: {e}")
else:
    st.info('⏳ MODEL UNDER PROCESSING')
