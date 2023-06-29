import pandas as pd
import datetime
from functools import reduce
df = pd.read_csv(r"hil_meas_cycle_time_sync\hil_meas.csv")
df = df.fillna(method='bfill')
cycle_time = "10ms"
print("Initial measurement count:",len(df))
datetime_format = df['Time[s]'].apply(lambda s : f"{datetime.timedelta(seconds=s)}")
df = df[['Time[s]','car::STEER_TORQUE::STEER_TORQUE','car::STEER_SENSOR::STEER_DIRECTION']]
idx = pd.to_datetime(datetime_format)
df = df.set_index(idx)
print("Sampling Cycle time:",cycle_time)
df = df.resample('10ms').bfill()
d = df.index.to_series().diff()
df.index = d.dt.total_seconds().cumsum().fillna(0)
print(df)
print("Synced measurement count:",len(df))
df.to_csv(r"hil_meas_cycle_time_sync\synced_meas.csv")