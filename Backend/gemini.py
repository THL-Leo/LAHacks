# import pathlib
# import textwrap

import google.generativeai as genai

# from IPython.display import display
# from IPython.display import Markdown

# def to_markdown(text):
#  text = text.replace('•', '  *')
#  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

#def to_markdown(text):
#    """Convert text to Markdown format."""
#    text = text.replace('•', '  *')
#    return textwrap.indent(text, '> ', predicate=lambda _: True)

# Used to securely store your API key
#from google.colab import userdata

import PIL.Image
#from PIL import Image

def list_to_image(string_list, width, height):
  # Convert the list of strings into a single string
  img_data = ''.join(string_list)
  
  # Create a new image object
  img = PIL.Image.new('RGB', (width, height))  # 'L' mode for grayscale

  # Convert the string data to pixel values and set them in the image
  pixels = [int(pixel) for pixel in img_data]
  img.putdata(pixels)

  return img

async def image_mood_generator(path):
  #input_img = list_to_image(input_list, width, height)

  GOOGLE_API_KEY='AIzaSyBKWsJtCf-WB1jpnHgen-87aeGPbqry5B4'

  genai.configure(api_key=GOOGLE_API_KEY)

  img_path = path[0] 
  img = PIL.Image.open(img_path)

  model = genai.GenerativeModel('gemini-pro-vision')

  response = model.generate_content(["""Please only respond with one exact word that reflects the 
                                     emotional mood conveyed by the provided image given this 
                                     list of words you can choose from. The list is [happy, sad, energetic]. 
                                     Feel free to interpret the mood in 
                                     any way you see fit, but only type one word, I want no other words or 
                                     sentences generated.""", img], stream=True)
  response.resolve()
  return response


