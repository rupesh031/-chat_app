# chat box
import tkinter as tk
import socket
import threading
import json
import ast
from tkinter import messagebox
from functools import partial
import time
global fr
l=0
wn = 0
client = 0
port=9011
#server = socket.gethostbyname(socket.gethostname())
server="127.0.1.1"
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
addr = (server, port)
client.connect(addr)
text = "a"
t = ""
y = 0
g = ""
user = ""
chat = []
data = []
schat = []
rchat = []
label = []
labelr = []
chat = []
shis = []
length = 0
in_room=False
use_poss=True
friend_added=False

def first():
    global wn
    wn = tk.Tk()
    wn.geometry("800x600")
    wn.title("MY CHAT BOX")
    wn.resizable(0,0)
    label = tk.Label(wn, text="USER LOGIN", font=("Courier", 30, "normal"), borderwidth=8)
    label.pack()

    label1 = tk.Label(wn, text="USER ID", font=("Courier", 20, "normal"))
    label1.place(relx=0.48, rely=0.3, anchor="center")
    first.sender = tk.Entry(wn, width=30, borderwidth=8, font=("Arial", 15, "normal"))
    first.sender.place(relx=0.5, rely=0.4, anchor="center")

    label1 = tk.Label(wn, text="PASSWORD", font=("Courier", 20, "normal"))
    label1.place(relx=0.48, rely=0.55, anchor="center")
    first.password = tk.Entry(wn, width=30, borderwidth=8, font=("Arial", 15, "normal"))
    first.password.place(relx=0.5, rely=0.65, anchor="center")

    label2 = tk.Button(wn, text="CREATE ID", font=("Arial", 12, "normal"), command=create_Id)
    label2.place(relx=0.48, rely=0.9, anchor="center")

    label3 = tk.Button(wn, text="LOGIN", font=("Arial", 12, "normal"), command=login)
    label3.place(relx=0.48, rely=0.75, anchor="center")

    wn.mainloop()


def lobby(i=0):
    global wn
    global y
    global data
    global shis
    global use_poss
    wn = tk.Tk()
    wn.geometry("800x600")
    wn.title("MY CHAT BOX")
    wn.resizable(0,0)
    label1 = tk.Label(wn, text=user, font=("arial", 25, "normal"), fg="red", bg="black", padx=800)
    label1.place(relx=0.5, rely=.05, anchor="center")
    if i == 0:
        client.send(user.encode("utf-8"))
        d = client.recv(10000)
        # threadr=threading.Thread(target=receiving_data)
        # threadr.start()
        # receiving_data()
        x = json.loads(d.decode())
        data = x[0]
        shis = x[1]
        print("sent history ", shis)
    add = tk.Button(wn, text="ADD FRIEND", font=("arial", 12, "normal"), fg="black", bg="grey", command=add_friends)
    add.place(relx=0.98, rely=0.16, anchor="e")
    friends_list = data[2]
    lobby.y = 0.2
    button = []
    for i in range(len(friends_list)):
        button.append(tk.Button(wn, text=friends_list[i], font=("arial", 20, "normal"), fg="white", bg="black",
                                command=partial(room, friends_list[i])))
        button[i].place(relx=0.05, rely=lobby.y, anchor="w")
        lobby.y += 0.2
    y = 0.8
    th = threading.Thread(target=chk_msg)
    th.start()
    wn.update()
    #wn.protocol("WM_DELETE_WINDOW", on_close)
    wn.mainloop()


