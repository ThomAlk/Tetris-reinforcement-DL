from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Input, Dense
import tensorflow as tf
from tetris_env import TetrisEnv 
import numpy as np
import random
from collections import deque

print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))
'''
memory = deque(maxlen=1000)

game = TetrisEnv()
game.reset()
state_size = np.prod(game.get_state().shape)
action_size = game.action_space

num_episodes = 10000
epsilon = 1.0         # Start fully random
epsilon_min = 0.1     # Minimum exploration
epsilon_decay = 0.995 # Decay rate

batch_size=32
def train_on_batch(memory, batch_size=32):
    batch = random.sample(memory, batch_size)
    states = []
    targets = []
    gamma = 0.99  # Discount factor

    for state, action, reward, next_state, done in batch:
        state = state.reshape(1, -1)
        next_state = next_state.reshape(1, -1)
        q_values = model.predict(state)
        q_next = model.predict(next_state)
        target = q_values.copy()
        if done:
            target[0, action] = reward
        else:
            target[0, action] = reward + gamma * np.max(q_next)
        states.append(state[0])
        targets.append(target[0])

    states = np.array(states)
    targets = np.array(targets)
    model.train_on_batch(states, targets)

model =Sequential([
    Input(shape=(state_size,)),
    Dense(128, activation='relu'),
    Dense(128, activation='relu'),
    Dense(action_size, activation='linear')
])
model.compile(optimizer='adam', loss='mse')

memory=[]
for episode in range(num_episodes):
    state = game.reset().flatten()
    done = False
    while not done:
        # Epsilon-greedy action selection
        if np.random.rand() < epsilon:
            action = np.random.randint(0, action_size)
        else:
            q_values = model.predict(state.reshape(1, -1))
            action = np.argmax(q_values)
        next_state, reward, done = game.step(action)
        # Store experience in replay buffer
        memory.append((state, action, reward, next_state.flatten(), done))
        # Sample batch and train
        if len(memory) > batch_size:
            train_on_batch(memory, batch_size)
        state = next_state.flatten()
    if epsilon > epsilon_min:
        epsilon *= epsilon_decay
'''