class Agent(object):

    def __init__(self, epsilon=None):
        """Init.

        Args:
            epsilon is optional exploration starting rate
        """
        self.epsilon = epsilon

    def act(self, state, **kwargs):

        raise NotImplementedError()

    def observe(self, state, action, reward, next_state, terminal, *args):
  
        raise NotImplementedError()

    def end(self):

        pass
