import pygame

screen = pygame.display.set_mode((100, 100))

while True:

    for event in pygame.event.get():

        if event.type == pygame.KEYDOWN:
            print(event.key)
