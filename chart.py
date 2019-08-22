#from pyecharts.charts.basic_charts.bar import Bar
#from pyecharts import options as opts
from pyecharts.globals import ThemeType
from pyecharts.charts import Bar
from pyecharts import options as opts

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

(Bar(init_opts=opts.InitOpts(theme=ThemeType.DARK))
    .add_xaxis(["Microsoft", "Amazon", "IBM", "Oracl", "Google", "Alibaba"])
    .add_yaxis('2017-2018 Revenue in (billion $)', [21.2, 20.4, 10.3, 6.08, 4, 2.2])
    .set_global_opts(title_opts=opts.TitleOpts(title="Top cloud providers 2018", subtitle="2017-2018 Revenue"))
    .render() # generate a local HTML file
)