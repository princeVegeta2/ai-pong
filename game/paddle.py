import pygame
import os

class Paddle:
    def __init__(self, x, y):
        # Load the paddle image
        self.image = pygame.image.load(os.path.join(os.path.dirname(__file__), '../assets/paddle2.png'))
        
        # Scale the image
        new_width = int(self.image.get_width())  
        new_height = int(self.image.get_height())  
        self.image = pygame.transform.scale(self.image, (new_width, new_height))

        # Update the rect to match the scaled image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        # Speed for moving the paddle
        self.speed = 5

    def update(self, game_width):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

        # Boundary checks to prevent paddle from going out of bounds
        if self.rect.left < 0:  # Prevent going beyond the left edge
            self.rect.left = 0
        if self.rect.right > game_width:  # Prevent going beyond the right edge
            self.rect.right = game_width

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def check_collision(self, ball, score):
        if self.rect.colliderect(ball.rect):
            # Ball hits the top of the paddle
            if ball.rect.bottom >= self.rect.top and ball.rect.centery < self.rect.top:
                ball.velocity[1] = -abs(ball.velocity[1])  # Reverse vertical direction (up)
                score.increment()  # Increment the score

            # Ball hits the left side of the paddle
            elif ball.rect.right >= self.rect.left and ball.rect.centerx < self.rect.left:
                ball.velocity[0] = -abs(ball.velocity[0])  # Move ball to the left

            # Ball hits the right side of the paddle
            elif ball.rect.left <= self.rect.right and ball.rect.centerx > self.rect.right:
                ball.velocity[0] = abs(ball.velocity[0])  # Move ball to the right

    def draw_collision(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)  # Red rectangle around the object
