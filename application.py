from flask import Flask, render_template, request, jsonify
import os
import pyodbc
import time
import redis
import random



from flask import Flask
app = Flask(__name__)

Creds=[]
Name='Akshay Shenvi'
UtaID='1001670648'
Creds.append([UtaID,Name])

def randrange_float(start, stop, step):
    return random.randint(0, int(round(abs(((stop - start) / step)))))

def sqlconn(sqlQuery):
    #try:

    server = 'akshayshenvi.database.windows.net'
    database = 'Earthquakes'
    username = 'akshay@akshayshenvi'
    password = 'Akshata1992'
    driver= '{ODBC Driver 17 for SQL Server}'
    connection = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = connection.cursor()
    # if num == None:
    #     num= 1

    # for i in range(num):
    cursor.execute(sqlQuery)
    row = cursor.fetchall()
    # while row:
    #     row = cursor.fetchone()
    return row

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


# def sqlconnwithredis(sqlQuery,num=None,method="Both"):
#     #try:
#     myHostname = "akshay.redis.cache.windows.net"
#     myPassword = "JehPyQGvHgF20jSqBN0k9n6sAgGDGaMSgaoKnO3DoXY="
#     r = redis.StrictRedis(host=myHostname, port=6380,password=myPassword,ssl=True)
#     key="SQL:"+sqlQuery
#     server = 'akshayshenvi.database.windows.net'
#     database = 'Earthquakes'
#     username = 'akshay@akshayshenvi'
#     password = 'Akshata1992'
#     driver= '{ODBC Driver 17 for SQL Server}'
#     connection = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
#     cursor = connection.cursor()
#     #Without Redis
#     elapsedWithoutRedis=[]
#     elapsedWithRedis=[]
#     if num == None:
#         num= 1
#     if method=="Without redis":
#         for i in range(num):
#             wotic=time.time()
#             cursor.execute(sqlQuery)
#             wotoc=time.time()
#             elapsedWithoutRedis.append(wotoc-wotic)
            

#         row = cursor.fetchall()
#         if not r.exists(key):
#                 r.set(key,str(row[0]))
#         return elapsedWithoutRedis,elapsedWithRedis,row
    
#     #elapsedworedis.append(wotoc-wotic)

#     #With Redis
#     elif method=="With redis":
        
        
#         #cursor = connection.cursor()
#         if num == None:
#             num= 1
        
#         for i in range(num):
            
#             if r.get(key):
                
#                 wtic=time.time()
#                 row=r.get(key)
#                 wtoc=time.time()
#                 row=row.decode("utf-8")
#                 row=int(row[1:-3])
#                 #print("Redis working")
#             else:
#                 wtic=time.time()
#                 cursor.execute(sqlQuery)
#                 wtoc=time.time()
#                 row = cursor.fetchall()
#                 r.set(key,str(row[0]))
                
#                 #r.expire()
#                 #print("Not found in redis")
            
#             elapsedWithRedis.append(wtoc-wtic)
#         return elapsedWithoutRedis,elapsedWithRedis,row
    
#     elif method=="Both":
#         for i in range(num):
#             wotic=time.time()
#             cursor.execute(sqlQuery)
#             wotoc=time.time()
#             elapsedWithoutRedis.append(wotoc-wotic)
            
#         row = cursor.fetchall()
#         if not r.exists(key):
#                 r.set(key,str(row[0]))

        
        
#         #cursor = connection.cursor()
#         if num == None:
#             num= 1
        
#         for i in range(num):
            
#             if r.get(key):
#                 wtic=time.time()
#                 row=r.get(key)
#                 wtoc=time.time()
#                 row=row.decode("utf-8")
                
#                 row=int(row[1:-3])
                
                
#                 #print("Redis working")
#             else:
#                 wtic=time.time()
#                 cursor.execute(sqlQuery)
#                 wtoc=time.time()
#                 row = cursor.fetchall()
#                 r.set(key,str(row))
#                 #r.expire()
#                 #print("Not found in redis")
            
#             elapsedWithRedis.append(wtoc-wtic)
#         return elapsedWithoutRedis,elapsedWithRedis,row



   

    # except:
    #     return("Connection Failed, Try Again.")

@app.route("/")
def hello():
    return render_template("index.html",creds=Creds)

@app.route("/connect")
def randomQuery():
    sqlQuery= request.args.get('query')
    print(sqlQuery)
    num = int(request.args.get('num'))
    #sqlQuery= "SELECT * FROM QUAKES;"
    tic= time.time()

    row=sqlconn(sqlQuery,num)
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
    row=sqlconn(sqlQuery,num)
    toc = time.time()
    timeelapsed =toc-tic
    return render_template("showrecords.html",result=timeelapsed)


# @app.route("/complexredis")
# def complexquerywithredis():
#     magfrom= request.args.get('magfrom','')
#     magto= request.args.get('magto','')
#     num = int(request.args.get('num',''))
#     sqlQuery= "SELECT * FROM QUAKES WHERE mag BETWEEN "+magfrom+" AND "+magto+" ;"

#     data=[]
#     elapsedworedis,elapsedwithredis=sqlconnwithredis(sqlQuery,num)
#     data.append([elapsedworedis,elapsedwithredis])
    

