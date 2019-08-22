from example.commons import Collector, Faker
from pyecharts import options as opts
from pyecharts.charts import Bar, Page

C = Collector()

@C.funcs
def bar_markline_type() -> Bar:
    c = (
        Bar()
        .add_xaxis(tryCnt)
        .add_yaxis("商家A", Faker.values())
        #.add_yaxis("商家B", Faker.values())
        .set_global_opts(title_opts=opts.TitleOpts(title="Bar-MarkLine（指定类型）"))
        .set_series_opts(
            label_opts=opts.LabelOpts(is_show=False),
            markline_opts=opts.MarkLineOpts(
                data=[
                    opts.MarkLineItem(type_="min", name="最小值"),
                    opts.MarkLineItem(type_="max", name="最大值"),
                    opts.MarkLineItem(type_="average", name="平均值"),
                ]
            ),
        )
    )
    return c

tryCnt = ["{}".format(i) for i in range(1, 1001)]
print(len(tryCnt))

Page().add(*[fn() for fn, _ in C.charts]).render('BarMarkLine.html')    