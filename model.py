import random


class Model:
    def __init__(self):
        # Initialize the qtable
        # the state has 3 values: the distance to the closest cone, the distance to the second closest cone, and the distance to the third closest cone
        # first action is left, second is right, third is nothing
        self.qtable = [
            [[[0.0, 0.0, 0.0] for i in range(15)] for j in range(15)] for k in range(15)
        ]
        self.alpha = 0.1
        self.gamma = 0.9
        self.epsilon = 0.1
        self.last_state = None
        self.last_action = None
        self.last_reward = None
        self.state = [7, 7, 7]
        self.action = 2

        # if we have a qtable, load it
        try:
            with open("qtable.txt", "r") as f:
                for i in range(15):
                    for j in range(15):
                        for k in range(15):
                            self.qtable[i][j][k] = [
                                float(x) for x in f.readline().split()
                            ]
        except:
            pass

    def get_action(self, state1, state2, state3):
        # state should be the distance from left cone, from 0 to 200
        # We also leave a margin of 200 pixels on each side
        # Then we divide by 40 to get the state
        self.state = [(state1 + 200) // 40, (state2 + 200) // 40, (state3 + 200) // 40]
        # epsilon greedy
        if random.random() < self.epsilon:
            self.action = random.randint(0, 2)
            return self.action
        else:
            self.action = self.qtable[self.state[0]][self.state[1]][
                self.state[2]
            ].index(max(self.qtable[self.state[0]][self.state[1]][self.state[2]]))
            return self.action

    def update(self, reward):
        if self.last_state is not None:
            self.qtable[self.last_state[0]][self.last_state[1]][self.last_state[2]][
                self.last_action
            ] += self.alpha * (
                reward
                + self.gamma
                * max(self.qtable[self.state[0]][self.state[1]][self.state[2]])
                - self.qtable[self.last_state[0]][self.last_state[1]][
                    self.last_state[2]
                ][self.last_action]
            )
        self.last_state = self.state
        self.last_action = self.action
        self.last_reward = reward

    def save_qtable(self):
        with open("qtable.txt", "w") as f:
            for i in range(15):
                for j in range(15):
                    for k in range(15):
                        f.write(" ".join([str(x) for x in self.qtable[i][j][k]]) + "\n")
