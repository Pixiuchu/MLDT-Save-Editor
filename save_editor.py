from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import os
from ml00x_values import *


mainWindow = Tk()
mainWindow.title("MLDT Save Editor v0.0.1")
mainWindow.geometry("350x130")
mainWindow.resizable(False, False)
mainWindow.iconbitmap("Starlow icon.ico")
MLDTfilename = ""
MLDTfilesize = 0

################################
## Initial Variables for Ckbx ##
################################
owHammerVar = IntVar()

################################
########### Functions ##########
################################

def hide_me(widget):
    widget.pack_forget()

def show_me(widget):
    widget.pack(fill="both", expand=True)

def menuState(menuname, index, newstate):  # use this when needing to change state of menu
    menuname.entryconfigure(index, state=newstate)

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
        mainWindow.geometry("500x380")
        readvalues(marioCurHPScroll, 0)
        readvalues(marioCurBPScroll, 1)
        readvalues(marioMaxHPScroll, 2)
        readvalues(marioMaxBPScroll, 3)
        readvalues(marioPowerScroll, 4)
        readvalues(marioDefenseScroll, 5)
        readvalues(marioSpeedScroll, 6)
        readvalues(marioStacheScroll, 7)
        readvalues(marioMaxHPBeanScroll, 8)
        readvalues(marioMaxBPBeanScroll, 9)
        readvalues(marioPowerBeanScroll, 10)
        readvalues(marioDefenseBeanScroll, 11)
        readvalues(marioSpeedBeanScroll, 12)
        readvalues(marioStacheBeanScroll, 13)
        readvalues(marioMaxHPLevelScroll, 14)
        readvalues(marioMaxBPLevelScroll, 15)
        readvalues(marioPowerLevelScroll, 16)
        readvalues(marioDefenseLevelScroll, 17)
        readvalues(marioSpeedLevelScroll, 18)
        readvalues(marioStacheLevelScroll, 19)
        readvalues(marioEXPScroll, 20)
        readvalues(marioLevelScroll, 21)

        readflags(owHammers, 0)

    else:
        #print("The loaded file does not appear to be a Mario & Luigi: Dream Team save file. Aborting save file.")
        menuState(filemenu, 1, DISABLED)
        menuState(filemenu, 2, DISABLED)
        menuState(filemenu, 3, DISABLED)
        hide_me(frameML000)
        hide_me(frameML00x)
        show_me(frameMain)
        mainWindow.geometry("350x110")
        MLDTfilename = ""
        MLDTfilesize = 0

def savefile():
    def savevalues(widget, addressindex):
        _, address, size, *_ = values[addressindex]
        with open(MLDTfilename, mode="r+b") as f:
            f.seek(address)
            newvalue = widget.get()
            newvalue_bytes = int(newvalue).to_bytes(size, "little")
            f.write(newvalue_bytes)

    def saveflags(variable, addressindex):
        _, address, bit, *_ = flags[addressindex]
        with open(MLDTfilename, mode="r+b") as f:
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
            #print("%d = f.tell()" % f.tell())
            f.write(newvalue_bit)

    def saveall():
        savevalues(marioCurHPScroll, 0)
        savevalues(marioCurBPScroll, 1)
        savevalues(marioMaxHPScroll, 2)
        savevalues(marioMaxBPScroll, 3)
        savevalues(marioPowerScroll, 4)
        savevalues(marioDefenseScroll, 5)
        savevalues(marioSpeedScroll, 6)
        savevalues(marioStacheScroll, 7)
        savevalues(marioMaxHPBeanScroll, 8)
        savevalues(marioMaxBPBeanScroll, 9)
        savevalues(marioPowerBeanScroll, 10)
        savevalues(marioDefenseBeanScroll, 11)
        savevalues(marioSpeedBeanScroll, 12)
        savevalues(marioStacheBeanScroll, 13)
        savevalues(marioMaxHPLevelScroll, 14)
        savevalues(marioMaxBPLevelScroll, 15)
        savevalues(marioPowerLevelScroll, 16)
        savevalues(marioDefenseLevelScroll, 17)
        savevalues(marioSpeedLevelScroll, 18)
        savevalues(marioStacheLevelScroll, 19)
        savevalues(marioEXPScroll, 20)
        savevalues(marioLevelScroll, 21)

        saveflags(owHammerVar, 0)

    saveall()

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
            #print("%d = f.tell()" % f.tell())
            f.write(newvalue_bit)
            #print("%d = f.tell()" % f.tell())
            #print("0x%x - oldvalue" % int(oldvalue))
            #print("0x%x - newvalue" % int(newvalue))
            #print("0x%x - newvalue_bitween" % int(newvalue_bitween))
            #print("%s - newvalue_bit" % newvalue_bit)

    def saveall():
        savevalues(marioCurHPScroll, 0)
        savevalues(marioCurBPScroll, 1)
        savevalues(marioMaxHPScroll, 2)
        savevalues(marioMaxBPScroll, 3)
        savevalues(marioPowerScroll, 4)
        savevalues(marioDefenseScroll, 5)
        savevalues(marioSpeedScroll, 6)
        savevalues(marioStacheScroll, 7)
        savevalues(marioMaxHPBeanScroll, 8)
        savevalues(marioMaxBPBeanScroll, 9)
        savevalues(marioPowerBeanScroll, 10)
        savevalues(marioDefenseBeanScroll, 11)
        savevalues(marioSpeedBeanScroll, 12)
        savevalues(marioStacheBeanScroll, 13)
        savevalues(marioMaxHPLevelScroll, 14)
        savevalues(marioMaxBPLevelScroll, 15)
        savevalues(marioPowerLevelScroll, 16)
        savevalues(marioDefenseLevelScroll, 17)
        savevalues(marioSpeedLevelScroll, 18)
        savevalues(marioStacheLevelScroll, 19)
        savevalues(marioEXPScroll, 20)
        savevalues(marioLevelScroll, 21)

        saveflags(owHammerVar, 0)

    saveall()



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

