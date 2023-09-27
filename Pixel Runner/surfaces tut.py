import pygame
from sys import exit

pygame.init()

screen_width, screen_height = 800, 400

# every image, text or colour in pygame is added using a surfacce
# There  are mainly two types of surfaces :- display surface(window) and a regular surface
win = pygame.display.set_mode((screen_width, screen_height))  # display surface
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()

red = (255, 0, 0)

test_surface = pygame.Surface((100, 200))
test_surface.fill(red)    # All surfaces are black by default

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    win.blit(test_surface, (100, 100))

    pygame.display.update()
    clock.tick(60)