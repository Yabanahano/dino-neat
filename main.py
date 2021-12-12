# Imports
import pygame
import os
import random
import sys
import math
import neat

# ------------------------------------------------------------------------------------------------------- #
# Init PyGame
pygame.init()

# ------------------------------------------------------------------------------------------------------- #
# Window
WIN_HEIGHT = 600
WIN_WIDTH = 1100
WIN = pygame.display.set_mode((
    WIN_WIDTH,
    WIN_HEIGHT
))

# ------------------------------------------------------------------------------------------------------- #
# Picture
DINO_RUN = [
    pygame.image.load(os.path.join("Images", "Dino", "DinoRun1.png")),
    pygame.image.load(os.path.join("Images", "Dino", "DinoRun2.png")),
]
DINO_JUMP = pygame.image.load(os.path.join("Images", "Dino", "DinoJump.png"))

CACTUS_SMALL = [
    pygame.image.load(os.path.join("Images", "Cactus", "SmallCactus1.png")),
    pygame.image.load(os.path.join("Images", "Cactus", "SmallCactus2.png")),
    pygame.image.load(os.path.join("Images", "Cactus", "SmallCactus2.png"))
]

CACTUS_LARGE = [
    pygame.image.load(os.path.join("Images", "Cactus", "LargeCactus1.png")),
    pygame.image.load(os.path.join("Images", "Cactus", "LargeCactus2.png")),
    pygame.image.load(os.path.join("Images", "Cactus", "LargeCactus2.png"))
]

BG = pygame.image.load(os.path.join("Images", "Others", "BG.png"))

# ------------------------------------------------------------------------------------------------------- #
# Font
FONT = pygame.font.Font("freesansbold.ttf", 30)

# ------------------------------------------------------------------------------------------------------- #
# DinoSuck
class DinoSuck:
    X_POS = 80
    Y_POS = 310
    VEL = 8.5

    def __init__(self):
        self.image = DINO_RUN[0]
        self.state = "RUN"
        self.vel = self.VEL
        self.box = pygame.Rect(self.X_POS, self.Y_POS, self.image.get_width(), self.image.get_height())
        self.step = 0
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    
    def update(self):
        if (self.state == "RUN"):
            self.run()
        if (self.state == "JUMP"):
            self.jump()
        if (self.step >= 10):
            self.step = 0

    def jump(self):
        self.image = DINO_JUMP
        if (self.state == "JUMP"):
            self.box.y -= self.vel * 4
            self.vel -= 0.8
        if (self.vel <= -self.VEL):
            self.state = "RUN"
            self.vel = self.VEL

    def run(self):
        self.image = DINO_RUN[self.step // 5]
        self.box.x = self.X_POS
        self.box.y = self.Y_POS
        self.step += 1

    def draw(self, WIN):
        WIN.blit(self.image, (self.box.x, self.box.y))
        pygame.draw.rect(WIN, self.color, (self.box.x, self.box.y, self.box.width, self.box.height), 2)
        for c in cactuds:
            pygame.draw.line(WIN, self.color, (self.box.x + 54, self.box.y + 12), c.box.center, 2)

# ------------------------------------------------------------------------------------------------------- #
# Cactud
class Cactud:
    def __init__(self, img, noc):
        self.image = img
        self.type = noc
        self.box = self.image[self.type].get_rect()
        self.box.x = WIN_WIDTH

    def update(self):
        self.box.x -= speed
        if (self.box.x <= -self.box.width):
            cactuds.pop()
    
    def draw(self, WIN):
        WIN.blit(self.image[self.type], self.box)

class SmallCactud(Cactud):
    def __init__(self, img, noc):
        super().__init__(img, noc)
        self.box.y = 320

class LargeCactud(Cactud):
    def __init__(self, img, noc):
        super().__init__(img, noc)
        self.box.y = 300

# ------------------------------------------------------------------------------------------------------- #
# Functions
def killDino(index): # Kill the too suck dino
    dino.pop(index)
    ge.pop(index)
    nets.pop(index)

def dist(a, b):
    dx = a[0] - b[0]
    dy = a[1] - b[1]
    return math.sqrt(dx**2+dy**2) # Thank you google

# ------------------------------------------------------------------------------------------------------- #
# Main
high_score = 0
def main(genomes, config):
    # Variable
    global speed, x_bg, y_bg, score, dino, cactuds, ge, nets
    clock = pygame.time.Clock()
    score = 0

    dino = []
    cactuds = []
    ge = []
    nets = []

    speed = 20
    x_bg = 0
    y_bg = 380

    # Genomes
    for g_id, g in genomes:
        dino.append(DinoSuck())
        ge.append(g)
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        g.fitness = 0

    # Functions
    def updateScore():
        global score, speed, high_score
        score += 1
        if (math.floor(score % 100) == 0):
            speed += 1
        if (score > high_score):
            high_score = score
        textScore = FONT.render("Score: " + str(math.floor(score)), True, (0, 0, 0))
        textHighScore = FONT.render("High Score: " + str(math.floor(high_score)), True, (0, 0, 0))
        WIN.blit(textScore, (900, 20))
        WIN.blit(textHighScore, (825, 60))

    def updateStats():
        global dino, speed, ge
        textAlive = FONT.render("Alive: " + str(len(dino)), True, (0, 0, 0))
        textGen = FONT.render("Gen: " + str(pop.generation + 1), True, (0, 0, 0))
        textSpeed = FONT.render("Speed: " + str(speed), True, (0, 0, 0))
        WIN.blit(textAlive, (50, 20))
        WIN.blit(textGen, (50, 60))
        WIN.blit(textSpeed, (225, 20))

    
    def bg():
        global  x_bg, y_bg
        img_width = BG.get_width()
        WIN.blit(BG, (x_bg, y_bg))
        WIN.blit(BG, (img_width + x_bg, y_bg))
        if (x_bg <= -img_width):
            x_bg = 0
        x_bg -= speed

    # Main
    run = True
    while run:
        # If Quit
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
        # Draw BG
        WIN.fill((255, 255, 255))

        # Dino
        for d in dino:
            d.update()
            d.draw(WIN)

        # Check Len Of Dino And Cactud
        if (len(dino) == 0):
            if (pop.best_genome):
                print(pop.best_genome)
            break
            
        if (len(cactuds) == 0):
            rand = random.randint(0, 1)
            if (rand == 0):
                rand = random.randint(0, 5)
                cactuds.append(SmallCactud(CACTUS_SMALL, random.randint(0, 2)))
            else:
                cactuds.append(SmallCactud(CACTUS_LARGE, random.randint(0, 2)))

        # Cactud
        for c in cactuds:
            c.update()
            c.draw(WIN)
            for i, d in enumerate(dino):
                if d.box.colliderect(c.box):
                    ge[i].fitness += 1
                    killDino(i)
        
        # Ahhh
        for i, d in enumerate(dino):
            output = nets[i].activate((d.box.y,
                dist((d.box.x, d.box.y), c.box.midtop)
            ))
            if (output[0] > 0.5 and d.box.y == d.Y_POS):
                d.state = "JUMP"

        # IDK
        updateStats()
        updateScore()
        bg()
        clock.tick(30)
        pygame.display.update()
# ------------------------------------------------------------------------------------------------------- #
# Run
def run(path):
    global pop
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, path)
    pop = neat.Population(config)
    pop.run(main, 50)

# ------------------------------------------------------------------------------------------------------- #
if (__name__ == "__main__"):
    dir = os.path.dirname(__file__)
    path = os.path.join(dir, "config.txt")
    run(path)