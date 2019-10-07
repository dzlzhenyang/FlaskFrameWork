"""
当前类实现的功能
1. 返回列表嵌套列表的日历
2. 按照日历的格式打印日历
"""
import datetime


class Calendar():
    def __init__(self, year=2019, month=9):
        # 定义列表返回的结果
        self.result = []
        # 定义最大月份和最小月份
        big_month = [1, 3, 5, 7, 8, 10, 12]
        small_month = [4, 6, 9, 11]

        if month in big_month:
            day_range = range(1, 32)
        elif month in small_month:
            day_range = range(1, 31)
        else:
            # 判断是否为闰年
            if year % 400 == 0 or year % 4 == 0 and year % 100 != 0:
                day_range = range(1, 30)
            else:
                day_range = range(1, 29)
        # 将day_range 转换为列表
        self.day_range = list(day_range)

        # 获取当月的第一天 年 月 日 时 分的形式显示
        first_day = datetime.datetime(year, month, 1, 0, 0)
        # 获取当月第一天是一周中的第几天
        where_day = first_day.weekday()

        # 第一行
        line1 = []
        # 比如第六天，6个空
        for i in range(where_day):
            line1.append("null")
        # 第六天，7-6个有值
        for j in range(7 - where_day):
            # 将day_range列表中的第一个元素弹出来，以字符串的方式添加到line1中
            line1.append(str(self.day_range.pop(0)))
        # 将line1添加到result中
        self.result.append(line1)

        # 第2-n行
        while self.day_range:
            line = []
            # 每行打印7个
            for i in range(7):
                # self.day_range 不存在时，进入else
                if self.day_range:
                    line.append(str(self.day_range.pop(0)))
                else:
                    line.append("null")
            # 在循环中，每打印一行line，添加一次
            self.result.append(line)

    def return_calendar(self):
        return self.result

    def print_calendar(self):
        print("周一", "周二", "周三", "周四", "周五", "周六", "周日")
        for line in self.result:
            for day in line:
                print(day, end="  ")
            print()


if __name__ == '__main__':
    calendar = Calendar(2018, 6)
    print(calendar.return_calendar())
    calendar.print_calendar()
