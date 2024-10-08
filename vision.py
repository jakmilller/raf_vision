import base64
import requests

# this script takes a picture of a plate and determines what food is on it
# the available foods it can choose from are found in prompts.txt
# based off of https://platform.openai.com/docs/guides/vision and inference_class.py from FLAIR

# OpenAI API Key
api_key = "insert API key here"

# # Function to encode the image to base64 for processing
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

# path to image that gpt should look at
image_path = "plate_pic.jpg"

# Getting the base64 string
base64_image = encode_image(image_path)

# headers for http request
headers = {
  "Content-Type": "application/json",
  "Authorization": f"Bearer {api_key}"
}

# read in prompt from text file
with open("prompt.txt", 'r') as f:
            prompt_text = f.read()


payload = {
  "model": "gpt-4o-mini",
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": prompt_text
        },
        {
          "type": "image_url",
          "image_url": {
            "url": f"data:image/jpeg;base64,{base64_image}"
          }
        }
      ]
    }
  ],
  "max_tokens": 300
}

# grab and format response from API
response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
response_text =  response.json()['choices'][0]["message"]["content"]

print(response_text)