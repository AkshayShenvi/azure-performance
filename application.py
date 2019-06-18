from flask import Flask, render_template, request, jsonify
import os
import pyodbc
import time
import redis
import random



from flask import Flask
app = Flask(__name__)

def randrange_float(start, stop, step):
    return random.randint(0, int(round(abs(((stop - start) / step)))))

def sqlconn(sqlQuery,num):
    #try:

    server = 'akshayshenvi.database.windows.net'
    database = 'Earthquakes'
    username = 'akshay@akshayshenvi'
    password = 'Akshata1992'
    driver= '{ODBC Driver 17 for SQL Server}'
    connection = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = connection.cursor()
    if num == None:
        num= 1

    for i in range(num):
        cursor.execute(sqlQuery)
    row = cursor.fetchone()
    while row:
        row = cursor.fetchone()
    return None

def connectAndQueryRun(sqlQuery):
    server = 'akshayshenvi.database.windows.net'
    database = 'Earthquakes'
    username = 'akshay@akshayshenvi'
    password = 'Akshata1992'
    driver= '{ODBC Driver 17 for SQL Server}'
    connection = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
    
    cursor = connection.cursor()
    tic= time.time()
    cursor.execute(sqlQuery)
    toc= time.time()
    acttime=toc-tic
    row = cursor.fetchall()
    #print(row[0][0])
    return row, acttime


def sqlconnwithredis(sqlQuery,num):
    #try:

    server = 'akshayshenvi.database.windows.net'
    database = 'Earthquakes'
    username = 'akshay@akshayshenvi'
    password = 'Akshata1992'
    driver= '{ODBC Driver 17 for SQL Server}'
    connection = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = connection.cursor()
    #Without Redis
    elapsedworedis=[]
    elapsedwithredis=[]
    if num == None:
        num= 1

    for i in range(num):
        wotic=time.time()
        cursor.execute(sqlQuery)
        wotoc=time.time()
        elapsedworedis.append(wotoc-wotic)
    row = cursor.fetchall()
    
    #elapsedworedis.append(wotoc-wotic)

    #With Redis
    myHostname = "akshay.redis.cache.windows.net"
    myPassword = "JehPyQGvHgF20jSqBN0k9n6sAgGDGaMSgaoKnO3DoXY="
    r = redis.StrictRedis(host=myHostname, port=6380,password=myPassword,ssl=True)
    #cursor = connection.cursor()
    if num == None:
        num= 1
    key="SQL:"+sqlQuery
    for i in range(num):
        
        if r.get(key):
            wtic=time.time()
            value=r.get(key)
            wtoc=time.time()
            
            print("Redis working")
        else:
            wtic=time.time()
            cursor.execute(sqlQuery)
            wtoc=time.time()
            row = cursor.fetchall()
            r.set(key,str(row))
            #r.expire()
            print("Not found in redis")
           
        elapsedwithredis.append(wtoc-wtic)


    return elapsedworedis,elapsedwithredis

    # except:
    #     return("Connection Failed, Try Again.")

@app.route("/")
def hello():
    return render_template("index.html",)

@app.route("/connect")
def randomQuery():
    sqlQuery= request.args.get('query')
    print(sqlQuery)
    num = int(request.args.get('num'))
    #sqlQuery= "SELECT * FROM QUAKES;"
    tic= time.time()

    sqlconn(sqlQuery,num)
    toc= time.time()
    timeelapsed = toc-tic
    return render_template("showrecords.html",result=timeelapsed)


@app.route("/complex")
def complexquery():
    magfrom= request.args.get('magfrom','')
    magto= request.args.get('magto','')
    num = int(request.args.get('num',''))
    sqlQuery= "SELECT * FROM QUAKES WHERE mag BETWEEN "+magfrom+" AND "+magto+" ;"
    tic = time.time()
    sqlconn(sqlQuery,num)
    toc = time.time()
    timeelapsed =toc-tic
    return render_template("showrecords.html",result=timeelapsed)


@app.route("/complexredis")
def complexquerywithredis():
    magfrom= request.args.get('magfrom','')
    magto= request.args.get('magto','')
    num = int(request.args.get('num',''))
    sqlQuery= "SELECT * FROM QUAKES WHERE mag BETWEEN "+magfrom+" AND "+magto+" ;"

    data=[]
    elapsedworedis,elapsedwithredis=sqlconnwithredis(sqlQuery,num)
    data.append([elapsedworedis,elapsedwithredis])
    

    return render_template("showredis.html",data=data)


