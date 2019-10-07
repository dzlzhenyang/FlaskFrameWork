import datetime

# 定义一个日期返回的嵌套列表，列表中嵌套的是每行7个元素的列表
result = []

# 定义最大月份和最小月份
big_month = [1, 3, 5, 7, 8, 10, 12]
small_month = [4, 6, 9, 11]

now = datetime.datetime.now()

# 当月第一天   年 月 日 时 分
first_date = datetime.datetime(now.year, now.month, 1, 0, 0)
month = now.month
if month in big_month:
    day_range = range(1, 32)
elif month in small_month:
    day_range = range(1, 31)
else:
    day_range = range(1, 29)

# 返回当月1号是周几
first_week = first_date.weekday()

# 将当月的天数，转换为列表
day_range = list(day_range)

# 第一行数据
line1 = []
for i in range(first_week):
    line1.append("空")
for j in range(7 - first_week):
    line1.append(str(day_range.pop(0)))
result.append(line1)

# 第二至n行数据
while day_range:  # 如果列表有值，就继续循环
    line = []
    # 每次循环向列表中添加7个元素
    for i in range(7):
        if len(line) < 7 and day_range:
            line.append(str(day_range.pop(0)))
        else:
            line.append("空")
    # 每次循环都将结果添加到result中
    result.append(line)
# print(result)
print(" Mon ", " Tue ", " Wed ", " Thu ", " Fri ", " Sat ", " Sun ")
for line in result:
    for day in line:
        day = day.center(4)
        print(day, end=" ")
    print()
