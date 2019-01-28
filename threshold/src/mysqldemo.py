import MySQLdb
import time
import datetime
import schedule
import time
import configparser

import threading
class Polling(threading.Thread):
    def __init__(self,data,minute,host,port,user,passwd,db,charset):
        self.data=data
        self.minute=minute
        self.host=host
        self.port=port
        self.user=user
        self.passwd=passwd
        self.db=db
        self.charset=charset
    def initd(self,deviceName,metricName,ruleId,sampleDataTimeRange,data):
        print 2222
        if deviceName not in data.keys():
            data[deviceName]={}
        if metricName not in data[deviceName].keys():
            data[deviceName][metricName]={}
        if "ruleId" not in data[deviceName][metricName].keys():
            data[deviceName][metricName]["ruleId"]=ruleId
        elif ruleId!=data[deviceName][metricName]["ruleId"]:
            print "changed"
            del data[deviceName][metricName]["timeout"]
            print data
            data[deviceName][metricName]["ruleId"]=ruleId
        data[deviceName][metricName]["sampleDataTimeRange"]=sampleDataTimeRange
        if "latestTime" not in  data[deviceName][metricName].keys():
            data[deviceName][metricName]["latestTime"] = time.time()
        
    def check(self):
        db = MySQLdb.connect(host=self.host,user=self.user,passwd=self.passwd,port=self.port,db=self.db,charset=self.charset)
        sql="SELECT *FROM RULE WHERE alarmType='THRESHOLD'"
        cursor = db.cursor()

        try:
                cursor.execute(sql)
                results = cursor.fetchall()
		total={}
                for row in results:
                        print 111
                        #row[0]=ruleId,row[1]=clusterId,row2=namespace,row3=ruleName,row4=description,row5=tab,row6=ruleState,row7=severity,row8=alarmType,row9=metricName,row10=monitorObjectType,row11=monitorObjectValue,row12=monitorCondition,row13=updateTime,row14=createTime
                        deviceName=str(row[11])
                        metricName=str(row[9])
                        monitorObjectType = str(row[10])
                        if monitorObjectType=="pod":
                            deviceName=str(row[2])+"_"+deviceName
                        ruleId=str(row[0])
                       
                        sampleDataTimeRange=eval(str(row[12]))
                        
                        sampleDataTimeRange=sampleDataTimeRange["sampleDataTimeRange"][:-1]
                       
                        self.initd(deviceName, metricName, ruleId, sampleDataTimeRange, self.data)
                       
			if deviceName not in total.keys():
			   
                            total[deviceName]=[]
                       
			total[deviceName].append(metricName)
                        
                
		for item in list(self.data.keys()):
			if item not in total.keys():
				del self.data[item]
			for i in list(self.data[item].keys()):
				if i not in total[item]:
					del self.data[item][i]

        except Exception,e:
                print "err", repr(e)
		
        db.close()
        print(self.data)
    def run(self):
        schedule.every(self.minute).minutes.do(self.check)
        self.check()
        while True:
            schedule.run_pending()
            time.sleep(100)

if __name__ == '__main__':
    data={}
    cf = configparser.ConfigParser()
    cf.read("python.ini")
    host =cf.get("mysql", "host").encode()
    port = int(cf.get("mysql", "port"))
    user = cf.get("mysql", "user").encode()
    passwd =cf.get("mysql", "passwd").encode()
    db = cf.get("mysql", "db").encode()
    charset = cf.get("mysql", "charset").encode()
    minute =int(cf.get("mysql", "minute"))
    print host,port ,user,passwd,db,charset,minute,type(minute),type(db)
    Polling(data,minute,host,port,user,passwd,db,charset).run()

