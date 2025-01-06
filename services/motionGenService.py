import requests
import base64

# Use this function to convert an image file from the filesystem to base64
def image_file_to_base64(image_path):
    with open(image_path, 'rb') as f:
        image_data = f.read()
    return base64.b64encode(image_data).decode('utf-8')

# Use this function to fetch an image from a URL and convert it to base64
def image_url_to_base64(image_url):
    response = requests.get(image_url)
    image_data = response.content
    return base64.b64encode(image_data).decode('utf-8')

api_key = "SG_9e2ce2defed043dc"
url = "https://api.segmind.com/v1/kling-image2video"

# Request payload
data = {
  "image": image_file_to_base64("blog_image_20241212_113618.png"),  # Or use image_file_to_base64("IMAGE_PATH")
  "prompt": "Barnaby, a small bunny, bounces beside a babbling brook. Blue and bright butterflies flutter nearby. He has a button nose.",
  "negative_prompt": "No sudden movements, no fast zooms.",
  "cfg_scale": 0.5,
  "mode": "pro",
  "duration": 5
}

headers = {'x-api-key': api_key}

response = requests.post(url, json=data, headers=headers)
print(response.content)  # The response is the generated image