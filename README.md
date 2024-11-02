# AI Pong

## Overview

This is a fun little project I have created in my spare time to familiarize myself with Deep-Q learning networks and Torch library. This is a simple pong game where a player controls a paddle which can be used to bounce the ball and score points. A built-in AI agent can be trained in real time to play the game and later observed.

## Prerequisites

Refer to `requirements.txt` for a comprehensive list of prerequisites used in the virtual environment.

## Usage

- Run the game by using `python main.py` command in the root folder
- Click `Play` if you want to play the game yourself. You can control the paddle with arrow left or arrow right buttons.
- Click `Train` to train a Deep-Q learning network in real time. 
- Click `Observe` to observe a trained agent playing the game. The repository already has a basic agent which is pretty much untrained.

## AI

The AI agent is made from a Deep-Q learning network using python's `torch` library. The way the agent itself is trained is simple reinforcement learning: It gets a reward when the ball bounces from the paddle and gets a punishment when the ball hits the floor below. You can see the setup of the agent in the `ai/dqn.py` script.

## Game

This simple game is created using `pygame`. It's assets(.png) are located in the `assets` folder and game scripts are located in the `game` folder. Both the game and AI agent are structured to work together in the `main.py` script in the root folder.

## Summary

This is a project I used to learn more about Deep-Q neural networks and reinforcement learning with `torch` specifically.

