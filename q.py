import pickle
from collections import defaultdict


class Q:
    def __init__(self, actions, default_value=0, discount_factor=0.8, learning_rate=0.2, load=False):
        self.q_table = None
        self.actions = actions
        self.default_value = default_value
        if load:
            self.load_q_table()
        else:
            self.q_table = defaultdict(
                lambda: [self.default_value for _ in range(len(self.actions))])

        self.discount_factor = discount_factor
        self.learning_rate = learning_rate

    def update_q_table(self, old_state, new_state, action, reward):
        old_value = self.q_table[old_state][action]
        max_new_value = max(self.q_table[new_state])
        new_value = old_value + self.learning_rate * \
            (reward + self.discount_factor * max_new_value - old_value)
        self.q_table[old_state][action] = new_value

    def save_q_table(self):
        with open("q_table.pkl", "wb") as f:
            pickle.dump(dict(self.q_table), f)

    def load_q_table(self):
        with open("q_table.pkl", "rb") as f:
            self.q_table = defaultdict(
                lambda: [self.default_value for _ in range(len(self.actions))], pickle.load(f))
