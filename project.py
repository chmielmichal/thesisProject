from google.cloud import storage
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import os
import pygame
from pygame.locals import *
import requests
from datetime import datetime
import qrcode

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "D:\\thesisProject\\thesisproject-8470d-a832794d2e11.json"

# Initialize Google Cloud Storage client
client = storage.Client()

# GCS bucket information
bucket_name = "thesisproject-8470d.appspot.com"

# Local folder to save downloaded images
local_folder = "downloaded_images"
os.makedirs(local_folder, exist_ok=True)

# Function to download and display an image from GCS
def display_image_from_gcs(object_name):
    # Local path to save the downloaded image
    local_path = os.path.join(local_folder, object_name)

    # Download image from GCS
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(object_name)
    blob.download_to_filename(local_path)

    # Display the downloaded image using Pygame
    display_image(local_path)

    # Clean up: Delete the local downloaded image file
    os.remove(local_path)

    # Display time
    pygame.time.wait(3000)

#QR code
def generate_qr_code(link):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(link)
    qr.make(fit=True)

    qr_img = qr.make_image(fill_color="black", back_color="white")
    return qr_img

# Pygame initialization
pygame.init()
screen = pygame.display.set_mode((2560, 1440))
pygame.display.set_caption("INFOKIOSK")

# Display
def display_image(file_path):
    image = Image.open(file_path)

    # Frame size and position
    border_width = int((screen.get_width() - image.width) / 2)
    border_height = int((screen.get_height() - image.height) / 2)
    composite_image = Image.new('RGB', (screen.get_width(), screen.get_height()), 'white')

    # Slide position
    composite_image.paste(image, (0, 0))

    # Borders
    draw = ImageDraw.Draw(composite_image)
    border_color = (23, 55, 110)
    draw.rectangle([(image.width, 0), (screen.get_width(), screen.get_height())], fill=border_color)
    draw.rectangle([(0, image.height), (screen.get_width(), screen.get_height())], fill=border_color)

    # Weather information from OpenWeatherMap API
    weather_text = get_weather_data()
    font_size = 20
    font = ImageFont.truetype("arial.ttf", font_size)
    weather_text_bbox = draw.textbbox((0, 0), weather_text, font=font)
    weather_text_width, weather_text_height = weather_text_bbox[2] - weather_text_bbox[0], weather_text_bbox[3] - weather_text_bbox[1]
    draw.text((screen.get_width() - weather_text_width - 190, border_height + 340), weather_text, font=font, fill="white")

    # Time display
    current_time = datetime.now().strftime("%H:%M")
    time_font_size = 50
    time_font = ImageFont.truetype("arial.ttf", time_font_size)
    text_bbox = draw.textbbox((0, 0), current_time, font=time_font)
    text_width, text_height = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]
    draw.text((screen.get_width() - text_width - 250, border_height + 200), current_time, font=time_font, fill="white")

    # Date display
    current_date = datetime.now().strftime("%d-%b-%Y")
    date_font_size = 30
    date_font = ImageFont.truetype("arial.ttf", date_font_size)
    date_text_bbox = draw.textbbox((0, 0), current_date, font=date_font)
    date_text_width, date_text_height = date_text_bbox[2] - date_text_bbox[0], date_text_bbox[3] - date_text_bbox[1]
    draw.text((screen.get_width() - date_text_width - 230, border_height + 270), current_date, font=date_font, fill="white")
    
    # Logo display
    logo_path = "logo/logo.jpg"
    logo = Image.open(logo_path)
    logo = logo.resize((300, 300))  
    composite_image.paste(logo, (screen.get_width() - logo.width - 160, 10))

    qr_code_link = "https://plany.ath.bielsko.pl"
    qr_code = generate_qr_code(qr_code_link)

    # Paste the QR code onto the composite image
    composite_image.paste(qr_code, (screen.get_width() - qr_code.width - 460, screen.get_height() - qr_code.height - 10))

    # Temp image
    result_path = "result.jpg"
    composite_image.save(result_path)

    # Pygame logics
    img = pygame.image.load(result_path)
    screen.blit(img, (0, 0))
    pygame.display.flip()

# OpenWeatherMap API
def get_weather_data():
    api_key = '84cea28a50728eb44f7ccde38994cb77'
    city_name = 'Chrzanów'  

    api_url = f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}'
    response = requests.get(api_url)
    data = response.json()

    # Information
    if 'main' in data and 'temp' in data['main']:
        temperature = round(data['main']['temp'] - 273.15)
        weather_description = data['weather'][0]['description']
        return f'Temperature: {temperature}°C\nWeather: {weather_description}'
    else:
        return 'Weather information not available'

# Main loop
running = True

try:
    while running:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                running = False

        # Get a list of all objects in the Google Cloud Service bucket
        bucket = client.get_bucket(bucket_name)
        blobs = bucket.list_blobs()

        # Download and display each image
        for blob in blobs:
            if blob.name.endswith(".jpg"):
                display_image_from_gcs(blob.name)

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    pygame.quit()