import pygame

class Score:
    def __init__(self):
        self.score = 0  # Initialize score to zero
        self.font = pygame.font.Font(None, 36)  # Set up font for score display

    def increment(self):
        self.score += 1  # Increment score by 1

    def reset(self):
        self.score = 0  # Reset score to zero

    def draw(self, screen):
        # Render the score text
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        # Display it at the top-left corner of the screen
        screen.blit(score_text, (10, 10))
