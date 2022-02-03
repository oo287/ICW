import sys, pygame
from random import randint

pygame.init()

screen = pygame.display.set_mode((700,700))

pygame.display.set_caption("Frequency Response Animation")

icon = pygame.image.load("spring_icon.png")
m_e_image = pygame.image.load("me.png")
m_1_image = pygame.image.load("m1.png")
m_2_image = pygame.image.load("m2.png")
m_3_image = pygame.image.load("m3.png")
m_4_image = pygame.image.load("m4.png")
m_5_image = pygame.image.load("m5.png")
pygame.display.set_icon(icon)

def Object():

    screen.blit(me, [randint(0,700), randint(0,700)])

running = True

while running:

    screen.fill((0,0,0))
    
    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False

    # Game Code Here
    Object()

    pygame.display.update()
    
pygame.display.quit()
pygame.quit()
sys.exit()

    