def room(c):
    global g
    global text
    global wn
    global data
    global rchat
    global chat
    global schat
    global fr
    global shis
    global in_room
    global use_poss
    in_room=True
    use_poss=False
    he=["need"]
    client.send(json.dumps(he).encode("utf-8"))
    d = client.recv(100000)
    x = json.loads(d.decode("utf-8"))
    data = x[0]
    shis = x[1]
    print("..........recieved",x)
    use_poss=True
    schat = []
    label = []
    man_chat()
    g = c
    wn.destroy()
    wn = tk.Tk()
    wn.geometry("800x600")
    wn.title(c)
    wn.resizable(0,0)
    for i in shis[1:]:
        if i[0] == c:
            schat.append(i[1])
    print(schat)
    try:
        room.f1 = tk.Frame(room.scroll_frame, bd=1, relief="sunken", bg="purple")
        room.f2 = tk.Frame(room.scroll_frame, bd=1, relief="sunken", bg="blue")
    except:
        pass
    
    frame = tk.Frame(wn,width=800, height=550)
    frame.place(x=0, y=0.9, relwidth=1, relheight=0.9)
    
    canvas = tk.Canvas(frame)
    canvas.pack(side="left", fill="both", expand=True)
    
    scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")
    
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion= canvas.bbox("all")))
    
    room.scroll_frame = tk.Frame(canvas,width=800, height=2200,bg="yellow")
    canvas.create_window((0, 0), window=room.scroll_frame, anchor="nw")
    
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    room.f1 = tk.Frame(room.scroll_frame, bd=1, relief="sunken", bg="purple")
    room.f2 = tk.Frame(room.scroll_frame, bd=1, relief="sunken", bg="blue")
    #canvas.update_idletasks()
    #canvas.yview_moveto('1.0')
    fr = room.scroll_frame
    split = 0.5
    room.f1.place(relx=0, relheight=1, relwidth=split)
    room.f2.place(relx=split, relheight=1.0, relwidth=1 - split)
    print(threading.active_count())
    chk_inbox(c)

    def inter(i=1):
        global t
        global y
        global schat
        #y = 0.95
        y=2160
        if i == 1:
            t = room.entry.get()
            schat.append(t)
            room.entry.delete(0, len(t))
            sends(c,t)

        room.f2 = tk.Frame(room.scroll_frame, bd=1, relief="sunken", bg="blue")
        room.f2.place(relx=split, relheight=1.0, relwidth=1 - split)
        for l in schat:
            label.append(tk.Label(room.f2, text=l, font=("arial", 15, "normal"), fg="red", bg="black"))
        for i in range(len(label) - 1, -1, -1):
            label[i].place(x=360,y=y, anchor="e")
            y -= 60
        #thread = threading.Thread(target=sends, args=(c, t))
        #thread.start()

    inter(0)
    room.entry = tk.Entry(wn, font=("arial", 20, "normal"), fg="white", bg="green", borderwidth=5, width=47)
    room.entry.place(relx=0, rely=0.95, anchor="w")
    button = tk.Button(wn, text="Send", font=("arial", 15, "normal"), fg="white", bg="black", command=inter)
    button.place(relx=0.9, rely=0.95, anchor="w")
    button = tk.Button(wn, text="back", font=("arial", 15, "normal"), fg="white", bg="black", command=back)
    button.place(relx=0.5, rely=0.05, anchor="center")
    wn.update()
    #wn.protocol("WM_DELETE_WINDOW", on_close)
    wn.mainloop()
    
def on_close():
	global wn
	global client
	global use_poss
	if messagebox.askokcancel("Exit","Do You Want To Quit?"):
		client.close()
		wn.destroy()
		exit()


def sends(c, t):
    m = [c, t]
    print(m)
    m1 = (json.dumps(m).encode("utf-8"))
    client.send(m1)


def dis_rt():
    global wn
    global rchat
    global labelr
    labelr=[]
    room.f1 = tk.Frame(room.scroll_frame, bd=1, relief="sunken", bg="purple")
    room.f1.place(relx=0, relheight=1, relwidth=0.5)
    y = 2160
    for l in rchat:
        labelr.append(tk.Label(room.f1, text=l, font=("arial", 15, "normal"), fg="red", bg="black"))
    for i in range(len(labelr) - 1, -1, -1):
        labelr[i].place(x=40,y=y, anchor="w")
        y -= 60
    y = 2160
    wn.update()


def login():
    global user
    m1 = [first.sender.get(), first.password.get()]
    user = m1[0]
    m1 = json.dumps(m1)
    message = m1.encode("utf-8")
    client.send(message)
    receiving()


def receiving():
    global wn
    global client
    global server
    global addr
    key = client.recv(100)
    if len(key.decode("utf-8")) > 0:
        key = key.decode()
        print(key)
        if key == "true":
            wn.destroy()
            lobby(0)
        else:
            messagebox.showinfo("message", "LOGIN FAILED: Try again")
            t1 = time.perf_counter()
            s=True
            while s:
                t2=time.perf_counter()
                if t2-t1>=1:
                    wn.destroy()
                    client.close()
                    #server = socket.gethostbyname(socket.gethostname())
                    server="127.0.1.1"
                    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    addr = (server, port)
                    client.connect(addr)
                    first()
                    break
            


def create_Id():
    global wn
    wn.destroy()
    wn = tk.Tk()
    wn.geometry("800x600")
    label = tk.Label(wn, text="CREATING USER ID", font=("Courier", 30, "normal"), borderwidth=8)
    
    wn.resizable(0,0)
    label.pack()

    label1 = tk.Label(wn, text="USERNAME", font=("Courier", 20, "normal"))
    label1.place(relx=0.48, rely=0.3, anchor="center")
    create_Id.Id = tk.Entry(wn, width=30, borderwidth=8, font=("Arial", 15, "normal"))
    create_Id.Id.place(relx=0.5, rely=0.4, anchor="center")

    label = tk.Label(wn, text="PASSWORD", font=("Courier", 20, "normal"))
    label.place(relx=0.48, rely=0.6, anchor="center")
    create_Id.password = tk.Entry(wn, width=30, borderwidth=8, font=("Arial", 15, "normal"))
    create_Id.password.place(relx=0.5, rely=0.7, anchor="center")

    label3 = tk.Button(wn, text="SIGNUP", font=("Arial", 12, "normal"), command=signup)
    label3.place(relx=0.48, rely=0.85, anchor="center")
    label3 = tk.Button(wn, text="BACK TO LOGIN PAGE", font=("Arial", 10, "normal"), command=first)
    label3.place(relx=0.48, rely=0.95, anchor="center")
    wn.mainloop()


