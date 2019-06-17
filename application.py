from flask import Flask, render_template, request, jsonify
import os
import pyodbc
import time
import redis



from flask import Flask
app = Flask(__name__)



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
    cursor.execute(sqlQuery)
    row = cursor.fetchall()
    print(row[0][0])
    return row


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
    data.append(elapsedworedis)
    data.append(elapsedwithredis)

    return render_template("showrecords.html",data=data)


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
        row=connectAndQueryRun(sqlQuery)
        print(int(row[0][0]))
        ans=int(row[0][0])
        result.append([startmag,stependmag,ans])
        startmag+=float(step)
        stependmag+=float(step)
    #print(result[0][0])
    return render_template('showrecords.html',result=result)
        

port = os.getenv('PORT', '8000')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(port))