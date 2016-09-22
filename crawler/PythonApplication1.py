#coding=utf-8
import decimal
import requests
from bs4 import BeautifulSoup
import uuid
import datetime
import time
import pymysql
import simplejson as json
import random
import logging
import re

logging.basicConfig(filename='eventlog',level=logging.INFO)
print "程式開始"
for area in range(13):
    areaStr="0"+str(area) if area<10 else str(area)
    if area>0:
        base104Link_area="http://www.104.com.tw/jobbank/joblist/joblist.cfm?jobsource=n104bank1&ro=0&jobcat=2007000000&area=60010010{0}&order=2&asc=0&page=1".format(areaStr)
        res_area = requests.get(base104_area)

        soup_area = BeautifulSoup(res_area.text)
        pageCount=0
        for item in soup_area.select(".joblist_bar"):
            pages=item.select(".right")
            page = re.sub(r'\D', "", pages[0].text[2:6])
            pageCount=int(page)/15  if int(page)<2250 else 151
            

        if pageCount>0:    
            for x in range(pageCount):
                if x >0:
                    jsonDateNowTemp=json.dumps({"now":str(datetime.datetime.now())})
                    DateNowTemp=json.loads(jsonDateNowTemp)
                    print str(x)+"page----"+DateNowTemp["now"].encode("utf8")
                    logging.info("area:"+str(area)+","+str(x)+"page-------"+DateNowTemp["now"].encode("utf8"))
                    base104Link="http://www.104.com.tw/jobbank/joblist/joblist.cfm?jobsource=n104bank1&ro=0&jobcat=2007000000&area=60010010{0}&order=2&asc=0&page={1}".format(areaStr,x)

                    res = requests.get(base104Link)

                    soup = BeautifulSoup(res.text)
                    for item in soup.select(".joblist_bar"):
                        pages=item.select(".right")
                        print pages[0].text[2:6].encode("utf8")
                    for item in soup.select(".j_cont"):
                       
                        try:
                            vacanciesName = item.select(".job_name")
                            vacanciesLink=item.select(".job_name > a")
                            print vacanciesName[0].text.encode("utf8")
                            companyName = item.select(".compname_summary")
                       
                        except:
                            print "抓資料失敗,"+DateNowTemp["now"].encode("utf8")
                            logging.info("抓資料失敗,"+DateNowTemp["now"].encode("utf8"))
                            
                        try:
                            connection = pymysql.connect()

                            with connection.cursor() as cursor:
                               
                                dataIfExist ="select id,startDate From VacanciesHealthCheck Where vacanciesLink = %s"
                            
                                cursor.execute(dataIfExist,vacanciesLink[0].attrs["href"].encode("utf8"))
                                id=cursor.fetchone()
                                if id:
                                    exitDay=datetime.datetime.now()-datetime.datetime.strptime(id["startDate"], "%Y-%m-%d %H:%M:%S.%f")
                                    sql = "Update  `VacanciesHealthCheck` SET `exitDay`= %s, `updateState`= 1 where id= %s"
                                    cursor.execute(sql, (str(exitDay.days).encode("utf8"),id["id"]))
                                else:
                                    sql = "INSERT INTO `VacanciesHealthCheck`(vacanciesName, vacanciesLink,companyName,startDate,updateDate,exitDay,updateState) VALUES (%s, %s,%s,%s,%s,%s,%s)"
                                    cursor.execute(sql, (vacanciesName[0].text.encode("utf8"), vacanciesLink[0].attrs["href"].encode("utf8"),companyName[0].text.encode("utf8"),DateNowTemp["now"].encode("utf8"),DateNowTemp["now"].encode("utf8"),"1".encode("utf8"),"1".encode("utf8")))
                                    print vacanciesName[0].text.encode("utf8")

                                cursor.execute("COMMIT")
                        except Exception as e:
                            print e
                            logging.info(e)
                            logging.info("資料庫錯誤,"+DateNowTemp["now"].encode("utf8"))
                            
                    try:
                        connection.close()
                    except Exception as e:
                           logging.info("connection.close error,"+DateNowTemp["now"].encode("utf8"))
                    time.sleep(random.randint(30, 75));

print "程式結束"
logging.info("程式結束,"+DateNowTemp[now].encode("utf8"))
logging.info("程式結束,")
