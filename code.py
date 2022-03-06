import mysql.connector as s
import datetime
import smtplib
import os

def overwrite_csv():
    conn=s.connect(host='localhost',user='root',passwd=os.environ.get('mysql_pass'),database='bdays')
    cursor=conn.cursor()
    cursor.execute('select * from list')
    sql_data=cursor.fetchall()
    conn.close()
    with open('csv.csv','w') as f:
        f.write('fname,email,bday\n')
        for i in sql_data:
            f.write('{},{},{}\n'.format(i[0],i[1],i[2]))

def overwrite_database():
    conn=s.connect(host='localhost',user='root',passwd=os.environ.get('mysql_pass'),database='bdays')
    cursor=conn.cursor()
    cursor.execute('drop table list')
    cursor.execute('create table list(fname char(20), email char(40), bday date)')
    conn.close()
    with open('csv.csv','r') as f:
        csv_data=f.readlines()
    for i in range(1,len(csv_data)):
        x=csv_data[i].split(',')
        add(x[0],x[1],x[2][0:-2])

def export_to_csv():
    conn=s.connect(host='localhost',user='root',passwd=os.environ.get('mysql_pass'),database='bdays')
    cursor=conn.cursor()
    cursor.execute('select * from list')
    sql_data=cursor.fetchall()
    conn.close()
    with open('csv.csv','r') as f:
        csv_data=f.readlines()
    names=[]
    for i in csv_data:
        x=i.split(',')
        names+=[x[0]]
    del names[0]
    with open('csv.csv','a') as f:
        for i in sql_data:
            if i[0] not in names:
                f.write('{},{},{}\n'.format(i[0],i[1],i[2]))

def import_from_csv():
    conn=s.connect(host='localhost',user='root',passwd=os.environ.get('mysql_pass'),database='bdays')
    cursor=conn.cursor()
    with open('csv.csv','r') as f:
        csv_data=f.readlines()
    cursor.execute('select * from list')
    sql_data=cursor.fetchall()
    conn.close()
    names=[]
    for i in sql_data:
        names+=[i[0]]
    for i in range(1,len(csv_data)):
        x=csv_data[i].split(',')
        if x[0] not in names:
            add(x[0],x[1],x[2][0:-2])

def add(name,email,bday):
    conn=s.connect(host='localhost',user='root',passwd=os.environ.get('mysql_pass'),database='bdays')
    cursor=conn.cursor()
    cursor.execute(f"insert into list values('{name}','{email}','{bday}')")
    conn.commit()
    conn.close()
    overwrite_csv()

def delete(name):
    conn=s.connect(host='localhost',user='root',passwd=os.environ.get('mysql_pass'),database='bdays')
    cursor=conn.cursor()
    cursor.execute("delete from list where fname = '{}'".format(name))
    conn.commit()
    conn.close()
    overwrite_csv()

def wish_current():
    conn=s.connect(host='localhost',user='root',passwd=os.environ.get('mysql_pass'),database='bdays')
    cursor=conn.cursor()
    cursor.execute('select * from list')
    f=cursor.fetchall()
    x=datetime.date.today()
    for i in f:
        if i[2].day==x.day and i[2].month==x.month:
            send_wishmail(i[0],i[1])
    conn.close()

def send_wishmail(name,email):
    address=os.environ.get('email_id')
    password=os.environ.get('email_pass')
    with smtplib.SMTP('smtp.gmail.com',587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

        smtp.login(address,password)

        subject = 'Happy Birthday {}!'.format(name)
        body = 'Many happy returns of the day to you!'

        msg = f'Subject: {subject}\n\n{body}'

        smtp.sendmail(address,email,msg)