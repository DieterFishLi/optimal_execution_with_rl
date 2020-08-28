from abc import abstractmethod

class Env(object):
    '''
    Abstract class for an environment
    '''


    def __init__(self):
        self.data = []

    @abstractmethod
    def step(self, action):
        """Run one timestep of the environment's dynamics.
        Accepts an action and returns a tuple (observation, reward, done, info).

        Args:
            action (numpy.array): action array

        Returns:
            tuple:
                - observation (numpy.array): Agent's observation of the current environment.
                - reward (float) : Amount of reward returned after previous action.
                - done (bool): Whether the episode has ended, in which case further step() calls will return undefined results.
                - info (str): Contains auxiliary diagnostic information (helpful for debugging, and sometimes learning).

        Types of all variable and returns may convert to the corresponding PyTorch types
        """
        pass

    @abstractmethod
    def reset(self):
        pass


    @abstractmethod
    def cal_reward(self):
        pass
