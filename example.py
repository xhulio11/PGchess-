import pygame

pygame.init()

# create a main surface to draw to
main_surface = pygame.display.set_mode((800, 600))

# create a surface for a frame
frame_surface = pygame.Surface((400, 300))

# draw something on the frame surface
frame_surface.fill((255, 255, 255))
pygame.draw.rect(frame_surface, (0, 0, 0), (50, 50, 100, 100))

# blit the frame surface onto the main surface
main_surface.blit(frame_surface, (200, 150))

# update the display
pygame.display.update()

# wait for the user to close the window
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
