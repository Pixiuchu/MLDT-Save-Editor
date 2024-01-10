from tkinter import *
from tkinter import filedialog
import os
import io

loadWindow = Tk()
loadWindow.title("MLDT load save file!")
loadWindow.geometry("200x100")
loadWindow.resizable(False, False)

def openfile():
    MLDTfilename = filedialog.askopenfilename(filetypes=[("Save file", ".sav")])
    print(MLDTfilename)
    MLDTfilesize = os.stat(MLDTfilename).st_size #Get filesize, if 8 then ML4_000 if 96688 then ML4_001 window otherwise fail
    print(f"{MLDTfilesize}")
    if MLDTfilesize == 8:
        print("Loaded ML4_000.sav!")
        loadWindow.destroy()
    elif MLDTfilesize == 96688:
        print("Loaded %s!" % MLDTfilename[-11:])
    else:
        print("The loaded file does not appear to be a Mario & Luigi: Dream Team save file.")

button1 = Button(text="Select your save file", command=openfile)
button1.pack()
loadWindow.mainloop()
