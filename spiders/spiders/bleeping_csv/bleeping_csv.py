import MySQLdb
import csv
import datetime
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
def get_conn():
    #conn=MySQLdb.connect(db="BleepingComputer_DB",host="localhost",user="root",passwd="123",use_unicode=True,charset="utf8")
    conn=MySQLdb.connect(db="BleepingComputer_DB",host="localhost",user="root",passwd = "root",use_unicode=True,charset="utf8")
    cursor=conn.cursor()
    return conn,cursor
class A():
    conn,cursor = get_conn()
    excel_file_name = 'bleeping_thread%s.csv'%str(datetime.datetime.now()).replace(' ','')
    oupf = open(excel_file_name, 'wb+')
    todays_excel_file = csv.writer(oupf)
    headers = ['Domain','Category','SubCategory', 'ThreadTitle', 'ThreadUrl', 'Postid', 'Posturl', 'PublishTime', 'FetchTime','Author', 'Text', ' Links','reference_url','crawl_type']
    todays_excel_file.writerow(headers)
    excel_auth_name1 = 'bleeping_Author%s.csv'%str(datetime.datetime.now()).replace(' ','')
    oupf1 = open(excel_auth_name1, 'wb+')
    todays_excel_file1  = csv.writer(oupf1)
    headers1 = ['thread_title','username', 'domain','crawl_type','author_signature','join_date','lastactive','totalposts','FetchTime','groups','reputation','credits','awards','rank','activetime','contactinfo','reference_url']
    todays_excel_file1.writerow(headers1)
    que = 'SELECT * from Threads'
    cursor.execute(que)
    row = cursor.fetchall()
    for i in row:
        x=[]
        for e in i:
            try:
                e = e.replace(';','0x3B')
                x.append(e)
            except:
                x.append(e)
        todays_excel_file.writerow(x)
    que1 = 'SELECT * from author'
    cursor.execute(que1)
    row1 = cursor.fetchall()
    for j in row1:
        x=[]
        for e in j:
            try:
                e = e.replace(';','0x3B')
                x.append(e)
            except:
                x.append(e)
        todays_excel_file1.writerow(x)
    cursor.close()
    conn.close()


