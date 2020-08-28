from keras.layers import Dense
from keras.models import Sequential, Model
from keras.optimizers import RMSprop
import numpy as np
from agent import agent

class Buffer:
    def __init__(self, size=256):
        self.size = size
        self.buffer = []

    # state, action, reward, next_state, terminal
    def add(self, state, action, reward, next_state, terminal):
        # [last_state, action, next_state, reward]
        if len(self.buffer) < self.size:
            self.buffer.append([state, action, reward, next_state, terminal])
        elif len(self.buffer) < self.size:
            to_delete = np.random.randint(0, self.size//2)
            self.buffer.pop(to_delete)
            self.buffer.append([state, action, reward, next_state, terminal])

    def sample(self, batch_size):
        return np.random.choice(self.buffer, batch_size, replace=False)





class DDQNAgent(agent.Agent):

    def __init__(self, batch_size, state_size, buffer_size, update_frequency):

        super(DDQNAgent).__init__()
        self.main_network = self._model()
        self.target_network = None
        self.batch_size = batch_size
        self.buffer = Buffer(buffer_size)
        self.state_size = state_size
        self.count = 0 #计数器
        self.update_frequency = update_frequency

    def _model(self):
        model = Sequential()
        neurons_per_layers = 20
        activation = 'relu'
        """Input & output size need to be modified"""
        # input layer
        model.add(Dense(neurons_per_layers, input_shape= (self.batch_size, self.state_size + 1), activation=activation))

        model.add(Dense(neurons_per_layers, activation=activation))
        model.add(Dense(neurons_per_layers, activation=activation))
        model.add(Dense(neurons_per_layers, activation=activation))
        model.add(Dense(neurons_per_layers, activation=activation))
        model.add(Dense(neurons_per_layers, activation=activation))
        model.add(Dense(neurons_per_layers, activation=activation))

        model.add(Dense(units=1,)) # output layer
        model.compile(loss='mse', optimizer=RMSprop)
        return model

    def act(self, state, test=False):
        # state(inventory left, cur time)
        inventory_left = state[...]
        time_left = 4 - state[...]
        """Epsilon Greedy"""
        if time_left == 0:
            action = inventory_left

        else:
            if np.random.rand() <= self.epsilon and not test:
                """随机选一个"""
                action = np.random.binomial(n=inventory_left, p=1/time_left)
            else:
                action_available = range(inventory_left+1) # [0, 1, 2, 3, 4, 5....,inventory_left]
                state_action = state.reshape(1, self.state_size)

                action = ...

        act_values = self.main_network.predict(state_action)

        if test:
            return action
        else:
            return action, act_values

    def update_target_network(self):
        self.target_network.set_weights(self.main_network.get_weights())



    def observe(self, state, action, reward, next_state, terminal, ):
        """
        Training procedure
        :param state:
        :param action:
        :param reward:
        :param next_state:
        :param terminal:
        :param pretraining:
        :return:
        """


        return self.main_network.fit(x=...,y=..., batch_size=..., epochs=..., verbose=False, validation_split=0.1)



    def _get_batches(self,):
        batch =  self.buffer.sample(self.batch_size)
        state_batch = np.concatenate(batch[:, 0]).reshape(self.batch_size, self.state_size)
        action_batch = np.concatenate(batch[:, 1]).reshape(self.batch_size, self.state_size)
        reward_batch = np.concatenate(batch[:, 2]).reshape(self.batch_size, self.state_size)
        next_batch = np.concatenate(batch[:, 3]).reshape(self.batch_size, self.state_size)
        done_batch = batch[:, 4]

        return state_batch, action_batch, reward_batch, next_batch, done_batch

