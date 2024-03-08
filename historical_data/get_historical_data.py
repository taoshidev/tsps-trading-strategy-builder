# Copyright © 2024 Taoshi Inc

import csv

from config import Config
from data_generator.binance_data_generator import BinanceDataGenerator
from utils.time_util.time_util import TimeUtil


if __name__ == "__main__":

	# choose the range of days to look back
	# number of days back start
	days_back_start = 5
	# number of days forward since end day
	# for example start from 100 days ago and get 70 days from 100 days ago
	# (100 days ago, 99 days ago, 98 days ago, etc.)
	days_back_end = 5

	ts_ranges = TimeUtil.convert_range_timestamps_to_millis(
		TimeUtil.generate_range_timestamps(
			TimeUtil.generate_start_timestamp(days_back_start), days_back_end, True))

	ds = [[], [], [], [], []]

	binance_data_generator = BinanceDataGenerator()
	for ts_range in ts_ranges:
		binance_data_generator.get_data_and_structure_data_points("BTCUSDT", "5m", ds, ts_range)

	data = ["Open Timestamp (ms)", "Close", "Datetime"]

	# CSV filename
	csv_filename = Config.BASE_DIR + "/historical_data/historical_binance_data.csv"

	with open(csv_filename, mode='w', newline='') as file:
		writer = csv.writer(file)
		writer.writerow(data)  # Write header

		for i in range(0, len(ds[0])):
			writer.writerow([ds[0][i], ds[1][i], TimeUtil.millis_to_timestamp(ds[0][i])])
