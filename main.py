import pygame
import os
import numpy as np
from game.paddle import Paddle
from game.ball import Ball
from game.ceiling import Ceiling
from game.floor import Floor
from game.score import Score
from game.button import Button
from ai.dqn import DQNAgent

pygame.init()

# Constants
GAME_HEIGHT = 800
GAME_WIDTH = 1200
FPS = 60

class PongGame:
    def __init__(self):
        # Initialize the display
        self.screen = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
        pygame.display.set_caption('AI Pong')

        # Load and scale the background image to fit the screen size
        background_image = pygame.image.load(os.path.join(os.path.dirname(__file__), 'assets/background.png'))
        self.background_image = pygame.transform.scale(background_image, (GAME_WIDTH, GAME_HEIGHT))

        # Initialize game objects
        self.paddle = Paddle(GAME_WIDTH // 2, GAME_HEIGHT - 300)
        self.ball = Ball(GAME_WIDTH // 2, GAME_HEIGHT // 5)
        self.ceiling = Ceiling()
        self.floor = Floor(GAME_WIDTH, GAME_HEIGHT)
        self.score = Score()

        # Initialize buttons
        self.play_button = Button(GAME_WIDTH // 2 - 100, GAME_HEIGHT // 3, 200, 50, "Play")
        self.train_button = Button(GAME_WIDTH // 2 - 100, GAME_HEIGHT // 3 + 100, 200, 50, "Train")
        self.observe_button = Button(GAME_WIDTH // 2 - 100, GAME_HEIGHT // 3 + 200, 200, 50, "Observe")
        self.stop_button = Button(1000, 0, 100, 50, "Stop", color=(255, 0, 0), hover_color=(200, 0, 0))

        # Initialize DQN agent
        self.state_size = 6
        self.action_size = 3
        self.agent = DQNAgent(self.state_size, self.action_size)
        self.batch_size = 32

    def reset_game(self):
        """Reset the game state and score."""
        self.ball.rect.topleft = (GAME_WIDTH // 2, GAME_HEIGHT // 5)
        self.ball.velocity = [5, 5]
        self.paddle.rect.topleft = (GAME_WIDTH // 2, GAME_HEIGHT - 300)
        self.score.reset()

    def get_state(self):
        """Return the current game state as a list."""
        return [
            self.paddle.rect.x,
            self.ball.rect.x,
            self.ball.rect.y,
            self.ball.velocity[0],
            self.ball.velocity[1],
            self.paddle.speed
        ]

    def main_menu(self):
        """Display the main menu and handle button interactions."""
        while True:
            self.screen.fill((0, 0, 0))
            self.play_button.draw(self.screen)
            self.train_button.draw(self.screen)
            self.observe_button.draw(self.screen)
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif self.play_button.is_clicked(event):
                    self.play_game(human=True)
                elif self.train_button.is_clicked(event):
                    self.train_agent()
                elif self.observe_button.is_clicked(event):
                    self.agent.load("dqn_model.pth")  # Load trained model
                    self.observe_agent()

    def play_game(self, human=True):
        """Human-controlled gameplay mode."""
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif self.stop_button.is_clicked(event):
                    return  # Exit to main menu

            if human:
                self.paddle.update(GAME_WIDTH)  # Use Paddle's internal control logic

            # Update game state and check collisions
            self.update_game_objects()
            self.draw_game_objects()

            pygame.display.flip()
            clock.tick(FPS)

    def train_agent(self):
        """Train the DQN agent in AI-controlled mode."""
        clock = pygame.time.Clock()
        state = np.array(self.get_state())
        self.agent.epsilon = 1.0  # Enable exploration

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif self.stop_button.is_clicked(event):
                    self.agent.save("dqn_model.pth")  # Save model on stop
                    return  # Exit to main menu

            # Agent action
            action = self.agent.act(state)
            self.apply_action(action)

            # Update game state and train agent
            reward, done = self.update_game_objects(train=True)
            next_state = np.array(self.get_state())
            self.agent.remember(state, action, reward, next_state, done)
            if len(self.agent.memory) > self.batch_size:
                self.agent.replay(self.batch_size)
            state = next_state if not done else np.array(self.get_state())

            self.update_game_objects()
            self.draw_game_objects()

            pygame.display.flip()
            clock.tick(FPS)

    def observe_agent(self):
        """Observe the trained DQN agent playing the game."""
        clock = pygame.time.Clock()
        state = np.array(self.get_state())
        self.agent.epsilon = 0.05  # Minimal exploration

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif self.stop_button.is_clicked(event):
                    return  # Exit to main menu

            action = self.agent.act(state)
            self.apply_action(action)
            self.update_game_objects()
            state = np.array(self.get_state())

            self.draw_game_objects()
            pygame.display.flip()
            clock.tick(FPS)

    def apply_action(self, action):
        """Control paddle based on agent's action."""
        if action == 0:
            self.paddle.rect.x -= self.paddle.speed
        elif action == 1:
            self.paddle.rect.x += self.paddle.speed
        self.paddle.update(GAME_WIDTH)  # Ensure boundary check

    def update_game_objects(self, train=False):
    
        self.paddle.update(GAME_WIDTH)
        self.ball.update()

        reward, done = 0, False

    
        self.paddle.check_collision(self.ball, self.score)

    
        self.ceiling.check_collision(self.ball)  # Ball bounces down if it hits the ceiling
        self.floor.check_collision(self.ball, self.reset_game)  # Ball hits floor, game resets

        if self.ball.rect.colliderect(self.floor.rect):
         reward = -10
         done = True
         self.reset_game()

        if train:
         return reward, done
        return None, None


    def draw_game_objects(self):
        """Draw all game elements on the screen."""
        self.screen.blit(self.background_image, (0, 0))
        self.paddle.draw(self.screen)
        self.ball.draw(self.screen)
        self.ceiling.draw(self.screen)
        self.floor.draw(self.screen)
        self.score.draw(self.screen)
        self.stop_button.draw(self.screen)

# Run the game
game = PongGame()
game.main_menu()
