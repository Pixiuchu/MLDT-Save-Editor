from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import os
import io
import numpy as np
from ml00x_values import *


mainWindow = Tk()
mainWindow.title("MLDT load save file!")
mainWindow.geometry("600x300")
mainWindow.resizable(False, False)
var = IntVar()

def hide_me(widget):
    widget.pack_forget()


def show_me(widget):
    widget.pack(fill="both", expand=True)


def menuState(menuname, index, newstate):  # use this when needing to change state of menu
    menuname.entryconfigure(index, state=newstate)


MLDTfilename = ""
MLDTfilesize = 0


def openfile():  ### Open the file dialog and sets filename to MLDTfilename, sets filesize to MLDTfilesize
    # TODO: Add an if statement if you already have a file loaded if you're sure you want to go through with this
    global MLDTfilename, MLDTfilesize
    MLDTfilename = filedialog.askopenfilename(filetypes=[("Save file", ".sav")])
    #print(MLDTfilename)
    MLDTfilesize = os.stat(
        MLDTfilename).st_size  # Get filesize, if 8 then ML4_000 if 96688 then ML4_001 window otherwise fail
    #print(f"{MLDTfilesize}")
    if MLDTfilesize == 8:
        #"Loaded ML4_000.sav!")
        menuState(filemenu, 1, NORMAL)
        menuState(filemenu, 2, NORMAL)
        menuState(filemenu, 3, NORMAL)
        show_me(frameML000)
        hide_me(frameML00x)
        hide_me(frameMain)
    elif MLDTfilesize == 96688:
        #print("Loaded %s!" % MLDTfilename[-11:])
        menuState(filemenu, 1, NORMAL)
        menuState(filemenu, 2, NORMAL)
        menuState(filemenu, 3, NORMAL)
        show_me(frameML00x)
        hide_me(frameML000)
        hide_me(frameMain)
        readvalues(marioHPScroll, 0)
        readvalues(marioEXPScroll, 4)
        readflags(owHammers, 0)

    else:
        #print("The loaded file does not appear to be a Mario & Luigi: Dream Team save file. Aborting save file.")
        menuState(filemenu, 1, DISABLED)
        menuState(filemenu, 2, DISABLED)
        menuState(filemenu, 3, DISABLED)
        hide_me(frameML000)
        hide_me(frameML00x)
        show_me(frameMain)
        MLDTfilename = ""
        MLDTfilesize = 0

def savefileas():
    MLDTreadfile = open(MLDTfilename, mode="rb")
    MLDToldfile = bytes(MLDTreadfile.read())
    MLDTnewfilename = filedialog.asksaveasfilename(filetypes=[("Save file", ".sav")])
    MLDTnewfile = open(MLDTnewfilename, "wb")
    MLDTnewfile.write(MLDToldfile)
    def savevalues(widget, addressindex):
        _, address, size, *_ = values[addressindex]
        with open(MLDTnewfilename, mode="r+b") as f:
            f.seek(address)
            newvalue = widget.get()
            newvalue_bytes = int(newvalue).to_bytes(size, "little")
            f.write(newvalue_bytes)
        #print(newvalue_bytes)

    def saveflags(variable, addressindex):
        _, address, bit, *_ = flags[addressindex]
        with open(MLDTnewfilename, mode="r+b") as f:
            f.seek(address)
            oldvalue = int.from_bytes(f.read(1))
            newvalue = variable.get()
            if newvalue == 0:
                tempbit = 0xFF - 2**bit
                newvalue_bitween = oldvalue & tempbit
            else:
                newvalue_bitween = oldvalue | 2**bit
            newvalue_bit = int(newvalue_bitween).to_bytes(1)
            f.seek(address)
            print("%d = f.tell()" % f.tell())
            f.write(newvalue_bit)
            print("%d = f.tell()" % f.tell())
            print("0x%x - oldvalue" % int(oldvalue))
            print("0x%x - newvalue" % int(newvalue))
            print("0x%x - newvalue_bitween" % int(newvalue_bitween))
            print("%s - newvalue_bit" % newvalue_bit)

    saveflags(var, 27)
    savevalues(marioHPScroll, 0)
    savevalues(marioEXPScroll, 4)



    #MLDTnewfile2.close()




def closefile():
    global MLDTfilename, MLDTfilesize
    menuState(filemenu, 1, DISABLED)
    menuState(filemenu, 2, DISABLED)
    menuState(filemenu, 3, DISABLED)
    hide_me(frameML000)
    hide_me(frameML00x)
    show_me(frameMain)
    MLDTfilename = ""
    MLDTfilesize = 0


def readvalues(widget, addressindex):   # Read the specific bytes and place them inside specific widgets
    _, address, size, *_ = values[addressindex]
    with open(MLDTfilename, mode="rb") as f:
        f.seek(address)
        data = f.read(size)
        number = int.from_bytes(data, byteorder="little")
    widget.delete(0, "end")
    widget.insert(0, number)

def readflags(widget, addressindex):
    _, address, bit, *_ = flags[addressindex]
    with open(MLDTfilename, mode="rb") as f:
        f.seek(address)
        number = int.from_bytes(f.read(1))
        number2 = number >> bit & 1
    if number2 == 0:
        widget.deselect()
    else:
        widget.select()


### Menu Bar
menubar = Menu(mainWindow)
filemenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="Open file", command=openfile)
filemenu.add_command(label="Save", state=DISABLED) #command=savefile
filemenu.add_command(label="Save as...", command=savefileas, state=DISABLED)
filemenu.add_command(label="Close file", command=closefile, state=DISABLED)
mainWindow.config(menu=menubar)

### Main frames
frameMain = Frame(mainWindow)
frameMain.pack(side=TOP, anchor=NW)
frameML000 = Frame(mainWindow)  # Frame for title screen save editing
frameML00x = Frame(mainWindow)  # Frame for main save file editing

### Before Save Frame


### Title Screen Frame
TextTest = Label(frameML000, text="This save file has 8 bytes!")
TextTest.pack()

### Main Save Editing Frame
marioHPText = Label(frameML00x, text="Mario HP")
marioEXPText = Label(frameML00x, text="Mario EXP")
owHammers = Checkbutton(frameML00x, text="Hammers", variable=var)
marioHPScroll = Spinbox(frameML00x, from_=1, to=999, width=3)
marioEXPScroll = Spinbox(frameML00x, from_=0, to=9999999, width=7)
marioHPText.place(x=10, y=10)
marioHPScroll.place(x=70, y=10)
marioEXPText.place(x=5, y=40)
marioEXPScroll.place(x=70, y=40)
owHammers.place(x=10, y=70)


mainWindow.mainloop()
