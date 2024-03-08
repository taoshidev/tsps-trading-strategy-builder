# Copyright © 2024 Taoshi Inc

from abc import ABC, abstractmethod
from typing import List


class BaseDataGenerator(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def get_data(self, *args):
        pass

    @abstractmethod
    def get_data_and_structure_data_points(self, *args):
        pass

    @staticmethod
    def convert_output_to_data_points(data_structure: List[List], days_data: List[List], order_to_ds: List[int]):
        """
        return close time, close
        """
        for tf_row in days_data:
            data_structure[0].append(int(tf_row[order_to_ds[0]]))
            data_structure[1].append(float(tf_row[order_to_ds[1]]))