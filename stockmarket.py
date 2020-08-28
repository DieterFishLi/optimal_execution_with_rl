import pandas as pd
from enviroment import datastream
import datetime

class MarketSimulator:
    '''
    A Naive trding environment.
    '''

    def __init__(self, code, start, end, tradinghour, inventory, mode, penalty,**kwargs):
        self.datasrc = datastream.DataStreamer(code, start, end, tradinghour)
        self.data_gen()

        self.done = False
        self.mode = mode
        self.count = 0
        self.inventory = inventory
        self.cur_state = None

        self.penalty = penalty

    def data_gen(self):
        self.cur_day = self.datasrc.get_next()
        self.prv_tick = next(self.cur_day)
        self.bar = next(self.cur_day)

    def step(self, action, termialQ=False):
        '''
        return [s, x, s^{s,x}, r] will be store in the Replay Buffer

        s^{s, x} is the next state given the last state s and acton x.

        r is the reward of state s and action x

        '''
        self.inventory -= action
        self.count += 1

        if self.count % 4 == 0:
            terminalQ = True
        else:
            terminalQ = False

        last_state = self.cur_state
        reward = self.cal_reward(action)
        # if not terminalQ:
        #     # reward = self._reward(self.cur_state, action)
        #     ...
        # else:
        #     '''last period; termial cases'''
        #     reward = self._reward(action)
        #     self.cur_day = self.datasrc.get_next()

        self.bar = next(self.cur_day)
        self.cur_state = self.bar.iloc[0]

        items = {
            'last_state': last_state,
            'action': action,
            'next_state':self.cur_state,
            'reward': reward,
            'termial':terminalQ
        }
        return items # [last_state, action, self.cur_state, reward, terminalQ,]

    def get_observation(self):
        self.cur_state = self.bar.iloc[0]
        return self.cur_state

    def cal_reward(self, action):
        '''
        action: int. the lots of shares that to be traded in this episode. 0 <= action <= q_t, the inventory left
        Over each period, we assume the agent sends orders at a constant rate,
        so that when the trader makes a decision at time Tk to
        send xTk orders over the next period, the actual trades are made of xTk/Mk equal trades every
        second.

        :param data:
        :param action:
        :return:
        '''

        num_ticks = len(self.bar) - 1
        trd_per_tick = action * 10000 // num_ticks
        remaining_invertorys = [self.inventory * 10000 - (i+1)*trd_per_tick for i in range(num_ticks)]
        prices_diff = self.bar['LastPrice'].diff().dropna()
        intra_reward = (remaining_invertorys*prices_diff - self.penalty*trd_per_tick**2).sum()
        return intra_reward





if __name__ == '__main__':
    #code, start, end, tradinghour, inventory, mode, ** kwargs):
    start = datetime.date(year=2019, month=6, day=1)
    end = datetime.date(year=2020, month=1, day=1)
    s = MarketSimulator('000001.SZ', start, end, '10', 20, 'Train', 0.001)
    s.get_observation()
    print(s.step(5))



