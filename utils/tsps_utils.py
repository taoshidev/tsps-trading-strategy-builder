# Copyright © 2024 Taoshi Inc

import ast
import csv
import os

from config import Config


class TSPSUtils:
	TSPS_BTCUSD_5_DIR = "/historical_data/tsps_btc/"
	TSPS_BTCUSD_5_CMW_DIR = "BTCUSD-5m-cmw/"
	TSPS_BTCUSD_5_PREDS_DIR = "BTCUSD-5m-predictions/"

	@staticmethod
	def get_all_files_in_dir(dir: str, ascending: bool = True) -> list[str]:
		all_files = []
		if os.path.exists(dir):
			for filename in os.listdir(dir):
				if os.path.isfile(os.path.join(dir, filename)):
					all_files.append(os.path.join(dir, filename))

		# Sort files based on creation date
		all_files.sort(key=lambda x: os.path.getctime(x), reverse=not ascending)

		return all_files

	@staticmethod
	def read_file(csv_filename: str):
		data = []
		with open(csv_filename, mode='r', newline='') as file:
			reader = csv.DictReader(file)
			for row in reader:
				data.append(dict(row))
		return data

	@staticmethod
	def get_all_cmw_files():
		all_cmw_files = TSPSUtils.get_all_files_in_dir(
			Config.BASE_DIR + TSPSUtils.TSPS_BTCUSD_5_DIR + TSPSUtils.TSPS_BTCUSD_5_CMW_DIR)
		return all_cmw_files

	@staticmethod
	def get_all_prediction_files():
		all_pred_files = TSPSUtils.get_all_files_in_dir(
			Config.BASE_DIR + TSPSUtils.TSPS_BTCUSD_5_DIR + TSPSUtils.TSPS_BTCUSD_5_PREDS_DIR)
		return all_pred_files

	@staticmethod
	def load_historical_data():
		all_cmw_files = TSPSUtils.get_all_cmw_files()
		all_pred_files = TSPSUtils.get_all_prediction_files()

		all_completed_historical_data = {}

		for cmw_file in all_cmw_files:
			fd = TSPSUtils.read_file(cmw_file)
			for row in fd:
				if row["request_uuid"] not in all_completed_historical_data:
					all_completed_historical_data[row["request_uuid"]] = {}
				all_completed_historical_data[row["request_uuid"]][row["miner_id"]] = {
					"rmse": row["rmse"],
					"weight_score": row["weight_score"]
				}

		for pred_file in all_pred_files:
			fd = TSPSUtils.read_file(pred_file)
			for row in fd:
				if row["request_uuid"] in all_completed_historical_data and row["miner_uid"] in \
						all_completed_historical_data[row["request_uuid"]]:
					miner_request_row = all_completed_historical_data[row["request_uuid"]][row["miner_uid"]]
					miner_request_row["start"] = row["start"]
					miner_request_row["end"] = row["end"]
					miner_request_row["predictions"] = ast.literal_eval(row["predictions"])

		return all_completed_historical_data

	@staticmethod
	def get_request_uuid_start_end_map():
		request_uuid_start_end_dates_map = {}
		all_preds_files = TSPSUtils.get_all_prediction_files()
		for pred_file in all_preds_files:
			fd = TSPSUtils.read_file(pred_file)
			for row in fd:
				request_uuid_start_end_dates_map[row["request_uuid"]] = {
					"start": row["start"],
					"end": row["end"]
				}
		return request_uuid_start_end_dates_map

