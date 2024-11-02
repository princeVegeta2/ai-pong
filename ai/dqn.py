import torch
import torch.nn as nn
import torch.optim as optim
import random
import numpy as np
from collections import deque

class DQNAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=2000)  # Replay memory
        self.gamma = 0.95  # Discount factor
        self.epsilon = 1.0  # Exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        self.model = self._build_model()
        self.optimizer = optim.Adam(self.model.parameters(), lr=self.learning_rate)

    def _build_model(self):
        # Define a simple neural network
        model = nn.Sequential(
            nn.Linear(self.state_size, 24),
            nn.ReLU(),
            nn.Linear(24, 24),
            nn.ReLU(),
            nn.Linear(24, self.action_size)
        )
        return model

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)  # Exploration
        state = torch.FloatTensor(state).float()  # Convert to FloatTensor
        act_values = self.model(state)
        return torch.argmax(act_values).item()  # Exploitation

    def replay(self, batch_size):
        if len(self.memory) < batch_size:
            return
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            state = torch.FloatTensor(state).float()  # Ensure FloatTensor
            next_state = torch.FloatTensor(next_state).float()  # Ensure FloatTensor
            target = reward
            if not done:
                target = reward + self.gamma * torch.max(self.model(next_state)).item()
            target_f = self.model(state).detach().clone()
            target_f[action] = target
            self.model.zero_grad()
            output = self.model(state).float()
            loss = nn.MSELoss()(output[action], torch.tensor(target, dtype=torch.float32))  # Convert target to float
            loss.backward()
            self.optimizer.step()
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
    
    # In dqn.py
    def save(self, filename="dqn_model.pth"):
     torch.save(self.model.state_dict(), filename)

    def load(self, filename="dqn_model.pth"):
     self.model.load_state_dict(torch.load(filename))
     self.model.eval()  # Set to evaluation mode for inference


