import pymysql
import simplejson as json
def lambda_handler(event, context):
    # TODO implement
    #context={'"linkArray":["/job/?jobno=4hi5a&jobsource=n104bank1&hotjob_chr=","/job/?jobno=4u9kp&jobsource=n104bank1&hotjob_chr=","1234"]'}
    strTest=["/job/?jobno=4hi5a&jobsource=n104bank1&hotjob_chr=","/job/?jobno=4u9kp&jobsource=n104bank1&hotjob_chr=","1234"]
    #test=json.dumps({"linkArray":strTest})
    #temp=json.loads('"linkArray":["1","2","3"]')
    #temp=json.loads(event)
    connection = pymysql.connect()    
    exitDayJson={};
    try:
        for item in event["linkArray"]:
            with connection.cursor() as cursor:
                # Create a new record
                exitDay ="select exitDay From VacanciesHealthCheck Where vacanciesLink = %s"
                queryResult=cursor.execute(exitDay,item)
                if queryResult:
                    for row in cursor:
                        exitDayJson[item]=row["exitDay"]

        connection.close()
    except:
        return json.dumps(event)
    #print json.dumps(exitDayJson)  
        
    return json.dumps(exitDayJson) 