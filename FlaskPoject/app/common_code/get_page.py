"""
   flask分页通过sqlalachemy查询进行分页
   分页器需要具备的功能
   页码
   分页数据
   分页范围
   是否第一页
   是否最后一页
   """


class Paginator():
    def __init__(self, data, page_size):
        """
        :param data: 要分页的的数据
        :param page_size: 每页有多少条数据
        """
        self.data = data  # 总数据 查询的一条数据信息，条数需要取len()
        self.page_size = page_size  # 每页的数据，传入的是数字
        self.next_page = 0  # 下一页
        self.previous_page = 0  # 上一页
        self.is_start = False  # 是否是首页
        self.is_end = False  # 是否是尾页
        # 页数 总数据个数/每页数据个数 向上取整加1
        self.page_number = int((len(data) + page_size - 1) / page_size)
        self.page_range = range(1, self.page_number + 1)  # 页码范围  3页的话是（1,4）

    def page_data(self, page):
        """
        :param page: 页码
       page_size = 10
       1. start 0 ,end 10
       2. start 10,end 20
       3, start 20, end 30
        """
        self.previous_page = int(page) - 1
        self.next_page = int(page) + 1
        if page <= self.page_number:
            start_page = (page - 1) * self.page_size
            end_page = page * self.page_size
            # 每页的数据
            page_data = self.data[start_page: end_page]
            if page == 1:
                self.is_start = True
            else:
                self.is_start = False
            if page == self.page_range[-1]:
                self.is_end = True
            else:
                self.is_end = False
        else:
            page_data = ["没有数据了"]
        return page_data


from app.models import *

if __name__ == '__main__':
    data = ApplicationForLeave.query.all()
    page_size = 3
    paginator = Paginator(data, page_size)

    while True:
        page = int(input("请输入页码>>>"))
        print("总页数为：%s" % (paginator.page_number,))
        print("页码范围为：%s" % (paginator.page_range,))

        page_data = paginator.page_data(page)
        print("页码数据为：%s" % (page_data,))
        print("当前页码是：%s" % page)
        print("是否首页：%s" % paginator.is_start)
        print("是否尾页：%s" % paginator.is_end)
