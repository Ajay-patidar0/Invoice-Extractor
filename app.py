from dotenv import load_dotenv
load_dotenv()  #load all the environment variable from .env

import streamlit as st
import os
from PIL import Image 
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

#load gemini pro vision model 
model=genai.GenerativeModel('gemini-1.5-flash')

def get_gemini_response(input,image,user_prompt):
    response=model.generate_content([input,image[0],user_prompt])
    return response.text

def input_image_details(uploaded_file):
    if uploaded_file is not None:
        #Read the file into bytes
        bytes_data=uploaded_file.getvalue()

        image_parts=[
            {
                "mime_type":uploaded_file.type, #get the mime time of uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No File Uploaded")

# Initialize our streamlit app

st.set_page_config(page_title="Invoice Extractor")

st.header("Invoice Extractor")
input=st.text_input("Input Prompt :",key="input")

uploaded_file= st.file_uploader("choose an image of the invoice...", type=["jpg","jpeg","png"])


if uploaded_file is not None:
    image=Image.open(uploaded_file)
    st.image(image,caption="Uploaded Image",use_column_width=True)

submit=st.button("Tell me about the Invoice")

input_prompt="""
 You are an expert in understanding invoices.
 You will receive input images as invoices &
 You will have to answer questions based on the input image"""

# if submit button is clicked
if submit:
    image_data=input_image_details(uploaded_file)
    response=get_gemini_response(input_prompt,image_data,input)
    st.subheader("The response is ")
    st.write(response)