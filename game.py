import pygame
import random
from collections import defaultdict
import numpy as np

from bird import Bird
from pipe import Pipe


class Game:
    def __init__(self, ai=True):
        self.ai = ai

        pygame.init()
        self.window_width = 300
        self.window_height = 400
        self.window = pygame.display.set_mode(
            (self.window_width, self.window_height))
        pygame.display.set_caption("Flappy Bird")

        self.bird_radius = 20
        self.gravity = 0.05
        self.jump_velocity = -2.0
        self.start_x = 25

        self.gap = 100
        self.pipe_width = 30
        self.min_pipe_height = 50
        self.pipe_velocity = 1

        self.reset_game()  # Initialize the bird and pipes

        self.score = 0
        self.max_score = 0
        self.game_over = False

        self.FPS = 120
        self.clock = pygame.time.Clock()
        self.time_elapsed = 0
        self.font = pygame.font.Font(None, 36)

        self.actions = [0, 1]  # 0: Do nothing, 1: Jump
        self.q_table = defaultdict(lambda: [0, 0])

        self.discount_factor = 0.8
        self.epsilon = 0  # Exploration rate
        self.learning_rate = 0.2

    def choose_action(self, state):
        if np.random.rand() < self.epsilon and self.time_elapsed > 1:
            self.time_elapsed = 0
            # Explore: choose a random action
            return np.random.choice([0, 1], p=[0.75, 0.25])
        else:
            # Exploit: choose the best known action for this state
            return np.argmax(self.q_table[state])

    def learn(self, old_state, new_state, action, reward):
        # Update Q-table
        old_value = self.q_table[old_state][action]
        max_new_value = max(self.q_table[new_state])
        new_value = old_value + self.learning_rate * \
            (reward + self.discount_factor * max_new_value - old_value)
        self.q_table[old_state][action] = new_value

    def get_current_state(self):
        x = int(self.bottom_pipe.rect.x - self.bird.rect.centerx)
        y = int(self.bottom_pipe.rect.y - self.bird.rect.centery)
        return (x, y, +self.game_over)

    def get_reward(self, new_state, action):
        if self.game_over:  # Game over
            return -100
        if new_state[0] < 0:  #  Passed the pipe
            return 10
        if new_state[1] < self.bird_radius and action == 0 or new_state[1] < self.gap - self.bird_radius and action == 1:  # Wrong action
            return -1
        return 1

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN and not self.ai:
                if event.key == pygame.K_SPACE:
                    self.bird.velocity = self.jump_velocity
        return True

    def is_over(self):
        if self.bird.rect.colliderect(self.top_pipe.rect) or self.bird.rect.colliderect(self.bottom_pipe.rect):
            return True
        if self.bird.rect.colliderect(self.temp_top_pipe.rect) or self.bird.rect.colliderect(self.temp_bottom_pipe.rect):
            return True
        if self.bird.rect.y < 0 or self.bird.rect.y > self.window_height:
            return True
        return False

    def update(self):
        if not self.ai:  # Human player
            self.bird.update()
            self.top_pipe.update()
            self.bottom_pipe.update()
            self.temp_top_pipe.update()
            self.temp_bottom_pipe.update()

            self.game_over = self.is_over()
        else:  # AI player
            old_state = self.get_current_state()

            action = self.choose_action(old_state)
            if action == 1:
                self.bird.velocity = self.jump_velocity

            self.bird.update()
            self.top_pipe.update()
            self.bottom_pipe.update()
            self.temp_top_pipe.update()
            self.temp_bottom_pipe.update()

            new_state = self.get_current_state()

            self.game_over = self.is_over()

            reward = self.get_reward(new_state, action)

            self.learn(old_state, new_state, action, reward)

        if self.bird.rect.x > self.bottom_pipe.rect.x:
            self.score += 1
            self.max_score = max(self.score, self.max_score)
            self.reset_pipe_positions()

        if self.temp_bottom_pipe.rect.x + self.pipe_width < 0:
            self.temp_top_pipe.rect.x = self.top_pipe.rect.x
            self.temp_top_pipe.rect.height = self.top_pipe.rect.height
            self.temp_bottom_pipe.rect.x = self.bottom_pipe.rect.x
            self.temp_bottom_pipe.rect.height = self.bottom_pipe.rect.height
            self.temp_bottom_pipe.rect.y = self.bottom_pipe.rect.y

        return True

    def reset_pipe_positions(self):
        self.top_pipe.rect.x = self.window_width
        self.top_pipe.rect.height = self.random_pipe_height()

        self.bottom_pipe.rect.x = self.window_width
        self.bottom_pipe.rect.height = self.window_height - \
            (self.top_pipe.rect.height + self.gap)
        self.bottom_pipe.rect.y = self.top_pipe.rect.height + self.gap

    def random_pipe_height(self):
        return random.randint(self.min_pipe_height, self.window_height - self.gap - self.min_pipe_height)

    def reset_game(self):
        self.bird = Bird(50, self.window_height // 2,
                         self.bird_radius, 0, self.gravity)
        self.top_pipe = Pipe(self.window_width, 0, self.pipe_width,
                             self.random_pipe_height(), self.pipe_velocity)
        self.bottom_pipe = Pipe(self.window_width, self.top_pipe.rect.height + self.gap, self.pipe_width,
                                self.window_height - (self.top_pipe.rect.height + self.gap), self.pipe_velocity)
        self.temp_top_pipe = Pipe(
            self.window_width, 0, self.pipe_width, self.top_pipe.rect.height, self.pipe_velocity)
        self.temp_bottom_pipe = Pipe(self.window_width, self.top_pipe.rect.height + self.gap, self.pipe_width,
                                     self.window_height - (self.top_pipe.rect.height + self.gap), self.pipe_velocity)
        self.score = 0

    def draw(self):
        self.window.fill("black")
        self.bird.draw(self.window)

        self.top_pipe.draw(self.window, "red")
        self.bottom_pipe.draw(self.window, "red")

        self.temp_top_pipe.draw(self.window, "red")
        self.temp_bottom_pipe.draw(self.window, "red")

        score_text = self.font.render(
            "Score: " + str(self.score), True, "white")
        max_score_text = self.font.render(
            "Max Score: " + str(self.max_score), True, "white")

        if self.ai:
            y = int(abs(self.bird.rect.centery - self.bottom_pipe.rect.y))
            if self.bird.rect.centery > self.bottom_pipe.rect.y:
                y *= -1
            pygame.draw.line(self.window, "lightgreen", (self.bird.rect.centerx,
                            self.bird.rect.centery + y), (self.bottom_pipe.rect.x, self.bottom_pipe.rect.y), 2)
            pygame.draw.line(self.window, "lightblue", (self.bird.rect.centerx,
                            self.bird.rect.centery), (self.bird.rect.centerx, self.bird.rect.centery + y), 2)

        self.window.blit(score_text, (10, 10))
        self.window.blit(max_score_text, (10, 35))
        pygame.display.update()

    def run(self):
        running = True
        iteration = 1
        while running:
            if self.game_over:
                print(iteration, "score:", self.score)
                iteration += 1
                self.reset_game()
                self.game_over = False

            running = self.handle_events()
            self.update()
            self.draw()
            self.time_elapsed += self.clock.tick(self.FPS) / 1000
