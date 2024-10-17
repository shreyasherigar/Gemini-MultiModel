import streamlit as st
import google.generativeai as genai



import io
from PIL import Image

genai.configure(api_key="API_KEY")

class TextInputHandler:
    def __init__(self,opt):
        self.model = genai.GenerativeModel(opt)
        
    def generate_response(self, input_text):
        text_response = self.model.generate_content(input_text, stream=True)
        for chunk in text_response:
            st.write(chunk.text)

class ImageInputHandler:
    def __init__(self,opt):
        self.model = genai.GenerativeModel(opt)

    def generate_response(self, input_image,prompt="Describe the image in one word"):
        # st.write("hi")
        image = Image.open(io.BytesIO(input_image.read()))

        image_response = self.model.generate_content([prompt, image])
        for chunk in image_response:
            st.write(chunk.text)

class TextToImageHandler:
    def __init__(self,opt):
        self.imagen = genai.ImageGenerationModel(opt)
    def generate_response(self,input):
        result =   self.imagen.generate_images(
                prompt=input,
                number_of_images=4,
                safety_filter_level="block_only_high",
                person_generation="allow_adult",
                aspect_ratio="3:4",
                negative_prompt="Outside",
        )
        return result


st.set_page_config(page_title="Gemini practice")  #Setting title of
selected_opt = st.selectbox("Select", options=["gemini-pro", "gemini-1.5-flash"])
st.header("Ask question")

if selected_opt == "gemini-pro":
    input_text = st.text_input("Input:", key="input")
    input_image = None
    text_input_handler= TextInputHandler(selected_opt)

elif selected_opt == "gemini-1.5-flash":
    input_image = st.file_uploader("Upload Image:", type=["jpg", "png"])
    input_text = ""
    image_input_handler=ImageInputHandler(selected_opt)

submit = st.button("Submit")

if submit:
    if input_text:
        text_input_handler.generate_response(input_text)
    elif input_image:
        image_input_handler.generate_response(input_image)
