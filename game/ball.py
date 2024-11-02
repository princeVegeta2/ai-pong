import pygame
import os

class Ball:
    def __init__(self, x, y):
        # Load and resize ball image (scale down by 50%)
        self.image = pygame.image.load(os.path.join(os.path.dirname(__file__), '../assets/ball2.png'))
        new_width = self.image.get_width() // 2
        new_height = self.image.get_height() // 2
        self.image = pygame.transform.scale(self.image, (new_width, new_height))

        # Update the rect to match the scaled image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        

        # Ball velocity
        self.velocity = [5, 5]

    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

        # Check for collisions with the walls
        if self.rect.left <= 0 or self.rect.right >= 1200:  # Adjust for screen width
            self.velocity[0] = -self.velocity[0]
        if self.rect.top <= 0 or self.rect.bottom >= 800:  # Adjust for screen height
            self.velocity[1] = -self.velocity[1]

    def draw(self, screen):
        screen.blit(self.image, self.rect)
    
    def draw_collision(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)  # Red rectangle around the object

