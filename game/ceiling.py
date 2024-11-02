import pygame
import os

class Ceiling:
    def __init__(self):
        # Load and resize ceiling image (reduce height by 50%)
        self.image = pygame.image.load(os.path.join(os.path.dirname(__file__), '../assets/ceiling.png'))
        new_width = self.image.get_width()
        new_height = int(self.image.get_height() * 0.5)  # 50% of the original height
        self.image = pygame.transform.scale(self.image, (new_width, new_height))

        # Update the rect to match the scaled image
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)  # Position the ceiling at the top

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def check_collision(self, ball):
        if self.rect.colliderect(ball.rect):
            ball.velocity[1] = -ball.velocity[1]  # Reverse vertical direction
    
    def draw_collision(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)  # Red rectangle around the object
