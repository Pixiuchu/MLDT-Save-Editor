from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import os
import io

mainWindow = Tk()
mainWindow.title("MLDT load save file!")
mainWindow.geometry("200x100")
mainWindow.resizable(False, False)

def hide_me(widget):
    widget.pack_forget()

def show_me(widget):
    widget.pack()

def menuState(filemenu, index, newstate):   #use this when needing to change state of menu
    filemenu.entryconfigure(index, state=newstate)

def openfile(): ### Open the file dialog and sets filename to MLDTfilename, sets filesize to MLDTfilesize
    MLDTfilename = filedialog.askopenfilename(filetypes=[("Save file", ".sav")])
    print(MLDTfilename)
    MLDTfilesize = os.stat(MLDTfilename).st_size #Get filesize, if 8 then ML4_000 if 96688 then ML4_001 window otherwise fail
    print(f"{MLDTfilesize}")
    if MLDTfilesize == 8:
        print("Loaded ML4_000.sav!")
        menuState(filemenu, 1, NORMAL)
        show_me(frameML000)
        hide_me(frameML00x)
        MLDToldfilename = MLDTfilename
        MLDToldfilesize = 8
    elif MLDTfilesize == 96688:
        print("Loaded %s!" % MLDTfilename[-11:])
        menuState(filemenu, 1, NORMAL)
        show_me(frameML00x)
        hide_me(frameML000)
        MLDToldfilename = MLDTfilename
        MLDToldfilesize = 96688
    else:
        if MLDToldfilesize == 8 or 96688:
            print("The loaded file does not appear to be a Mario & Luigi: Dream Team save file. Aborting loading save file.")
            MLDTfilename = MLDToldfilename
            MLDTfilesize = MLDToldfilesize
        else:
            print("The loaded file does not appear to be a Mario & Luigi: Dream Team save file. Nothing changed.")

def closefile():
    MLDTfilename = ""
    MLDTfilesize = 0
    print(f"MLDTfilename is {MLDTfilename} while MLDTfilesize is {MLDTfilesize}.")
    menuState(filemenu, 1, DISABLED)
    hide_me(frameML000)
    hide_me(frameML00x)


### Menu Bar
menubar = Menu(mainWindow)
filemenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="Open save file...", command=openfile)
filemenu.add_command(label="Close save file", command=closefile, state=DISABLED)
mainWindow.config(menu=menubar)


frameML000 = Frame(mainWindow)
frameML00x = Frame(mainWindow)

TextTest = Label(frameML000, text="This save file has 8 bytes!")
TextTest2= Label(frameML00x, text="This save file has 96688 bytes! Haha!")
MarioStatHP = Spinbox(frameML00x, from_=1, to=999)
TextTest.pack()
TextTest2.pack()
MarioStatHP.pack()



mainWindow.mainloop()