#def validate(user_input):
#    if user_input.isdigit():
#        minval = int(mainWindow.nametowidget(spinbox).config('from')[4])
#        maxval = int(mainWindow.nametowidget(spinbox).config('to')[4])
#
#        if int(user_input) not in range(minval, maxval):
#            return False
#        return True
#    elif user_input == "":
#        return True
#    else:
#        return False


################################
########### Menu Bar ###########
################################
menubar = Menu(mainWindow)
filemenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="Open file", command=openfile)
filemenu.add_command(label="Save", command=savefile, state=DISABLED) #command=savefile
filemenu.add_command(label="Save as...", command=savefileas, state=DISABLED)
filemenu.add_command(label="Close file", command=closefile, state=DISABLED)
mainWindow.config(menu=menubar)


################################
########## List frames #########
################################
tkstyle = ttk.Style()
frameMain = Frame(mainWindow)
frameMain.pack(fill="both", expand=True)
frameML000 = Frame(mainWindow)  # Frame for title screen save editing
frameML00x = Frame(mainWindow)  # Frame for main save file editing
notebML00x = ttk.Notebook(frameML00x)
frameML00x_StatsMario = Frame(notebML00x, padx=10, pady=10)
frameML00x_StatsMarioBeans = LabelFrame(frameML00x_StatsMario, text="Bean Uses", background="white", padx=7)
frameML00x_StatsMarioBeans.place(x=130, y=170, width=110, height=170)
frameML00x_StatsMarioLevels = LabelFrame(frameML00x_StatsMario, text="Level-Up Bonuses", background="white", padx=7)
frameML00x_StatsMarioLevels.place(x=10, y=170, width=110, height=170)
frameML00x_StatsLuigi = Frame(notebML00x)
frameML00x_Flags = Frame(notebML00x)
notebML00x.add(frameML00x_StatsMario, text="Mario")
notebML00x.add(frameML00x_StatsLuigi, text="Luigi")
notebML00x.add(frameML00x_Flags, text="Flags")
notebML00x.pack(ipadx=500, ipady=500)

################################
####### Load screen frame ######
################################
welcomeText = Label(frameMain, text="""Welcome to the Mario & Luigi: Dream Team Save File editor!
To load a save file, please select File on the top left and
load a save file. You can load either:
the ML4_000.sav savefile for editing title screen save, or
the ML4_001.sav/ML4_002.sav for editing the full saves.""")
welcomeText.place(x=15, y=15)


