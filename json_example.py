import json
import requests
import time
from pprint import pprint
from requests.exceptions import HTTPError

while True :
    try :
        # 테스트에 사용할 postman collection json 파일 위치를 입력받는다
        caseFile = input('Enter a full location of case file:')
        if caseFile == '' : caseFile = 'D:\Documents\[PGM-PR-972]QA 심의 서류 관리.json'
        # cpc949 인코딩 처리시 문제가 발생하기 때문에 UTF8로 handler를 받아온다.
        fhandle = open(caseFile, encoding='UTF8')
    except FileNotFoundError as nfErr :
        # 존재하지 않는 파일일 경우 계속 재입력을 요구한다.
        print('No such file. Input valid location!')
        continue
    else : break
    
while True :
    try :
        # 테스트 횟수를 입력받는다
        iterations = int(input('Enter a loop count(number only, above 0):'))
        if iterations <= 0 : raise ValueError()
    except ValueError as vErr :
        # 숫자형식이 아닐 경우 재입력을 요구한다.
        print('Not a valid number. Input a number above 0!')
        continue
    else : break
        

#with open('D:\Documents\[PGM-PR-972]QA 심의 서류 관리.json', encoding='UTF8') as json_file :
with fhandle as json_file :

    failCnt = 0     # 실패 횟수
    succCnt = 0     # 성공 횟수
    totalCnt = 0    # 전체 횟수 
    subLoopCnt = 0  # collection json에 존재하는 request 수만큼 loop
    method = ''
    base_url = ''    
    totalTime = 0
    succTime = 0
    jsonData = json.load(json_file)
    #key가 item인 객체 가져와서 만들기
    item = jsonData["item"]
    '''
    아래와 같이 json format에 따라 어떤것은 list 객체로 parsing되고 어떤 것은 dict 객체로 parsing된다.
    print('type(item): ', type(item))                           # <class 'list'>
    print('type(item[0]): ' , type(item[0]))                    # <class 'dict'>
    print("type(item[0]['item']): ", type(item[0]['item']))     # <class 'list'>
    '''
    for cnt in range(iterations) :
        fileNo = ''
        for each in item[0]['item'] :
            if '_018_' not in str(each) : continue  # 특정 문자열을 가진 request만 추출            
            for key,value in each.items() :
                paramStr = ''                              # GET 전송용 parameter string            
                paramDict = dict()                         # POST 전송용 parameter set
                fileDict = dict()                          # POST FILE 전송시 file set 
                #print ('key:', key,'value:', value)
                if key == 'request' :
                    subLoopCnt += 1   
                    for request in value.items() :
                        if 'method' in request : method = request[1]   # Method 추출 
                        if 'url' in request : 
                            #print(request[1])                         # <class 'dict'>
                            reqDict = request[1]                        
                            base_url = reqDict['raw']
                            #print(type(reqDict['query']))             # <class 'list'>       
                            if 'query' in reqDict : # print('EXT NOT EXISTS!!!!!!!!!!!!!!!')
                                querySet = reqDict['query']
                                for paramSet in querySet :
                                    if paramSet['key'] != 'file' :
                                        '''
                                        if paramSet['key'] == 'fileNo' : 
                                            paramDict[paramSet['key']] = fileNo
                                            paramStr += paramSet['key']+'='+fileNo+'&' 
                                        else :
                                        '''
                                        paramDict[paramSet['key']] = paramSet['value']
                                        paramStr += paramSet['key']+'='+paramSet['value']+'&' 
                                        #print(paramSet['key']+'='+paramSet['value'])
                        # body쪽 파라미터는 따로 체크하지 않는다. 
                        '''
                        if 'body' in request :
                            if "formdata" in request[1] : # "body"
                                for bodySet in request[1]['formdata'] :
                                    #print(bodyDict)
                                    if bodySet['key'] != 'file' : continue
                                    else : 
                                        if len(bodySet['src']) > 0 : print("src:",bodySet['src'][1:])
                        '''
                    if base_url != '' and method != '' :
                        #print('BASE_URL :', base_url)
                        #print('METHOD :', method)
                        #print('PARAMS :', paramStr)
                        #print('PARAMDICT :', paramDict)
                        #print('Total Numbers of Test Request : ', len(item[0]['item']))
                        
                        print(f'Try {subLoopCnt} ==================================================================================================')
                        print(f'Sending in "{method}" to "{base_url}"')
                        totalCnt += 1
                        try :
                            headers = {
                                "User-Agent": "TestCaseRunner",
                                "Accept-Encoding": "*",
                                "Cache-Control": "no-cache",
                                "Host": "sellerapi-d.kshop.co.kr",
                                "Connection": "close",
                                "Postman-Token": "87229a52-a9ef-4f5a-8f20-e2adce340eae"+str(subLoopCnt),
                            }
                            '''                           
                                "Accept": "*/*",
                                "Accept-Encoding": "gzip, deflate",
                                "Cache-Control": "no-cache",
                                "Connection": "keep-alive",
                                "Content-Type": "multipart/form-data; boundary=--------------------------945171453175027715639666",
                                "Host": "sellerapi-d.kshop.co.kr",
                                "Postman-Token": "87229a52-a9ef-4f5a-8f20-e2adce340eae",
                                "User-Agent": "PostmanRuntime/7.15.2"                             
                                
                                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
                                "Accept-Encoding": "*",
                                "Connection": "keep-alive"
                            '''
                            if method == 'POST' :
                                #res = requests.post('http://localhost:9005/sellerapi/partner/goods/sqc-paper-menagement'
                                res = requests.post(base_url
                                , headers=headers
                                , files={'file' : open('D:/Documents/nkshop/03.단위테스트케이스/API_0082_테스트용_업로드파일모음/018_DOC.doc','rb')}
                                , data=paramDict)
                            else :                        
                                res = requests.get(base_url, data=paramDict)
                            totalTime += res.elapsed.total_seconds()
                            #print('totalTime:',totalTime)                            

                            resData = res.json()                        
                            if res.status_code != 200 :   # Failed
                                print(f'Request Failed : {resData["message"]}')
                                failCnt += 1
                                #continue     
                            else :
                                print(f'Completed request in "{res.elapsed.total_seconds()}" seconds')
                                succCnt += 1          
                                succTime += res.elapsed.total_seconds()              
                            #print('succTime:',succTime)                                                            

                            fileNo = resData['fileNo']         
                            #print('fileNo:'+fileNo)                   
                        except Exception as err :        
                            print(f'Error occured: {res.json(),err}')
                            failCnt += 1
                            continue                
                            #res.raise_for_status()
                            #print("Response:", res.json())
                        '''
                        except HTTPError as http_err :
                            print(f'HTTP error occured: {res.json()}')
                            failCnt += 1                            
                            continue
                        except Exception as err :        
                            print(f'Other error occured: {res.json()}')
                            failCnt += 1
                            continue                
                        else :
                            print(f'Completed request in "{res.elapsed.total_seconds()}" seconds')
                            succCnt += 1                                                        
                            #print("Response:", res.json())
                        '''
                        #time.sleep(1)
                    # End of if base_url != '' and method != '' :
                else : continue                             
            # End of for loop
    succAverageTime = 0
    totalAverageTime = 0
    if succCnt > 0 : succAverageTime = format(succTime / succCnt, '.3f')
    if totalTime > 0 : totalAverageTime = format(totalTime / totalCnt, '.3f')

    print(f"Total Time:{format(totalTime, '.3f')}s / Total Success Time:{format(succTime, '.3f')}")
    print(f'Total Request Counts:{totalCnt} / succeeded Counts:{succCnt} / Failed Counts:{failCnt}')
    print(f"Average Request Time:{totalAverageTime}s / Average Success Time:{succAverageTime}s")