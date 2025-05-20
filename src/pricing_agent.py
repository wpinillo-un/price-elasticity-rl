import numpy as np
from keras.models import Sequential # type: ignore
from keras.layers import Dense # type: ignore
from keras.optimizers import Adam # type: ignore
import random

class PricingAgent:
    def __init__(self, state_size, action_size, epsilon=0.1):
        self.state_size = state_size
        self.action_size = action_size
        self.discount_factor = 0.99
        self.learning_rate = 0.001
        self.epsilon = epsilon  # Exploration rate (epsilon)
        self.epsilon_min = 0.01  # Minimum epsilon value for exploration
        self.epsilon_decay = 0.995  # Decay rate for epsilon
        self.model = self.build_model()
        self.states, self.actions, self.rewards = [], [], []

    def build_model(self):
        model = Sequential()
        model.add(Dense(24, input_dim=self.state_size, activation='relu'))
        model.add(Dense(24, activation='relu'))
        model.add(Dense(self.action_size, activation='softmax'))
        model.compile(loss='categorical_crossentropy', optimizer=Adam(lr=self.learning_rate))
        return model

    def get_action(self, state):
        # Epsilon-Greedy: Choose action based on epsilon-greedy policy
        if np.random.rand() <= self.epsilon:
            # Random action (exploration)
            return np.random.choice(self.action_size)
        else:
            # Best action based on policy (exploitation)
            policy = self.model.predict(state, batch_size=1).flatten()
            return np.random.choice(self.action_size, 1, p=policy)[0]

    def discount_rewards(self, rewards):
        discounted_rewards = np.zeros_like(rewards)
        running_add = 0
        for t in reversed(range(0, len(rewards))):
            running_add = running_add * self.discount_factor + rewards[t]
            discounted_rewards[t] = running_add
        return discounted_rewards

    def append_sample(self, state, action, reward):
        self.states.append(state)
        self.rewards.append(reward)
        self.actions.append(action)

    def train_model(self):
        episode_length = len(self.states)
        discounted_rewards = self.discount_rewards(self.rewards)
        discounted_rewards -= np.mean(discounted_rewards)
        discounted_rewards /= np.std(discounted_rewards)

        update_inputs = np.zeros((episode_length, self.state_size))
        advantages = np.zeros((episode_length, self.action_size))

        for i in range(episode_length):
            update_inputs[i] = self.states[i]
            advantages[i][self.actions[i]] = discounted_rewards[i]

        # Train the model using the advantages
        self.model.fit(update_inputs, advantages, epochs=1, verbose=0)
        
        # Decay epsilon after each training step to gradually reduce exploration
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
        
        # Clear memory
        self.states, self.actions, self.rewards = [], [], []


