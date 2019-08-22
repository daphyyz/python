#from pyecharts.charts.basic_charts.bar import Bar
#from pyecharts import options as opts
from pyecharts.charts import Bar
from pyecharts import options as opts

(Bar()
    .add_xaxis(["Microsoft", "Amazon", "IBM", "Oracl", "Google", "Alibaba"])
    .add_yaxis('2017-2018 Revenue in (billion $)', [21.2, 20.4, 10.3, 6.08, 4, 2.2])
    .set_global_opts(title_opts=opts.TitleOpts(title="Top cloud providers 2018", subtitle="2017-2018 Revenue"))
    .render() # generate a local HTML file
)