# Copyright © 2024 Taoshi Inc

import numpy as np

from config import Config
from utils.time_util.time_util import TimeUtil
from utils.tsps_utils import TSPSUtils

import matplotlib.pyplot as plt

if __name__ == "__main__":
	# flatten all historical data
	historical_data = TSPSUtils.load_historical_data()
	# map the start / end dates of all request uuids
	request_uuid_start_end_map = TSPSUtils.get_request_uuid_start_end_map()
	print(request_uuid_start_end_map)

	request_uuid_map_w_historical_prices = request_uuid_start_end_map

	# get historical closes for every request uuid
	# you can do this in 2 ways

	##################################################################################################
	# Option 1
	# get the data directly from binance if you don't have a local binance data file downloaded
	# binance_data_generator = BinanceDataGenerator()
	# for k, v in request_uuid_start_end_map.items():
	# 	ds = [[],[]]
	# 	binance_data_generator.get_data_and_structure_data_points("BTCUSDT","5m", ds,(v["start"], v["end"]))
	# 	if len(ds[0]) < 100:
	# 		print(f"WARN - closing prices list less than 100 rows [{len(closing_prices)}]")
	# 	else:
	# 		print("SUCCESS - found 100 rows with closing prices for range.")
	# 		request_uuid_map_w_historical_prices[k]["closes"] = ds[1]
	##################################################################################################

	##################################################################################################
	# Option 2 - default
	# if you have the local file stored after generating from get_historical_data.py
	historical_binance_data = TSPSUtils.read_file(Config.BASE_DIR + "/historical_data/historical_binance_data.csv")

	# get mapping between closes to request uuid
	for k, v in request_uuid_start_end_map.items():
		closing_prices = []
		for row in historical_binance_data:
			if int(v["start"]) <= int(row["Open Timestamp (ms)"]) <= int(v["end"]):
				closing_prices.append(float(row["Close"]))
		if len(closing_prices) < 100:
			print(f"WARN - closing prices list less than 100 rows [{len(closing_prices)}]")
		else:
			print("SUCCESS - found 100 rows with closing prices for range.")
			request_uuid_map_w_historical_prices[k]["closes"] = closing_prices
	##################################################################################################

	# get the top [x] miners per request uuid by weight_score
	top_miners = 10

	top_miners_per_request_uuid = {}
	top_miners_per_request_uuid_only_closes_flattened = {}
	for r, v in historical_data.items():
		muid_scores = []
		for muid, mv in v.items():
			if "predictions" in mv:
				muid_scores.append([muid, mv["weight_score"], mv["rmse"], mv["predictions"]])
		# muid_scores = [[muid, mv["weight_score"], mv["rmse"], mv["predictions"]] for muid, mv in v.items()]
		muid_scores_sorted = sorted(muid_scores, key=lambda x: x[1], reverse=True)
		top_muid_scores = muid_scores_sorted[:top_miners]
		top_miners_per_request_uuid[r] = top_muid_scores
		# adding predictions with actual closes
		top_miners_per_request_uuid_only_closes_flattened[r] = [top_muid_score[3] for top_muid_score in top_muid_scores]
		if r in request_uuid_map_w_historical_prices:
			top_miners_per_request_uuid_only_closes_flattened[r].append(
				request_uuid_map_w_historical_prices[r]["closes"])

	# Plot each request_uuid
	for request_uuid, miners_per_request_uuid in top_miners_per_request_uuid_only_closes_flattened.items():
		array = np.array(miners_per_request_uuid)
		transposed_array = array.transpose()

		plt.plot(transposed_array)

		request_uuid_timestamp = TimeUtil.millis_to_timestamp(int(request_uuid_start_end_map[request_uuid]["start"]))

		# Show the plot
		plt.xlabel('Time')
		plt.ylabel('Price')
		plt.title(f'Top [{top_miners}] miners vs. Closing Prices on [{request_uuid_timestamp}] (start)')
		plt.show()
