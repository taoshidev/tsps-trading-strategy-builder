# Copyright © 2024 Taoshi Inc

from datetime import datetime
from typing import List, Tuple

import requests
from requests import Response
import time

from data_generator.base_data_generator import \
    BaseDataGenerator


class BinanceDataGenerator(BaseDataGenerator):
    def __init__(self):
        super().__init__()

    def get_data(self,
                 symbol,
                 interval,
                 start,
                 end,
                 limit=1000,
                 retries=0) -> Response:

        url = f'https://api.binance.com/api/v3/klines?symbol={symbol}' \
              f'&interval={interval}&startTime={start}&endTime={end}&limit={limit}'

        response = requests.get(url)

        try:
            if response.status_code == 200:
                return response
            else:
                raise Exception("received error status code")
        except Exception:
            if retries < 5:
                time.sleep(retries)
                retries += 1
                # print("retrying getting historical binance data")
                self.get_data(symbol, interval, start, end, limit, retries)
            else:
                raise ConnectionError("max number of retries exceeded trying to get binance data")

    def get_data_and_structure_data_points(self, symbol: str, interval: str, data_structure: List[List], ts_range: Tuple[int, int]):
        bd = self.get_data(symbol=symbol, interval=interval, start=ts_range[0], end=ts_range[1]).json()
        if "msg" in bd:
            raise Exception("error occurred getting Binance data, please review", bd["msg"])
        else:
            # print("received binance historical data from : ", TimeUtil.millis_to_timestamp(ts_range[0]),
            #       TimeUtil.millis_to_timestamp(ts_range[1]))
            self.convert_output_to_data_points(data_structure,
                                               bd,
                                               [0, 4]
                                               )