################################
###### Title screen frame ######
################################
TextTest = Label(frameML000, text="""This save file has 8 bytes!
Nothing to be found here though,
you can close the file or open another one.""")
TextTest.pack()


################################
#### Main save editing frame ###
################################

Labellam = lambda a, b: Label(a, text=b, background="#FFFFFF")
##### Mario Stats Page
marioCurHPText = Labellam(frameML00x_StatsMario, "Current HP")
marioMaxHPText = Labellam(frameML00x_StatsMario, "Max HP")
marioCurBPText = Labellam(frameML00x_StatsMario, "Current BP")
marioMaxBPText = Labellam(frameML00x_StatsMario, "Max BP")
marioPowerText = Labellam(frameML00x_StatsMario, "Pow")
marioDefenseText = Labellam(frameML00x_StatsMario, "Defense")
marioSpeedText = Labellam(frameML00x_StatsMario, "Speed")
marioStacheText = Labellam(frameML00x_StatsMario, "Stache")
marioLevelText = Labellam(frameML00x_StatsMario, "Level")
marioEXPText = Labellam(frameML00x_StatsMario, "EXP")
marioMaxHPBeanText = Labellam(frameML00x_StatsMarioBeans, "Max HP")
marioMaxBPBeanText = Labellam(frameML00x_StatsMarioBeans, "Max BP")
marioPowerBeanText = Labellam(frameML00x_StatsMarioBeans, "Power")
marioDefenseBeanText = Labellam(frameML00x_StatsMarioBeans, "Defense")
marioSpeedBeanText = Labellam(frameML00x_StatsMarioBeans, "Speed")
marioStacheBeanText = Labellam(frameML00x_StatsMarioBeans, "Stache")
marioMaxHPLevelText = Labellam(frameML00x_StatsMarioLevels, "Max HP")
marioMaxBPLevelText = Labellam(frameML00x_StatsMarioLevels, "Max BP")
marioPowerLevelText = Labellam(frameML00x_StatsMarioLevels, "Power")
marioDefenseLevelText = Labellam(frameML00x_StatsMarioLevels, "Defense")
marioSpeedLevelText = Labellam(frameML00x_StatsMarioLevels, "Speed")
marioStacheLevelText = Labellam(frameML00x_StatsMarioLevels, "Stache")


Spinlam = lambda a, b, c, d: Spinbox(a, from_=b, to=c, width=d, relief="flat", highlightthickness=1, highlightbackground="#999999", justify=RIGHT, buttondownrelief=SUNKEN)
# ^^^^^^ Refer to https://discord.com/channels/267624335836053506/1195368132076896326 for more methods ^^^^^^

marioCurHPScroll = Spinlam(frameML00x_StatsMario, 1, 999, 4)
marioMaxHPScroll = Spinlam(frameML00x_StatsMario, 1, 999, 4)
marioCurBPScroll = Spinlam(frameML00x_StatsMario, 1, 999, 4)
marioMaxBPScroll = Spinlam(frameML00x_StatsMario, 1, 999, 4)
marioPowerScroll = Spinlam(frameML00x_StatsMario, 1, 999, 4)
marioDefenseScroll = Spinlam(frameML00x_StatsMario, 1, 999, 4)
marioSpeedScroll = Spinlam(frameML00x_StatsMario, 1, 999, 4)
marioStacheScroll = Spinlam(frameML00x_StatsMario, 1, 999, 4)
marioLevelScroll = Spinlam(frameML00x_StatsMario, 1, 100, 4)
marioEXPScroll = Spinlam(frameML00x_StatsMario, 0, 9999999, 8)
marioMaxHPBeanScroll = Spinlam(frameML00x_StatsMarioBeans, 0, 999, 4)
marioMaxBPBeanScroll = Spinlam(frameML00x_StatsMarioBeans, 0, 999, 4)
marioPowerBeanScroll = Spinlam(frameML00x_StatsMarioBeans, 0, 999, 4)
marioDefenseBeanScroll = Spinlam(frameML00x_StatsMarioBeans, 0, 999, 4)
marioSpeedBeanScroll = Spinlam(frameML00x_StatsMarioBeans, 0, 999, 4)
marioStacheBeanScroll = Spinlam(frameML00x_StatsMarioBeans, 0, 999, 4)
marioMaxHPLevelScroll = Spinlam(frameML00x_StatsMarioLevels, 0, 999, 4)
marioMaxBPLevelScroll = Spinlam(frameML00x_StatsMarioLevels, 0, 999, 4)
marioPowerLevelScroll = Spinlam(frameML00x_StatsMarioLevels, 0, 999, 4)
marioDefenseLevelScroll = Spinlam(frameML00x_StatsMarioLevels, 0, 999, 4)
marioSpeedLevelScroll = Spinlam(frameML00x_StatsMarioLevels, 0, 999, 4)
marioStacheLevelScroll = Spinlam(frameML00x_StatsMarioLevels, 0, 999, 4)

