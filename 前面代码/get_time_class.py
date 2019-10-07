"""
   当前类实现日历功能
   1、返回列表嵌套列表的日历
   2、按照日历格式打印日历

   # 如果一号周周一那么第一行1-7号   0
       # 如果一号周周二那么第一行empty*1+1-6号  1
       # 如果一号周周三那么第一行empty*2+1-5号  2
       # 如果一号周周四那么第一行empty*3+1-4号  3
       # 如果一号周周五那么第一行empyt*4+1-3号  4
       # 如果一号周周六那么第一行empty*5+1-2号  5
       # 如果一号周日那么第一行empty*6+1号   6
       # 输入 1月
       # 得到1月1号是周几
       # [] 填充7个元素 索引0对应周一
       # 返回列表
       # day_range 1-30
   """
import datetime


class Calendar():
    # 定义日历
    def __init__(self, year=2019, month=9):
        # 定义一个日期返回的嵌套列表，列表中嵌套的是每行7个元素的列表
        self.result = []

        # 定义最大月份和最小月份
        big_month = [1, 3, 5, 7, 8, 10, 12]
        small_month = [4, 6, 9, 11]

        # 获取当前月的第一天
        first_date = datetime.datetime(year, month, 1, 0, 0)

        if month in big_month:
            day_range = range(1, 32)
        elif month in small_month:
            day_range = range(1, 31)
        else:
            day_range = range(1, 29)

        self.day_range = list(day_range)
        # 当前月的第一天是一周的第几天
        first_week = first_date.weekday()

        # 第一行
        line1 = []
        for i in range(first_week):
            line1.append("空")
        for j in range(7 - first_week):
            line1.append(str(self.day_range.pop(0)))
        self.result.append(line1)

        # 第n至多行
        while self.day_range:
            line = []
            for i in range(7):
                if len(line) < 7 and self.day_range:
                    line.append(str(self.day_range.pop(0)))
                else:
                    line.append("空")

            self.result.append(line)

    def return_calendar(self):
        return self.result

    # 打印日历
    def print_calendar(self):
        print(" Mon ", " Tue ", " Wed ", " Thu ", " Fri ", " Sat ", " Sun ")
        for line in self.result:
            for day in line:
                day = day.center(4)
                print(day, end=" ")
            print()


if __name__ == '__main__':
    c = Calendar(2019, 8)
    print(c.return_calendar())
    c.print_calendar()
