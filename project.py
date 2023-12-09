from google.cloud import storage
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import os
import pygame
from pygame.locals import *

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

    # Wait for a short duration before displaying the next image
    pygame.time.wait(3000)

# Pygame initialization
pygame.init()
screen = pygame.display.set_mode((2560, 1440))
pygame.display.set_caption("Image Viewer")

# Function to display an image with frame and text
def display_image(file_path):
    image = Image.open(file_path)

    # Adjust frame size and position
    border_width = 200
    border_height = 300
    composite_image = Image.new('RGB', (image.width + border_width, image.height + border_height), 'white')
    composite_image.paste(image, (0, 0))

    # Add frame in the shape of the letter "L"
    draw = ImageDraw.Draw(composite_image)
    draw.rectangle([(image.width, 0), (image.width + border_width, image.height)], outline="white", width=border_width)
    draw.rectangle([(0, image.height), (image.width, image.height + border_height)], outline="white", width=border_width)

    # Add text
    font = ImageFont.load_default()
    draw.text((10, image.height + border_width + 10), "Your text here", font=font, fill="black")

    # Save temporary file with the result
    result_path = "result.jpg"
    composite_image.save(result_path)

    # Display the image in the Pygame window
    img = pygame.image.load(result_path)
    screen.blit(img, (0, 0))
    pygame.display.flip()

# Main loop
running = True

try:
    while running:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                running = False

        # Get a list of all objects in the GCS bucket
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











