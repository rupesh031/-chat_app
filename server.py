import socket
import threading
import json
import csv
import ast
import time
f=1
server=socket.gethostbyname(socket.gethostname())
port=9011
addr=(server,port)
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind(addr)
print(server+" binded to {}".format(port))
lock=threading.Lock()
def start():
    global f
    print("[SERVER] Running..... at {}".format(server))
    s.listen(5)
    while True:
        conn,addr=s.accept()
        f=1
        start.thread=threading.Thread(target=handle_client,args=(conn,addr))
        start.thread.start()
        print("Active Connections",threading.activeCount()-1)
def handle_client(conn,addr):
    global f
    handle_client.length=0
    print("[NEW CONNECTION] {}".format(addr),end="\n")
    handle_client.connected=True
    while handle_client.connected:
        while True and f==1:
            d=conn.recv(100)
            if len(d.decode("utf-8")) >0:
                if d.decode("utf-8")=="new_id":
                    new_id(conn,addr)
                else:
                    d=json.loads(d.decode("utf-8"))
                    print(f"[{addr}]",d)
                    f=open("database.csv",'r')
                    reader=csv.reader(f)
                    i=0
                    for rows in reader:
                        if len(rows)>0:
                            if rows[0]==d[0] and rows[1]==d[1]:
                                conn.send("true".encode("utf-8"))
                                chatroom(conn, addr)
                                f=0
                                i=1
                                break
                    if i==0:
                        conn.send("false".encode("utf-8"))
                        print(conn,"closed")
                        pass
            else:
                break


def chatroom(conn,addr,h=0):
    global length
    if h==0:
       u=conn.recv(100)
       u=u.decode("utf-8")
    if h!=0:
        u=h
    f=open("database.csv",'r')
    reader=csv.reader(f)
    l=[]
    for rows in reader:
        try:
            if rows[0]==u:
                print("sent data")
                for j in range(len(rows)):
                    if j >= 2:
                        f1 = ast.literal_eval(rows[j])
                        l.append(f1)
                    else:
                        l.append(rows[j])
        except:
            pass
    send_file_man()
    f.close()
    g=open("sentdata.csv","r")
    l1=[]
    r=csv.reader(g)
    for i in r:
        try:
            if i[0]==u:
                print("retriving sent data")
                for j in range (len(i)):
                    if j>=1:
                        f=ast.literal_eval(i[j])
                        l1.append(f)
                    else:
                        l1.append(i[j])
        except:
            pass
    g.close()
    d=[l,l1]
    print(d)
    conn.send(json.dumps(d).encode())
    #length=len(rows)
    #sthread=threading.Thread(target=send_data,args=(conn,addr,u))
    #sthread.start()
    #send_data(conn,addr,u)
    if h==0:
        threads=threading.Thread(target=rec,args=(u,conn,addr))
        threads.start()
        """th=threading.Thread(target=inbox,args=(u,conn,addr,d[0]))
        th.start()"""
    #rec(u,conn,addr)

def new_id(conn,addr):
    d=conn.recv(100)
    d=json.loads(d.decode("utf-8"))
    f=open("database.csv",'a+')
    writer=csv.writer(f)
    d.append([])
    writer.writerow(d)
    conn.send("ID CREATED".encode("utf-8"))
    f.close()
    g=open("sentdata.csv","a+")
    writer=csv.writer(g)
    writer.writerow(d[0:1])
    g.close()


