#分析房价数据并简单可视化
import csv
import statistics
import matplotlib.pyplot as plt

# 读取CSV文件
with open('hefei_house_price_.csv', 'r', encoding='utf-8') as f:
  reader = csv.reader(f)
  data = list(reader)

# 获取小区名称列表和房价列表
names = [row[0] for row in data]
prices = [int(row[1]) for row in data]

# 计算数据的统计信息
mean = statistics.mean(prices)
median = statistics.median(prices)
min_price = min(prices)
max_price = max(prices)
print('房价平均数：',mean)
print('房价中位数：',median)
print('房价最小值：',min_price)
print('房价最大值：',max_price)

# 获取前二十个最高和最低价格的小区
sorted_prices = sorted(data, key=lambda x: int(x[1]))
highest_prices = sorted_prices[-20:]
lowest_prices = sorted_prices[:20]

# 输出前二十个最高和最低价格的小区
print('前二十个最高价格的小区：')
for row in highest_prices:
  print(row[0], row[1])

print('前二十个最低价格的小区：')
for row in lowest_prices:
  print(row[0], row[1])

# 绘制直方图
plt.hist(prices, bins=20)
plt.show()

# 绘制散点图
plt.scatter(names, prices)
plt.show()
