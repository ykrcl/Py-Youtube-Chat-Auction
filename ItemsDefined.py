import tkinter as tk
import tkinter.font as fonty
from tkinter import simpledialog
from PIL import ImageTk,Image
from pytchat import LiveChatAsync,exceptions
import asyncio
import threading
import datetime
import time as Time
width = 550
height =280

currentbid = 0
minimumbid = 0
currentname= ""
currentitem = "-"
photoadress = ""
time = 0
initialtime=0

totalfund = 0
currentindex = 0

items = []
youtubeid =""


changePhotoFlag = False

class App(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.start()
        
    def callback(self):
        self.root.destroy()
        global exitFlag
        self.is_destroyed = True
        exitFlag = True
    def run(self):
        self.root = tk.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.callback)
        
        self.root.pack_propagate(0)
        self.root.geometry(str(width)+"x"+str(height)) 
        self.root.resizable(0, 0) 
        self.auction = Auction(master=self.root)
        self.is_destroyed = False
        while True:
            global time, timeFlag,changePhotoFlag, currentbid, currentname, currentitem, photoadress, exitFlag
            if not exitFlag:
                self.auction.time['text'] = str(datetime.timedelta(seconds=time))
                self.auction.bid['text'] = str(currentbid) + " TL"
                self.auction.bidder['text'] = currentname
                if changePhotoFlag:
                    self.auction.item['text'] = currentitem
                    try:
                        load = Image.open(photoadress)
                        load = load.resize((350, width), Image.ANTIALIAS)
                    except:
                        load = Image.new("RGB", (350, width), (255, 255, 255))
                    renders = ImageTk.PhotoImage(load)
                    self.auction.item_photo.image = renders
                    changePhotoFlag =False
                self.root.update()
                if exitFlag and not self.is_destroyed:
                    self.root.destroy()


