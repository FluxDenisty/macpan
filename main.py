from pygame import draw
import pygame
import sys

WIDTH = 17
HEIGHT = 19
DELAY = 0

pygame.init()

# GRID[ Y ][ X ]


class Player:
    pass


class Macpan:

    clock = pygame.time.Clock()
    cmd = False
    SIZE = 30
    SPEED = 4

    def __init__(self):
        self.width = 0
        self.height = 0
        self.importMap("map.txt")

        self.player = Player()
        self.player.x = 9
        self.player.y = 12
        self.player.vx = 0
        self.player.vy = 0

        self.window = pygame.display.set_mode(
            (self.width * self.SIZE, self.height * self.SIZE))
        pygame.display.set_caption('Macpan')

    def input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LSUPER or event.key == pygame.K_RSUPER:
                    self.cmd = True
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_a:
                    self.player.vx = -self.SPEED
                elif event.key == pygame.K_d:
                    self.player.vx = self.SPEED
                elif event.key == pygame.K_w:
                    self.player.vy = -self.SPEED
                elif event.key == pygame.K_s:
                    self.player.vy = self.SPEED
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LSUPER or event.key == pygame.K_RSUPER:
                    self.cmd = False

    def draw(self):
        SIZE = self.SIZE
        blue = pygame.Color("blue")
        yellow = pygame.Color("yellow")
        black = pygame.Color("black")
        self.window.fill(pygame.Color("white"))
        for y, row in enumerate(self.grid):
            for x, sq in enumerate(row):
                if sq is False:
                    box = (x * SIZE, y * SIZE, SIZE, SIZE)
                    draw.rect(self.window, blue, box, 0)
        pos = (self.player.x * SIZE, self.player.y * SIZE)
        pos = (int(pos[0] + SIZE / 2), int(pos[1] + SIZE / 2))
        draw.circle(self.window, yellow, pos, int(SIZE / 2 * 0.8), 0)
        draw.circle(self.window, black, pos, int(SIZE / 2 * 0.8), 1)

    def importMap(self, name="map.txt"):
        grid = []
        for line in open("./" + name):
            grid.append([])
            for char in line[:-1]:
                grid[-1].append(char == '.')

        self.width = len(grid[0])
        self.height = len(grid)
        self.grid = grid

    def update(self, diff):
        w = self.width
        h = self.height

        self.player.x += self.player.vx * diff
        self.player.y += self.player.vy * diff

        if (self.player.x < 0):
            self.player.x = w + self.player.x
        elif (self.player.x > w):
            self.player.x = self.player.x - w

        if (self.player.y < 0):
            self.player.y = h + self.player.y
        elif (self.player.y > h):
            self.player.y = self.player.y - h

        x = int(round(self.player.x))
        y = int(round(self.player.y))
        if (self.grid[(y - 1) % h][x % w] is False and self.player.y < y):
            self.player.y = max(y, self.player.y)
        elif (self.grid[(y + 1) % h][x % w] is False and self.player.y > y):
            self.player.y = min(y, self.player.y)
        if (self.grid[y % h][(x - 1) % w] is False and self.player.x < x):
            self.player.x = max(x, self.player.x)
        elif (self.grid[y % h][(x + 1) % w] is False and self.player.x > x):
            self.player.x = min(x, self.player.x)

    def run(self):
        while True:
            self.input()

            self.update(1.0 / 60.0)
            self.draw()
            pygame.display.update()
            self.clock.tick(60)

game = Macpan()
game.run()
