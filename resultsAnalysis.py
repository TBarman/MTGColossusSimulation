import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

results = pd.read_csv("results.csv")


print(len(results))
# Pivot into 9x9 table
pivot = results.pivot_table(index="cheap_reanimation", columns="expensive_reanimation", values="lands_in_play", aggfunc="mean")
# Display as heatmap
fig, ax = plt.subplots(1, 1, figsize=(10, 8))

sns.heatmap(pivot, annot=True, fmt=".2f", cmap="YlOrRd", ax=ax)
ax.set_title("Lands In Play by Turn 4 (1,000,000 Samples Per Group)")

plt.tight_layout()
plt.show()