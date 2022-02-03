import sys, pygame
from random import randint
import numpy as np

clock = pygame.time.Clock()

mass_positions = np.array([[0.0,0.0,0.0],[0.0,2.0,2.0]])

omega = 5.0

amps = [0.50248756, -0.50248756]

pygame.init()

screen = pygame.display.set_mode((700,700))

pygame.display.set_caption("Frequency Response Animation")

icon = pygame.image.load("Images/spring_icon.png").convert_alpha()
spring_image = pygame.image.load("Images/spring.png").convert_alpha()
m_e_image = pygame.image.load("Images/me.png").convert_alpha()
m_1_image = pygame.image.load("Images/m1.png").convert_alpha()
m_2_image = pygame.image.load("Images/m2.png").convert_alpha()
m_3_image = pygame.image.load("Images/m3.png").convert_alpha()
m_4_image = pygame.image.load("Images/m4.png").convert_alpha()
m_5_image = pygame.image.load("Images/m5.png").convert_alpha()
mass_images = [m_e_image,m_1_image,m_2_image,m_3_image,m_4_image,m_5_image]
pygame.display.set_icon(icon)

def Mass(x,y,mass_no):

    screen.blit(mass_images[mass_no], [int(50.0*x+350.0), int(600.0-50.0*y)])

running = True

t = 0.0

while running:

    screen.fill((140,255,251))
    
    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False

    # Game Code Here
    for i in range(0,len(mass_positions)):

        mass_positions[i] = np.array([0,mass_positions[i][2] + amps[i]*np.cos(omega*t), mass_positions[i][2]])

        Mass(mass_positions[i][0],mass_positions[i][1],i)
        
    pygame.display.update()

    clock.tick(50)
    t += 0.02
    
pygame.display.quit()
pygame.quit()
sys.exit()

    