class Auction(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.config(bg="#0180a0")
        self.pack(fill=tk.BOTH,expand=1)
        self.create_widgets()

    def create_widgets(self):
        self.label_bid = tk.Label(self,  text="Highest Bid - En yüksek Teklif:", fg="red")
        self.label_bid["font"] = fonty.Font(family="Helvetica",size=15,weight="bold")
        self.label_bid.place(x=0, y=20, width=width)
        self.bid = tk.Label(self,  text="0 TL", fg="green")
        self.bid["font"] = fonty.Font(family="Helvetica",size=13,slant="italic", underline=True,weight="bold")
        self.bid.place(x=0, y=50, width=width)
        self.label_bidder = tk.Label(self,  text="Bidder - Teklifi Veren:", fg="red")
        self.label_bidder["font"] = fonty.Font(family="Helvetica",size=15,weight="bold")
        self.label_bidder.place(x=0, y=90, width=width)
        self.bidder = tk.Label(self,  text="-", fg="purple")
        self.bidder["font"] = fonty.Font(family="Helvetica",size=14,weight="bold")
        self.bidder.place(x=0, y=120, width=width)
        self.time = tk.Label(self,  text="3:00", fg="red")
        self.time["font"] = fonty.Font(family="Helvetica",size=15,weight="bold")
        self.time.place(x=0, y=150, width=width)
        self.label_item = tk.Label(self,  text="Ürün - Item:", fg="red")
        self.label_item["font"] = fonty.Font(family="Helvetica",size=15,weight="bold")
        self.label_item.place(x=0, y=180, width=width)
        self.item = tk.Label(self,  text=currentitem, fg="brown")
        self.item["font"] = fonty.Font(family="Helvetica",size=14,weight="bold")
        self.item.place(x=0, y=210, width=width)
        try:
            load = Image.open(photoadress)
            load = load.resize((350, width), Image.ANTIALIAS)
        except:
            load = Image.new("RGB", (350, width), (255, 255, 255))
        render = ImageTk.PhotoImage(load)
        self.item_photo = tk.Label(self, image=render)
        self.item_photo.image = render
        self.item_photo.place(x=0, y=235, width= width, height=350)



def nextitem():
    global changePhotoFlag, currentindex, currentitem, photoadress
    if currentindex < len(items)-1:
        currentindex = currentindex + 1
    changePhotoFlag = True
    try:
        currentitem = items[currentindex]["name"]
        photoadress = items[currentindex]["photofile"]
    except:
        pass
    resetitem()
def preitem():
    global changePhotoFlag, currentindex
    if currentindex > 0:
        currentindex = currentindex - 1
    changePhotoFlag = True 
    try:
        currentitem = items[currentindex]["name"]
        photoadress = items[currentindex]["photofile"]
    except:
        pass
    resetitem()
def set_min(app_root):
    global minimumbid
    minimumbid = simpledialog.askinteger("minvalue", "Min?",
                                 parent=app_root,
                                 minvalue=0, maxvalue=100000)
    resetitem()
def savefund(app_root):
    global totalfund, currentbid
    totalfund = totalfund + currentbid
    
    set_min(app_root)
def resetitem():
    global time, currentbid, currentname,timeFlag
    time = initialtime
    currentbid = minimumbid
    currentname = "-"
    timeFlag =False

def starttime():
    global timeFlag
    timeFlag=True

class Admin(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.start()

    def callback(self):
        self.root.destroy()
    
    def run(self):
        self.root = tk.Tk()
        self.root.title("Admin")
        self.root.protocol("WM_DELETE_WINDOW", self.callback)
        self.root.pack_propagate(0)
        self.root.resizable(0, 0) 
        self.adminFrame = AdminFrame(master=self.root)
        self.root.mainloop()
class AdminFrame(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.config()
        self.pack(fill=tk.BOTH,expand=1)
        self.create_widgets()
    
    def create_widgets(self):
         self.next = tk.Button(self, text="set min bid")
        self.next["command"] = lambda: set_min(app_root=self.master)
        self.next.pack()
        self.reset = tk.Button(self, text="save fund")
        self.reset["command"] = lambda: savefund(app_root=self.master)
        self.reset.pack()
        self.next = tk.Button(self, text="next")
        self.next["command"] = lambda: nextitem(app_root=self.master) 
        self.next.pack()
        self.reset = tk.Button(self, text="reset")
        self.reset["command"] = lambda: resetitem(app_root=self.master) 
        self.reset.pack()
        self.previous = tk.Button(self, text="previous")
        self.previous["command"] = lambda: preitem(app_root=self.master) 
        self.previous.pack()
        self.start = tk.Button(self, text="start")
        self.start["command"] = lambda: starttime(app_root=self.master) 
        self.start.pack()
async def func(chatdata):

  for c in chatdata.items:
    global time, initialtime, currentbid, currentname, minimumbid
    print(f"{c.datetime} [{c.author.name}]-{c.message} {c.amountString}")
    if c.message.startswith('+++') and not time == 0 and not time == initialtime:
        cleannumber = c.message.replace("+++","").replace('TL',"").replace('Tl',"").replace('tL',"").replace('tl',"").replace(' ',"")
        if cleannumber.isnumeric():
            if int(cleannumber) > currentbid and int(cleannumber) > minimumbid:
                currentbid = int(cleannumber)
                currentname = c.author.name
                if time < 10:
                    time = time + 8

    await chatdata.tick_async()


async def main():
    try:
        livechat = LiveChatAsync(youtubeid, callback = func)
        while livechat.is_alive() and not exitFlag:
            await asyncio.sleep(0.5)
            #other background operation.
            # if not exitFlag:
            #     app.update()
            # else:
            #     break
            
        # If you want to check the reason for the termination, 
        # you can use `raise_for_status()` function.
        try:
            livechat.raise_for_status()
        except exceptions.ResponseContextError:
            print("Chat data finished.")
        except Exception as e:
            print(type(e), str(e))
    except:
        pass


    
            

exitFlag = False
timeFlag= False


class Timing(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        

    def run(self):
        while True:
            Time.sleep(1.0)
            global time
            if timeFlag and not time == 0:       
                time = time - 1
            if exitFlag:
                break
            


timing = Timing()
timing.start()
# this will stop the timer

application_window = tk.Tk()
init_comp0 = False
while not init_comp0:
    listy = simpledialog.askstring("Input", "List of items [ \{\"name\": \"...\", \"photofile\":\"...\"}]", parent=application_window)
    if listy == "":
        items=[{"name":"demoitem", "photofile":""}]
        init_comp0 = True
        currentitem = items[currentindex]["name"]
        photoadress = items[currentindex]["photofile"]
    else:
        try:
            items = eval(listy)
            currentitem = items[currentindex]["name"]
            photoadress = items[currentindex]["photofile"]
            init_comp0= True
        except:
            pass
init_comp = False
while not init_comp:
    time = simpledialog.askinteger("Set Time", "Time Set?", parent=application_window)
    initialtime = time
    minimumbid  = simpledialog.askinteger("Minimum Bid", "Minimum Bid?", parent=application_window)
    currentbid = minimumbid
    if not minimumbid ==0 and not time == 0:
        init_comp = True
application_window.destroy()

app = App()
admin=Admin()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
while True and not exitFlag:
    application_window = tk.Tk()
    youtubeid = simpledialog.askstring("Input", "What is stream id? (type \"close\" to end program)", parent=application_window)
    if youtubeid =="close":
        exitFlag = True
        application_window.destroy()
    else:
        application_window.destroy()
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())