#     return render_template("showredis.html",data=data)
@app.route("/group")
def groupbyclause():
    sqlQuery="select count(*) as cnt , mag from QUAKES where mag between 1 and 2  group by mag having count(*) >= 100;"
    row,acttime=connectAndQueryRun(sqlQuery)
    print(row)
    return render_template('showsomechart.html',creds=Creds,result=row)

@app.route("/showdate")
def showdate():
    sqlQuery="select  Count(*),CONVERT(VARCHAR(10), TIME, 111) from QUAKES Group by CONVERT(VARCHAR(10), TIME, 111);"
    row,acttime=connectAndQueryRun(sqlQuery)
    print(row)
    return render_template('datechart.html',creds=Creds,result=row)

@app.route("/magrange")
def magrange():
    magfrom = request.args.get('magfrom','')
    magto= request.args.get('magto','')
    step = request.args.get('step','')
    chart= request.args.get('chart','')
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
    return render_template('showrecords.html',creds=Creds,result=result,chart=chart)

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


# @app.route('/practicequiz')
# def rangewithmag():
#     latfrom = float(request.args.get('latfrom',''))
#     latto= float(request.args.get('latto',''))
#     count = int(request.args.get('count',''))
#     method= str(request.args.get('redisopt',''))
#     #interval= float(request.args.get('interval',''))
#     # myHostname = "akshay.redis.cache.windows.net"
#     # myPassword = "JehPyQGvHgF20jSqBN0k9n6sAgGDGaMSgaoKnO3DoXY="
    
#     # r = redis.StrictRedis(host=myHostname, port=6380,password=myPassword,ssl=True)
#     timeli=[]
#     data=[]
#     randnumbers=[]
#     timeWithoutRedis=[]
#     timeWithRedis=[]
#     withoutRedis=0
#     withRedis=0
#     #timewithOutRedis=0
#     #timewithRedis=0
#     totaltime=0

#     for i in range(count):
        
#         randomnumfrom = round((random.uniform(float(latfrom),float(latto))),1)
#         randomnumto = round((random.uniform(float(latfrom),float(latto))),1)
#         #print(randomnumfrom,randomnumto)
        
#         if float(randomnumfrom)>float(randomnumto):
#             temp=randomnumfrom
#             randomnumfrom=randomnumto
#             randomnumto=temp
#         sqlQuery = "select count(*) from QUAKES1 where latitude BETWEEN '"+str(randomnumfrom)+"' AND '"+str(randomnumto)+"';"
#         timeWithoutRedis,timeWithRedis,row=sqlconnwithredis(sqlQuery,1,method)
#         if len(timeWithoutRedis)==0:
#             withoutRedis=None
#         else:
#             for i in timeWithoutRedis:
#                 withoutRedis+=i
#         if len(timeWithRedis)==0:
#             withRedis=None
#         else:
#             for i in timeWithRedis:
#                 withRedis+=i
        
#         # key="SQL:"+sqlQuery
#         # tic=time.time()
#         # #row=sqlconn(sqlQuery)
        


#         # if r.get(key):
            
#         #     value=r.get(key)
            
            
#         #     print("Redis working")
#         # else:
            
#         #     row=sqlconn(sqlQuery)
            
            
#         #     r.set(key,str(row))
#         #     #r.expire()
#         #     print("Not found in redis")
#         # toc=time.time()
#         #print(row)

#         if isinstance(row, int):

#             randnumbers.append([randomnumfrom,randomnumto,row])
#         else:
#             randnumbers.append([randomnumfrom,randomnumto,row[0][0]])
        
#         # if len(row) ==0:
#         #     continue
#         # else:
#         #     #print(row[0])
#         #     data.append(row[0])
#         # time1=toc-tic
#         # totaltime+=time1
#         # timeli.append(time1)
#     #print(randnumbers)



#         #elapsedWithoutRedis,elapsedWithRedis=sqlconnwithredis(sqlQuery,1)
#         #print(elapsedWithoutRedis[0],elapsedWithRedis[0])
#         #timewithOutRedis+=elapsedWithoutRedis[0]
#         #timewithRedis+=elapsedWithRedis[0]
#         #time.append([elapsedWithoutRedis[0],elapsedWithRedis[0]])
    
#     return render_template('something.html',withoutRedis=withoutRedis,withRedis=withRedis,randnumbers=randnumbers)


# @app.route('/practicequiz')
# def rangewithmag():
#     magfrom = float(request.args.get('magfrom',''))
#     magto= float(request.args.get('magto',''))
#     count = int(request.args.get('count',''))
#     interval= float(request.args.get('interval',''))
#     time=[]
#     timewithOutRedis=0
#     timewithRedis=0
#     for i in range(count):
#         random_num=randrange_float(magfrom,magto,interval)
#         sqlQuery = "select place from QUAKES where mag = '"+str(random_num)+"';"
#         elapsedWithoutRedis,elapsedWithRedis=sqlconnwithredis(sqlQuery,1)
#         #print(elapsedWithoutRedis[0],elapsedWithRedis[0])
#         timewithOutRedis+=elapsedWithoutRedis[0]
#         timewithRedis+=elapsedWithRedis[0]
#         time.append([elapsedWithoutRedis[0],elapsedWithRedis[0]])
    
#     return render_template('something.html',time=time,withOutRedis=timewithOutRedis,withRedis=timewithRedis)
         

port = os.getenv('PORT', '8000')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(port))
