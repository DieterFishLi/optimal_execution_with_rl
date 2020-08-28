import datetime
import math
import os
from collections import deque
from collections import namedtuple
import pandas as pd
import time

_COLUMNS = ['TradingTime', 'SellPrice05',
            'SellPrice04', 'SellPrice03', 'SellPrice02', 'SellPrice01',
            'BuyPrice01', 'BuyPrice02', 'BuyPrice03', 'BuyPrice04', 'BuyPrice05',
            'SellVolume05', 'SellVolume04', 'SellVolume03', 'SellVolume02','SellVolume01',
            'BuyVolume01', 'BuyVolume02', 'BuyVolume03','BuyVolume04', 'BuyVolume05', 'LastPrice']

interval = namedtuple('interval', ('start', 'end'))
_TRADINGHOURS = {
    '10': interval('10:00:00', '11:00:00'),
    '13': interval('13:00:00', '14:00:00'),
}


def inverntory_action_transform(x, q, q0):
    q_hat, x_hat = q / q0 - 1, x / q0

    r = math.sqrt(q_hat ** 2 + x_hat ** 2)
    zeta = - (x_hat / q_hat) if not q_hat == 0 else float('inf')
    theta = math.atan(zeta)

    if theta <= math.pi / 4:
        r_tilt = r * (math.sqrt(
            (
                    math.pow(zeta, 2) + 1
            ) *
            (
                    2 * math.pow(
                math.cos(
                    math.pi / 4 - theta
                ),
                2
            )
            )
        ))
    else:
        r_tilt = r * (math.sqrt(
            (
                    math.pow(zeta, -2) + 1
            ) *
            (
                    2 * math.pow(
                math.cos(
                    - math.pi / 4 + theta
                ),
                2
            )
            )
        ))

    q_tilt = -r_tilt * math.cos(theta)
    x_tilt = r_tilt * math.sin(theta)
    return x_tilt, q_tilt


def quadratic_variation(dataframe):
    return dataframe


def midprice(dataframe):
    return dataframe


def data_preprocess(filepath, tradinghour):
    df = pd.read_hdf(filepath).filter(items=_COLUMNS)
    df['TradingTime'] = pd.to_datetime(df['TradingTime'])
    period = _TRADINGHOURS[tradinghour]
    _minus_one = df[df['TradingTime'].dt.strftime("%H:%M:%S") < period.start].iloc[-1]
   # _plus_one = df[df['TradingTime'].dt.strftime("%H:%M:%S") > period.end].iloc[0]

    df = df[df['TradingTime'].dt.strftime("%H:%M:%S").between(*period)].reset_index(drop=True)
    first_timestamp = df['TradingTime'].iloc[0]

    df = pd.concat([pd.DataFrame(_minus_one.to_dict(), index=[0]), df, ],ignore_index=True)
    df['minutes_group'] = (df['TradingTime'] - first_timestamp).dt.seconds // (60*15)
    df.loc[0,'minutes_group'] = -1
    return (bar for _, bar in df.groupby('minutes_group'))


class DataStreamer:
    trading_calender = pd.read_hdf('tradingdate.h5')

    def __init__(self, code, start, end, tradinghour, **kwargs):
        self.filelist = deque(self.generate_periods(start, end, code))
        self.start = start
        self.end = end
        self.code = code
        self.tradinghour = tradinghour

    def is_tradingdate(self, curdate):
        return DataStreamer.trading_calender[pd.to_datetime(DataStreamer.trading_calender['tradingdate']) == pd.to_datetime(curdate)].empty

    def generate_periods(self, start, end, code):
        result = []
        curdate = start
        while curdate <= end:
            if self.is_tradingdate(curdate):
                curdate = curdate + datetime.timedelta(days=1)
                continue
            file_path = os.path.join(r'..\tick', code, curdate.strftime('%Y%m%d') + '.h5')
            if os.path.exists(file_path):
                result.append(file_path)
            curdate = curdate + datetime.timedelta(days=1)
        return result

    def get_trading_list(self):
        return self.filelist

    def get_next(self):
        cur = self.filelist.popleft()
        self.filelist.append(cur)
        df = data_preprocess(cur, self.tradinghour)
        return df


if __name__ == '__main__':
    start = datetime.date(year=2019, month=6, day=1)
    end = datetime.date(year=2020, month=1, day=1)
    test_data = DataStreamer('000001.SZ', start, end, '10').get_next()
    print(next(test_data))
    print(next(test_data))

