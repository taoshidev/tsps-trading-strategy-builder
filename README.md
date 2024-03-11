# TSPS Trading Strategy Builder

This repo allows users to consume the historical data from TSPS and build trading strategies. This repository will
provide a basis for you to be able to do analysis on the data, build a trading strategy, and backtest the strategy
against historical data on all Streams inside of TSPS.

## Current TSPS Data

Currently, the concentration will be on BTCUSD, but that will expand soon. Please read the instructions below to get started.

<img width="500" alt="img1" src="https://github.com/taoshidev/tsps-trading-strategy-builder/assets/68529441/362f6d25-b2a7-477b-90d9-c0187d7a0fd4">
<img width="500" alt="img2" src="https://github.com/taoshidev/tsps-trading-strategy-builder/assets/68529441/a7d26d77-b7e0-4ffa-a8f9-aecbeb618338">

## Requirements to Download Historical Data

### 1. Download Historical TSPS Data

You'll need the historical data in order to build a trading strategy.

To download historical performance of miners and their predictions, you first need to have Google's gcloud SDK installed.

- For Mac, you can use brew [google-cloud-sdk](https://www.google.com/url?q=https://formulae.brew.sh/cask/google-cloud-sdk&sa=D&source=editors&ust=1709847321009780&usg=AOvVaw08rMMGBBvNtBBMA-PLkmMZ).
- A more comprehensive documentation is also provided by Google: [Install the gcloud CLI | Google Cloud CLI Documentation](https://www.google.com/url?q=https://cloud.google.com/sdk/docs/install&sa=D&source=editors&ust=1709847321011119&usg=AOvVaw1neRJNmU3o8D4AUqCmP7kC).

Clone repository

```bash
git clone https://github.com/taoshidev/tsps-trading-strategy-builder.git
```

Change directory

```bash
cd /tsps-trading-strategy-builder/historical_data
```

Download historical data

```bash
gsutil cp -r gs://tsps_btc .
```

This should automatically build a tsps_btc folder in this repository.

Expected output dir: `historical_data/tsps_btc/`

### 2. Download Historical BTC Data

Once you've downloaded historical TSPS data, you should download historical BTC data to speed up your processes.

You can do this by running the `get_historical_data.py` script.

```bash
python historical_data/get_historical_data.py
```

This will generate a data file from binance called `historical_binance_data.csv` which will provide the actual closes that occurred that can be paired with the predictions to analyze results.

### Analyzing Data

The main logic outlined currently lives in the `run.py` script. The current setup takes the ongoing historical data
dump from gcloud, along with the generated historical btc data, and transforms it to allow you to analyze the results
by top miners on the network.

**Things to consider**

- Adding smoothing averages across top performing miners using weighted averages
- Concentrating trading strategies on larger moves, and consensus on larger moves
- Adding additional market indicators to add more signal
  - horizontal / diagonal resistances
  - traditional indicators such as MACD / RSI
  - futures data (such as liquidiation events)
- Using the above in a consensus model (LSTM)

### Next Feature

- Build additional signals
- Create the first open source consensus model (LSTM)
- Build a backtesting engine

## License

### Copyright © 2024 Taoshi Inc

```Taoshi All rights reserved.
Source code produced by Taoshi Inc may not be reproduced, modified, or distributed
without the express permission of Taoshi Inc.
```
