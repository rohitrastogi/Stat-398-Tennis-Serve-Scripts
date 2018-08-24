import pandas as pd

data = pd.read_csv('all_data.csv')
handedness = pd.read_csv("handedness.csv")


merged = pd.merge(data, handedness, on = "player")

merged.to_csv("all_data_with_handeness.csv")
