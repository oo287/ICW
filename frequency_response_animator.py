import sys, pygame
from random import randint
import numpy as np
from equation_solver import y_amplitudes

print("\n\nPlease input the name of the txt file to read mass and stiffness matrices and force vector from.\n")

s = False

while not s:

    filename = input("File name: ")

    try:

        txt_file = open(filename,"r").readlines()

        s = True

    except:

        try:
            
            txt_file = open(str(filename) + ".txt","r").readlines()

            s = True

        except:

            print("Failed to open file.")

text = []

for line in txt_file:

    a = line.split(",")
    
    text.append(a[0:-1]+[a[-1][0:-1]]) # Remove the \n s from the last items on each line

n = len(text[0])

for line in text[0:-1]:

    if len(line) != n:

        raise("Dimension Error- Matrices must be square")

if len(text) != 2*n+2:

    raise("Dimension Error- Matrices must be of the same size")

m_matrix = np.zeros((n,n))
k_matrix = np.zeros((n,n))
f_vector = np.zeros(n)
omega = 0.0

try:

    for j in range(0,n):

        for i in range(0,n):

            m_matrix[j][i] = float(text[j][i])

    for j in range(n,2*n):

        for i in range(0,n):

            k_matrix[j-n][i] = float(text[j][i])

    for i in range(0,n):

        f_vector[i] = float(text[2*n][i])

    omega = float(text[2*n+1][0])

except:

    raise("All values must be floats/integers")

y_vector = y_amplitudes(m_matrix, k_matrix, omega, f_vector)

clock = pygame.time.Clock()

mass_positions = np.zeros((2,3))

for i in range(0,n):

    mass_positions[i] = np.array([0.0, 2*i, 2*i])

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

    try:
        screen.blit(mass_images[mass_no], [int(50.0*x+350.0), int(600.0-50.0*y)])
    except:
        pass
    
def Spring(x0,y0,x1,y1):

    try:
        pygame.draw.rect(screen,(50,50,50),pygame.Rect(50*x1+361,632-50*y1,10,50*(y1-y0)-31))
    except:
        pass

running = True

t = 0.0

while running:

    screen.fill((140,255,251))
    
    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False

    # Game Code Here
    for i in range(0,len(mass_positions)):

        mass_positions[i] = np.array([0,mass_positions[i][2] + y_vector[i]*np.cos(omega*t), mass_positions[i][2]])

        Mass(mass_positions[i][0],mass_positions[i][1],i)

        if i != 0:

            Spring(mass_positions[i-1][0],mass_positions[i-1][1],mass_positions[i][0],mass_positions[i][1])
        
    pygame.display.update()

    clock.tick(50)
    t += 0.02
    
pygame.display.quit()
pygame.quit()
sys.exit()





