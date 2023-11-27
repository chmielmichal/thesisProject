from PIL import Image, ImageDraw, ImageFont
import os
import pygame
from pygame.locals import *

# Inicjalizacja Pygame
pygame.init()

# Ustawienia ekranu
screen = pygame.display.set_mode((1920, 1080))
pygame.display.set_caption("Image Viewer")

# Funkcja do wczytywania i wyświetlania obrazu z obramówką i napisami
def display_image(file_path):
    image = Image.open(file_path)
    
    # Dodaj obramowanie
    border_size = 10
    bordered_image = Image.new('RGB', (image.width + 2 * border_size, image.height + 2 * border_size), 'white')
    bordered_image.paste(image, (border_size, border_size))

    # Dodaj napisy
    draw = ImageDraw.Draw(bordered_image)
    font = ImageFont.load_default()
    draw.text((10, image.height + border_size + 10), "Twój tekst tutaj", font=font, fill="black")

    # Zapisz tymczasowy plik z wynikiem
    result_path = "result.jpg"
    bordered_image.save(result_path)

    # Wyświetl obraz w oknie Pygame
    img = pygame.image.load(result_path)
    screen.blit(img, (0, 0))
    pygame.display.flip()

# Główna pętla programu
running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    # Tutaj umieść kod do wczytywania kolejnych obrazów z folderu
    image_folder = "D:\\thesisProject\\pictures"
    for filename in os.listdir(image_folder):
        if filename.endswith(".jpg"):
            file_path = os.path.join(image_folder, filename)
            display_image(file_path)
            pygame.time.wait(2000)  # Poczekaj 2 sekundy przed przejściem do kolejnego obrazu

pygame.quit()