def signup():
    global wn
    client.send("new_id".encode("utf-8"))
    m1 = [create_Id.Id.get(), create_Id.password.get()]
    m1 = json.dumps(m1)
    message = m1.encode("utf-8")
    client.send(message)
    rc = client.recv(150)
    rc = rc.decode("utf-8")
    messagebox.showinfo("message", rc)
    wn.destroy()
    first()


def add_friends():
    global wn
    add_friends.nf = tk.Entry(wn, width=20, borderwidth=3, font=("Arial", 10, "normal"))
    add_friends.nf.place(relx=0.98, rely=0.22, anchor="e")
    add_friends.b = tk.Button(wn, text="ADD", font=("Arial", 8, "normal"), command=new_f)
    add_friends.b.place(relx=0.93, rely=0.28, anchor="center")
    add_friends.b1=tk.Button(wn,text="Cancel",font=("Arial", 8, "normal"), command=cancel_new)
    add_friends.b1.place(relx=0.85,rely=0.28, anchor="center")

def new_f():
    global use_poss
    global friend_added
    global data
    use_poss=False
    n = add_friends.nf.get()
    l = ["add_friend", n]
    m1 = (json.dumps(l).encode("utf-8"))
    client.send(m1)
    d = client.recv(100)
    use_poss=True
    d = json.loads(d)
    print(d)
    if d[0] == "exist":
        messagebox.showinfo("message", "Adding Friend: Please Wait")
        he=["need"]
        client.send(json.dumps(he).encode("utf-8"))
        sf = client.recv(1000)
        x = json.loads(sf.decode("utf-8"))	
        data=x[0]
        print("data recievied...................",x)
        back()
        
    elif d[0]=="not exist":
        messagebox.showinfo("message", "User not found")
    elif d[0]=="no need":
        messagebox.showinfo("message", "Already Present in Frined list")
    
    
def cancel_new():
	add_friends.nf.destroy()
	add_friends.b.destroy()
	add_friends.b1.destroy()
	



def man_chat():
    global chat
    global data
    chat = []
    for i in range(3, len(data)):
        if len(data[i]) > 0:
            l = data[i]
            chat.append(l)
    print(chat)


def chk_inbox(c):
    global length
    global rchat
    print(c)
    rchat = []
    for l in chat:
        if l[0] == c:
            rchat.append(l[1])
    print(rchat)
    dis_rt()
    # if len(rchat)>length:
    # dis_rt()
    # length=len(rchat)


def back():
    global wn
    global in_room
    global use_poss
    in_room=False
    wn.destroy()
    lobby(1)
    use_poss=True

def notify(h1):
    def close_not():
        notify.label.destroy()
        print("label destroyed")
    global wn
    global g
    print("notify",h1)
    n=[]
    for i in h1:
        if i[0] not in n:
            if (not in_room):
                n.append(i[0])
            else:
                if i[0]!=g:
                    n.append(i[0])
    print(n)
    q="You have text from: "
    for j in n:
        q=q+j+","
    q=q[:-1]
    print(q)
    if len(n)>0:
        notify.label = tk.Label(wn, text=q, font=("Courier", 10, "normal"))
        notify.label.place(relx=0.45, rely=0.03, anchor="w")
        t1 = time.perf_counter()
        s=True
        while s:
            t2=time.perf_counter()
            if t2-t1>=2:
                notify.label.destroy()
                print("destroyed",t2-t1)
                s=False
        print("broken ")

def chk_msg():
    f=0
    global g
    global l
    global data
    global friend_added
    global wn
    while True:
        if use_poss:
            he=["need"]
            client.send(json.dumps(he).encode("utf-8"))
            d = client.recv(100000)
            x = json.loads(d.decode("utf-8"))	
            try:
                if l<len(x[0]):
                    if f==1:
                        print(x[0][l:])
                        print("sleeping........data........you have unread msg.........\n \n")
                        h=x[0][l:]
                        l=len(x[0])
                        data=x[0]
                        if in_room:
                            flag=False
                            print("in room with ",g)
                            for i in h:
                                if i[0]==g:
                                    flag=True
                            if flag:
                                print("checking inbox")
                                man_chat()
                                chk_inbox(g)
                        notify(h)
                    l=len(x[0])
                    f=1
            except Exception:
                print("reciving thread error........................")
            time.sleep(5)  
first()
