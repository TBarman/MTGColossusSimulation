import pandas as pd
import matplotlib.pyplot as plt

deckConfigs = [(i, j) for i in range(1, 10) for j in range(1, 10)]

results = pd.read_csv("results.csv")

means = [[0] * 9 for i in range(9)]
maxConfig = (1, 1)
max = 0
for (cheap, expensive) in deckConfigs:
    data = results[(results.cheap_reanimation == cheap) & (results.expensive_reanimation == expensive)]["lands_in_play"]
    mean = data.mean()
    if mean > max:
        maxConfig = (cheap, expensive)
        max = mean


print(f"{maxConfig}: {max}")

