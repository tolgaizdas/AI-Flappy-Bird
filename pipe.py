import pygame


class Pipe:
    def __init__(self, x, y, width, height, velocity):
        self.rect = pygame.Rect(x, y, width, height)
        self.velocity = velocity

    def update(self):
        self.rect.x -= self.velocity

    def draw(self, window, color="white"):
        pygame.draw.rect(window, color, self.rect)