marioCurHPText.grid(row=0, column=0, sticky=E)
marioMaxHPText.grid(row=2, column=0, sticky=E)
marioCurBPText.grid(row=1, column=0, sticky=E)
marioMaxBPText.grid(row=3, column=0, sticky=E)
marioPowerText.grid(row=0, column=4, sticky=E, padx=(20,0))
marioDefenseText.grid(row=1, column=4, sticky=E, padx=(20,0))
marioSpeedText.grid(row=2, column=4, sticky=E, padx=(20,0))
marioStacheText.grid(row=3, column=4, sticky=E, padx=(20,0))
marioLevelText.grid(row=4, column=0, sticky=E, padx=(20,0))
marioEXPText.grid(row=4, column=4, sticky=E)
marioMaxHPBeanText.grid(row=0, column=0, sticky=E)
marioMaxBPBeanText.grid(row=1, column=0, sticky=E)
marioPowerBeanText.grid(row=2, column=0, sticky=E)
marioDefenseBeanText.grid(row=3, column=0, sticky=E)
marioSpeedBeanText.grid(row=4, column=0, sticky=E)
marioStacheBeanText.grid(row=5, column=0, sticky=E)
marioMaxHPLevelText.grid(row=0, column=0, sticky=E)
marioMaxBPLevelText.grid(row=1, column=0, sticky=E)
marioPowerLevelText.grid(row=2, column=0, sticky=E)
marioDefenseLevelText.grid(row=3, column=0, sticky=E)
marioSpeedLevelText.grid(row=4, column=0, sticky=E)
marioStacheLevelText.grid(row=5, column=0, sticky=E)

marioCurHPScroll.grid(row=0, column=1, sticky=W, pady=2)
marioMaxHPScroll.grid(row=2, column=1, sticky=W, pady=2)
marioCurBPScroll.grid(row=1, column=1, sticky=W, pady=2)
marioMaxBPScroll.grid(row=3, column=1, sticky=W, pady=2)
marioPowerScroll.grid(row=0, column=5, sticky=W, pady=2)
marioDefenseScroll.grid(row=1, column=5, sticky=W, pady=2)
marioSpeedScroll.grid(row=2, column=5, sticky=W, pady=2)
marioStacheScroll.grid(row=3, column=5, sticky=W, pady=2)
marioLevelScroll.grid(row=4, column=1, sticky=W, pady=6)
marioEXPScroll.grid(row=4, column=5, sticky=W, pady=6)
marioMaxHPBeanScroll.grid(row=0, column=1, sticky=W, pady=2)
marioMaxBPBeanScroll.grid(row=1, column=1, sticky=W, pady=2)
marioPowerBeanScroll.grid(row=2, column=1, sticky=W, pady=2)
marioDefenseBeanScroll.grid(row=3, column=1, sticky=W, pady=2)
marioSpeedBeanScroll.grid(row=4, column=1, sticky=W, pady=2)
marioStacheBeanScroll.grid(row=5, column=1, sticky=W, pady=2)
marioMaxHPLevelScroll.grid(row=0, column=1, sticky=W, pady=2)
marioMaxBPLevelScroll.grid(row=1, column=1, sticky=W, pady=2)
marioPowerLevelScroll.grid(row=2, column=1, sticky=W, pady=2)
marioDefenseLevelScroll.grid(row=3, column=1, sticky=W, pady=2)
marioSpeedLevelScroll.grid(row=4, column=1, sticky=W, pady=2)
marioStacheLevelScroll.grid(row=5, column=1, sticky=W, pady=2)


owHammers = Checkbutton(frameML00x_Flags, text="Hammers", variable=owHammerVar)

owHammers.place(x=10, y=70)


mainWindow.mainloop()