@app.route("/magrange")
def magrange():
    magfrom = request.args.get('magfrom','')
    magto= request.args.get('magto','')
    step = request.args.get('step','')
    if float(magfrom)>float(magto):
        temp=magfrom
        magfrom=magto
        magto=temp
    startmag= float(magfrom)
    stependmag = startmag+float(step)
    result=[]
    while stependmag<=float(magto):
        sqlQuery="SELECT COUNT(*) AS COUNT FROM QUAKES WHERE MAG BETWEEN '"+str(startmag)+"' AND '"+str(stependmag)+"';"
        row,acttime=connectAndQueryRun(sqlQuery)
        print(row[0])
        ans=int(row[0][0])
        result.append([startmag,stependmag,ans])
        startmag+=float(step)
        stependmag+=float(step)
    #print(result[0][0])
    print(result)
    return render_template('showrecords.html',result=result)

@app.route('/scatterlongitude')
def scatterLongitude():
    magfrom = request.args.get('magfrom','')
    magto= request.args.get('magto','')
    loc=[]
    if float(magfrom)>float(magto):
        temp=magfrom
        magfrom=magto
        magto=temp
    sqlQuery="SELECT latitude, longitude FROM QUAKES WHERE MAG BETWEEN '"+str(magfrom)+"' AND '"+str(magto)+"' ;"
    row,acttime=connectAndQueryRun(sqlQuery)
    print(row[0][0])
    for i in row:
        print(i[0])
        lat=float(i[0])
        longitude=float(i[1])
        loc.append([lat,longitude])
    return render_template('scatterlongilati.html',result=loc)




# @app.route('/practicequiz')
# def rangewithmag():
#     magfrom = float(request.args.get('magfrom',''))
#     magto= float(request.args.get('magto',''))
#     count = int(request.args.get('count',''))
#     interval= float(request.args.get('interval',''))
#     i=0
#     timewithoutredis=[]
#     timewithredis=[]
#     totaltime=[]
#     while i< int(count):
#         lower=randrange_float(magfrom,magto,interval)
#         upper=randrange_float(magfrom,magto,interval)
#         if float(lower)>float(upper):
#             temp=lower
#             lower=upper
#             upper=temp
#         steplow=float(lower) 
#         stephigh=steplow+interval
#         #Without Redis 
#         while float(stephigh)<float(upper):
#             sqlQuery="SELECT Count(*) FROM QUAKES WHERE MAG BETWEEN '"+str(lower)+"' AND '"+str(upper)+"' ;"
#             row,noredistime=connectAndQueryRun(sqlQuery)
#             steplow+=float(interval)
#             stephigh+=float(interval)
#             timewithoutredis.append(noredistime)
#         #With Redis
#         while float(stephigh)<float(upper):
#             sqlQuery="SELECT Count(*) FROM QUAKES WHERE MAG BETWEEN '"+str(lower)+"' AND '"+str(upper)+"' ;"
#             myHostname = "akshay.redis.cache.windows.net"
#             myPassword = "JehPyQGvHgF20jSqBN0k9n6sAgGDGaMSgaoKnO3DoXY="
#             r = redis.StrictRedis(host=myHostname, port=6380,password=myPassword,ssl=True)
#             key="SQL:"+sqlQuery
#             if r.get(key):
#                 print("working")
#                 rtic=time.time()
#                 value=r.get(key)
#                 rtoc=time.time()
#                 rtime=rtoc-rtic
#             else:
#                 rtic=time.time()
#                 row,noredistime=connectAndQueryRun(sqlQuery)
#                 r.set(key,str(row))
#                 rtoc=time.time()
#                 rtime=rtoc-rtic

#             steplow+=float(interval)
#             stephigh+=float(interval)
#             timewithredis.append(rtime)
#         i+=1
#     print(len(timewithoutredis))
#     print(len(timewithredis))
#     for i in range(0,len(timewithoutredis)):
#         totaltime.append([timewithoutredis[i],timewithredis[i]])

#     return render_template('something.html',time=totaltime)


@app.route('/practicequiz')
def rangewithmag():
    magfrom = float(request.args.get('magfrom',''))
    magto= float(request.args.get('magto',''))
    count = int(request.args.get('count',''))
    interval= float(request.args.get('interval',''))
    time=[]
    timewithOutRedis=0
    timewithRedis=0
    for i in range(count):
        random_num=randrange_float(magfrom,magto,interval)
        sqlQuery = "select place from QUAKES where mag = '"+str(random_num)+"';"
        elapsedWithoutRedis,elapsedWithRedis=sqlconnwithredis(sqlQuery,1)
        #print(elapsedWithoutRedis[0],elapsedWithRedis[0])
        timewithOutRedis+=elapsedWithoutRedis[0]
        timewithRedis+=elapsedWithRedis[0]
        time.append([elapsedWithoutRedis[0],elapsedWithRedis[0]])
    
    return render_template('something.html',time=time,withOutRedis=timewithOutRedis,withRedis=timewithRedis)
         

port = os.getenv('PORT', '8000')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(port))
