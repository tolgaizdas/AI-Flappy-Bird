import pygame


class Bird:
    def __init__(self, x, y, radius, velocity, gravity):
        self.radius = radius
        self.rect = pygame.Rect(x, y, self.radius, self.radius)

        self.velocity = velocity
        self.gravity = gravity

    def update(self):
        self.rect.y += self.velocity
        self.velocity += self.gravity

    def draw(self, window, color="white"):
        pygame.draw.ellipse(window, color, self.rect, self.radius)
