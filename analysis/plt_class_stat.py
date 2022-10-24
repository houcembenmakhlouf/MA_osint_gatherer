import matplotlib
import matplotlib.pyplot as plt


x = [
    "automotiveIndustry",
    "corona",
    "economics",
    "fun",
    "history",
    "politics",
    "promotion",
    "social",
    "sport",
    "technology",
    "war",
    "weather",
]
y = [270, 3169, 973, 1332, 458, 3444, 524, 1951, 4952, 169, 7608, 443]

plt.bar(x, y)
plt.xlabel("class names")
plt.ylabel("data instances")
plt.title(
    "Distribution of the number of tweets per topic with multi-class classification"
)
plt.show()
