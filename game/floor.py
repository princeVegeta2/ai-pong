import pygame
import os

class Floor:
    def __init__(self, game_width, game_height):
        # Load and resize floor image (reduce height by 50%)
        self.image = pygame.image.load(os.path.join(os.path.dirname(__file__), '../assets/floor.png'))
        new_width = self.image.get_width()
        new_height = int(self.image.get_height() * 0.5)  # 50% of the original height
        self.image = pygame.transform.scale(self.image, (new_width, new_height))

        # Update the rect to match the scaled image
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, game_height - new_height)  # Position the floor at the bottom

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def check_collision(self, ball, reset_game_callback):
        if self.rect.colliderect(ball.rect):
            reset_game_callback()  # Call the reset function when the ball hits the floor

    def draw_collision(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)  # Red rectangle around the object
