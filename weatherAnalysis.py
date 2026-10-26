import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("weather.csv")

print("Average Temperature:", df["Temperature"].mean())
print("Maximum Temperature:", df["Temperature"].max())
print("Minimum Temperature:", df["Temperature"].min())

print("Hottest Day:")
print(df.loc[df["Temperature"].idxmax()])

# Line chart
plt.plot(df["Date"], df["Temperature"])
plt.show()

# Histogram
plt.hist(df["Temperature"])
plt.show()

# Scatter plot
plt.scatter(df["Humidity"], df["Temperature"])
plt.show()