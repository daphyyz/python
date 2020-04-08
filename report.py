import os
import pprint
import math
import json
import plotly
from pyecharts.charts import Line, Bar, Pie, Page, Grid
from pyecharts import options as opts
from example.commons import Collector, Faker

def search(dirName) :
    fileList = list()
    fileNames = os.listdir(dirName)
    if len(fileNames) > 0 :
        for fileName in fileNames :
            fullFileName = os.path.join(dirName, fileName)
            ext = os.path.splitext(fullFileName)[-1]
            if ext == '.json' and 'postman_test_run' in fullFileName :
                print(fullFileName)
                fileList.append(fullFileName)
    else :
        print('!파일이 존재하지 않습니다!')
    return fileList


def groupTime(time) :
    if time in timeTable :
        timeTable[time] += 1
    else :
        timeTable[time] = 1
    return timeTable
    


while True :
    try :
        dirName = input('리포트를 작성할 데이터들이 들어있는 디렉토리를 입력하세요(중단하려면 q)\n파일명에 postman_test_run이 들어가있어야함\n:')            
        if dirName == 'q' : 
            print('중단입력')  
            break
        else :
            if dirName == '' : dirName = 'D:\Documents\StressTestResult'
            fileList = search(dirName)
            if len(fileList) <= 0 :
                print('!테스트 결과 파일이 존재하지 않습니다!')
                continue            
    except :
        print('!존재하지 않는 디렉토리입니다. 다시 입력해주세요!')
        continue
    else : break

timeList = list()
passList = list()
failList = list()
totalTimeList = list()
averageTimeList = list()
apiList = list()
timeGroup = list()
maxTimeList = list()

for file in fileList : 
    fhandler = open(file, encoding='UTF8')       
    jsonData = json.load(fhandler)
    resultSet = jsonData['results']
    eachTimes = list()
    timeTable = dict()    
    for time in resultSet[0]['times'] :
        eachTimes.append(int(time))  # 숫자형으로 변경해줘야 챠트에 정상적으로 값이 노출된다.
        # 253 / 100 -> math.round(2.53) -> 3 * 100 -> 300
        # 253 / 100 -> 2.53 -> math.ceil(2.53) -> 3 * 100 -> 300
        # 93 / 100 -> 0.93 -> math.ceil(0.93) -> 1 * 100 -> 100        
        boundary = math.ceil(int(time) / 100) * 100
        groupTime(boundary)
    maxTimeList.append(max(eachTimes))
    timeList.append(eachTimes)
    timeGroup.append(timeTable)
    apiList.append(jsonData['name'])
    passList.append(jsonData['totalPass'])
    failList.append(jsonData['totalFail'])
    totalTimeList.append(jsonData['totalTime'])
    averageTimeList.append(int(jsonData['totalTime'] / len(resultSet[0]['times'])))    
    #print (apiList, timeList, passList, failList, totalTimeList,averageTimeList)
    
tryCnt = ["{}".format(i) for i in range(1, 1001)]        
page = Page()
for i in range(len(apiList)) : 
    # 막대 차트 그리기
    ichart = (
        Bar()
        # X축에 표시될 값들을 리스트 객체로 넘긴다. 아래 값은 1부터 1000까지
        .add_xaxis(tryCnt)
        # Y축에 표시될 값들을 리스트 객체로 넘긴다. color 파라미터로 색상 지정가능하며 아래는 랜덤 컬러가 부여된다
        .add_yaxis("경과시간(단위:ms)", timeList[i], color=Faker.rand_color())
        .set_global_opts(
            # 타이틀 및 서브타이틀 지정 가능
            title_opts=opts.TitleOpts(
                title='요청별 응답시간', pos_right="2%",title_textstyle_opts=opts.TextStyleOpts(font_size=15)
                ,subtitle='최대 응답속도 :'+str(maxTimeList[i])+'ms\n평균 응답속도: '+str(averageTimeList[i])+'ms'
            ),
            # 인터렉티브 차트 기능인 줌 기능 설정 inside, 수직, 수평을 설정했다 (필요없을 시 인자에서 빼주면된다)
            datazoom_opts=[opts.DataZoomOpts(), opts.DataZoomOpts(orient="vertical"), opts.DataZoomOpts(type_="inside")],
            # 막대 차트의 값 분류들의 위치 지정 (서브 타이틀쪽에 표시된다)
            legend_opts=opts.LegendOpts(pos_right="30%"),
        )        
        .set_series_opts(
            label_opts=opts.LabelOpts(is_show=False),
            # 유의미한 특정 부분을 강조할때 사용된다. 아래는 라인(화살표)형태로 표시되며 markpoint 형식도 따로 있다.
            markline_opts=opts.MarkLineOpts(
                data=[
                    # 최소,최대,평균값을 알아서 표시해준다
                    opts.MarkLineItem(type_="min", name="최소"),
                    opts.MarkLineItem(type_="max", name="최대"),
                    opts.MarkLineItem(type_="average", name="평균"),
                ]
            ),
        )        
    )
    # 응답시간 그룹별 키와 값을 추출하여 각각 분류와 값 리스트에 담는다.
    groupDict = timeGroup[i]
    nameList = list()
    valueList = list()
    for k,v in groupDict.items() :
        nameList.append(k)
        valueList.append(v)

    # 파이 차트 그리기
    pchart = (
        Pie()
        .add("", [list(z) for z in zip(nameList, valueList)], center=["20%", "50%"]) # center에서 위치를 조정한다 첫번째 20%는 X축기준, 두번째는 Y축기준     
        .set_colors(["blue", "green", "yellow", "red", "pink", "orange", "purple"])
        .set_global_opts(
            # 타이틀 설정 pos_left(right,top,bottom등)로 위치 조절 가능
            title_opts=opts.TitleOpts(title=apiList[i]+" 응답시간 분류",title_textstyle_opts=opts.TextStyleOpts(font_size=15), subtitle='100 = 100ms 이하', pos_left="2%"),
            # 파이 차트 분류별 색상표의 수직,수평 또는 위치를 지정해준다
            legend_opts=opts.LegendOpts(
                orient="vertical", pos_top="15%", pos_left="2%"
            )
        )
        # 파이 차트에서 표시되는 값 형식 지정 아래와 같을 경우 900ms 응답그룹이 533명일 경우 900: 533으로 표시된다.
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))            
    )        

    # 막대차트와, 파이 차트를 그리드로 묶는다
    grid = (
        Grid()
        .add(ichart, grid_opts=opts.GridOpts(pos_left="40%"))
        .add(pchart, grid_opts=opts.GridOpts(pos_right="50%"))
    )
    # 묶은 그리드를 페이지 객체에 추가
    page.add(grid)
# End of For

# 페이지 객체에 들어있는 챠트들을 명시된 파일명으로 한페이지 출력
page.render('D:\\Documents\\StressTestResult\\reports_interactive.html')    

""" Plot.ly 라이브러리 사용시 
plotly.offline.init_notebook_mode() 
plotly.offline.plot({
"data": [{
    "x": ["{}".format(i) for i in range(1, 1001)] ,
    "y": timeList
}],
"layout": {
    "title": "hello world"
}
})
"""