def rec(u,conn,addr):
    rec.len=0
    while True:
        d=conn.recv(100)
        try:
            a=len(json.loads(d.decode("utf-8")))>0
        except Exception:
            print(u,"connection closed")
            # conn.close()
            # break
            a=False

        if a:
            d=json.loads(d.decode("utf-8"))
            if d[0]=="add_friend":
                f=f=open("database.csv",'r')
                reader=csv.reader(f)
                datas=[]
                c=0
                c1=0
                for rows in reader:
                    try:
                        if len(rows)>0:
                            if rows[0]==d[1]:
                                c=1         
                    except:
                        print("read out of bound")
                f.close()
                if c==0:
                    s=["not exist"]
                    conn.send(json.dumps(s).encode("utf-8"))
                    
                
                elif c==1:
                    f=open("database.csv",'r')
                    reader=csv.reader(f)
                    datas=[]
                    l=[]
                    for rows in reader:
                        if len(rows)>0:
                            if rows[0]==u:
                                for i in range (len(rows)):
                                    if i==2:
                                        print(rows[i])
                                        m=ast.literal_eval(rows[i])
                                        if d[1] not in m:
                                            m.append(d[1])
                                        else:
                                            c1=1
                                        l.append(m)
                                    else:
                                        l.append(rows[i])
                                datas.append(l)
                            else:
                                datas.append(rows)
                    print(datas)
                    f=open('database.csv','w+')
                    writer=csv.writer(f)
                    writer.writerows(datas)
                    f.close()
                    if c1==0:
                        s=["exist"]
                        conn.send(json.dumps(s).encode("utf-8"))
                    else:
                        s=["no need"]
                        conn.send(json.dumps(s).encode("utf-8"))
            elif d[0]=="need":
                print("reached")
                chatroom(conn,addr,h=u)
            else:
                print("block found",u)
                f=open("database.csv",'r')
                reader=csv.reader(f)
                datas=[]
                for rows in reader:
                    if len(rows)>0:
                        if rows[0]==d[0]:
                            l=[u,d[1]]
                            print(l)
                            rows.append(l)
                            datas.append(rows)
                        else:
                            datas.append(rows)
                f.close()
                f=open('database.csv','w+')
                writer=csv.writer(f)
                writer.writerows(datas)
                f.close()
                g=open("sentdata.csv","r")
                reader=csv.reader(g)
                data=[]
                for row in reader:
                    print(row)
                    if len(row)>0:
                        if row[0]==u:
                            row.append(d)
                            data.append(row)
                        else:
                            data.append(row)
                print("storing sent data",data)
                g=open("sentdata.csv","w+")
                writer=csv.writer(g)
                writer.writerows(data)
                g.close()
                send_file_man()


def file_man(i=0):
    f=open("database.csv","r")
    reader=csv.reader(f)
    data=[]
    for rows in reader:
        try:
            if len(rows[0])>0:
                l=[]
                for i in rows:
                    if len(i)>0:
                        l.append(i)
                data.append(l)
            else:
                pass
        except:
            pass
    for i in data:
        l=[]
        for j in range (len(i)):
            if j>=2:
                l.append(i[j])
            else:
                l.append(i[j])
        data.append(l)
    f.close()
    if i==0:
        f=open('database.csv',"w")
        writer=csv.writer(f)
        writer.writerows(data)
    elif i==1:
        return data


def send_data(conn,addr,u):
    f=open("database.csv",'r')
    reader=csv.reader(f)
    l=[]
    for i in reader:
        if i[0]==u:
            if len(i)>handle_client.length:
                handle_client.length=len((i))
                for j in range (len(i)):
                    if j>=2:
                        f1=ast.literal_eval(i[j])
                        l.append(f1)
                    else:
                        l.append(i[j])
    f.close()
    g=open("sentdata.csv","r")
    l1=[]
    r=csv.reader(g)
    for i in r:
        if i[0]==u:
            try:
                print("sent data")
                print(i)
                for j in range (len(i)):
                    if j>=1:
                        f=ast.literal_eval(i[j])
                        l1.append(f)
                    else:
                        l1.append(i[j])
            except:
                break
    g.close()
    d=[l,l1]
    print(d)
    conn.send(json.dumps(d).encode("utf-8"))

def send_file_man():
    """s=open("sentdata.csv","r")
    r=csv.reader(s)
    msg=[]
    for i in r:
        l=[]
        try:
            a=i[0]
            if a.isalpha():
                for j in i:
                    if len(j)!=0:
                        l.append(j)
                msg.append(l)
        except:
            pass
    s.close()
    s=open("sentdata.csv","w")
    w=csv.writer(s)
    w.writerows(msg)
    s.close()"""

"""def inbox(u,conn,addr,d):
    print("inbox????????????????",d)
    inbox_len=len(d)
    f=0
    while True:
        t=[]
        s=file_man(i=1)
        if f==0:
            print(s)
            f=1
        le=0
        t=[]
        for i in s:
            if i[0]==u:
                le=len(i)
                t=i
        if le>inbox_len:
            rec.len=le
            print(".................length has inc",t)
            #conn.send(json.dumps(t).encode("utf-8"))
        else:
            time.sleep(10)"""
        
        


start()

