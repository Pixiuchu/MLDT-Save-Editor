from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import os

import ml00x_values
from ml00x_values import *
from PIL import Image, ImageTk
import ctypes

mainWindow = Tk()
mainWindow.title("MLDT Save Editor v0.2")
mainWindow.geometry("500x390")
mainWindow.resizable(False, False)
mainWindow.iconbitmap("Images/Starlow icon.ico")
MLDTfilename = ""
MLDTfilesize = 0

################################
###### IntVar() Collection #####
################################


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
    MLDTfilesize = os.stat(MLDTfilename).st_size  # Get filesize, if 8 then ML4_000 if 96688 then ML4_001 window otherwise fail
    #print(f"{MLDTfilesize}")
    if MLDTfilesize == 8:
        #"Loaded ML4_000.sav!")
        menuState(filemenu, 1, NORMAL)
        menuState(filemenu, 2, NORMAL)
        menuState(filemenu, 3, DISABLED)
        show_me(frameML000)
        hide_me(frameML00x)
        hide_me(frameMain)
    elif MLDTfilesize == 96688:
        #print("Loaded %s!" % MLDTfilename[-11:])
        menuState(filemenu, 2, NORMAL)
        menuState(filemenu, 3, DISABLED)
        menuState(filemenu, 4, NORMAL)
        show_me(frameML00x)
        hide_me(frameML000)
        hide_me(frameMain)
        readall()

    else:
        #print("The loaded file does not appear to be a Mario & Luigi: Dream Team save file. Aborting save file.")
        menuState(filemenu, 1, DISABLED)
        menuState(filemenu, 2, DISABLED)
        menuState(filemenu, 3, DISABLED)
        hide_me(frameML000)
        hide_me(frameML00x)
        show_me(frameMain)
        mainWindow.geometry("500x390")
        MLDTfilename = ""
        MLDTfilesize = 0

def openfresh():
    global MLDTfilename
    MLDTfilename = "Saves/ML4_00x New Save.sav"
    menuState(filemenu, 2, DISABLED)
    menuState(filemenu, 3, DISABLED)
    menuState(filemenu, 4, NORMAL)
    show_me(frameML00x)
    hide_me(frameML000)
    hide_me(frameMain)
    readall()

def savefile():
    saveall(MLDTfilename)

def savefileas():
    MLDTreadfile = open(MLDTfilename, mode="rb")
    MLDToldfile = bytes(MLDTreadfile.read())
    MLDTnewfilename = filedialog.asksaveasfilename(filetypes=[("Save file", ".sav")])
    MLDTnewfile = open(MLDTnewfilename, "wb")
    MLDTnewfile.write(MLDToldfile)
    saveall(MLDTnewfilename)

def closefile():
    global MLDTfilename, MLDTfilesize
    menuState(filemenu, 2, DISABLED)
    menuState(filemenu, 3, DISABLED)
    menuState(filemenu, 4, DISABLED)
    hide_me(frameML000)
    hide_me(frameML00x)
    show_me(frameMain)
    MLDTfilename = ""
    MLDTfilesize = 0


class ReadSavex:
    def readvalues(self, widget, addressindex):  # Read the specific bytes and place them inside specific widgets
        _, address, size, *_ = values[addressindex]
        with open(MLDTfilename, mode="rb") as f:
            f.seek(address)
            data = f.read(size)
            number = int.from_bytes(data, byteorder="little")
        widget.delete(0, "end")
        widget.insert(0, number)

    def readflags(self, widget, addressindex):
        _, address, bit, *_ = flags[addressindex]
        with open(MLDTfilename, mode="rb") as f:
            f.seek(address)
            number = int.from_bytes(f.read(1))
            number2 = number >> bit & 1
        if number2 == 0:
            widget.deselect()
        else:
            widget.select()

    def readrankbonus(self, widget, addressindex):
        _, address, size, *_ = values[addressindex]
        with open(MLDTfilename, mode="rb") as f:
            f.seek(address)
            data = f.read(size)
            number = int.from_bytes(data, byteorder="little")
            if number & 0xFF00 == 0xE000:
                bonus = number & 0x00FF
                widget.set(allBonuses[bonus + 1])
            else:
                widget.set(allBonuses[0])

    def readrank(self, widget, addressindex, type):
        _, address, size, *_ = values[addressindex]
        with open(MLDTfilename, mode="rb") as f:
            f.seek(address)
            data = f.read(1)
            number = int.from_bytes(data)
            setgear = number & 0xF0
            setgear -= 0x20
            setgear /= 0x10
            setgear = int(setgear)
            setrank = number & 0x0F
            if type == "Gear":
                widget.delete(0, "end")
                widget.insert(0, setgear)
            elif type == "Rank":
                widget.set(allRanks[setrank])

    def readfilenumber(self, widget, addressindex):
        _, address, size, *_ = values[addressindex]
        with open(MLDTfilename, mode="rb") as f:
            f.seek(address)
            data = f.read(1)
            number = int.from_bytes(data)
            if number == 1 or number == 4:
                widget.set(ml00x_values.file1or2[0])
            else:
                widget.set(ml00x_values.file1or2[1])

    def savefilenumber(self):
        with open(MLDTfilename, mode="r+b") as f:
            f.seek(0x11A4)
            filetext = MiscellaneousPage.miscFileNumber.get()
            if filetext == "File 1":
                f.write(int(0x01).to_bytes(1))
            else:
                f.write(int(0x09).to_bytes(1))

    def savevalues(self, file, widget, addressindex):
        _, address, size, *_ = values[addressindex]
        with open(file, mode="r+b") as f:
            f.seek(address)
            newvalue = widget.get()
            newvalue_bytes = int(newvalue).to_bytes(size, "little")
            f.write(newvalue_bytes)

    def saveflags(self, file, variable, addressindex):
        _, address, bit, *_ = flags[addressindex]
        with open(file, mode="r+b") as f:
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

    def saverank(self, file, widgetrank, widgetgear, addressindex):
        _, address, size, *_ = values[addressindex]
        with open(file, mode="r+b") as f:
            namerank = allRanks.index(widgetrank.get())
            gearslot = int(widgetgear.get())
            #print("%x" % gearslot)
            gearslot *= 0x10
            #print("%x" % gearslot)
            gearslot += 0x20
            #print("%x" % gearslot)
            rankandgear = namerank + gearslot
            #print("%x" % rankandgear)
            finalbyte = int(rankandgear).to_bytes(1)
            f.seek(address)
            f.write(finalbyte)

    def saverankbonus(self, file, widget, addressindex):
        _, address, size, *_ = values[addressindex]
        with open(file, mode="r+b") as f:
            namerankb = allBonuses.index(widget.get()) - 1
            #print(namerankb)
            if namerankb == -1:
                f.seek(address)
                f.write(int(0x0000).to_bytes(2))
            else:
                ranktobyte = int(namerankb).to_bytes(1)
                rankyes = int(0xE0).to_bytes(1)
                f.seek(address)
                f.write(ranktobyte + rankyes)

def saveall(x):
    useself = ReadSavex()
    useself.savevalues(x, MarioStatsPage.mCurHPScroll, 0)
    useself.savevalues(x, MarioStatsPage.mCurBPScroll, 1)
    useself.savevalues(x, MarioStatsPage.mMaxHPScroll, 2)
    useself.savevalues(x, MarioStatsPage.mMaxBPScroll, 3)
    useself.savevalues(x, MarioStatsPage.mPowerScroll, 4)
    useself.savevalues(x, MarioStatsPage.mDefenseScroll, 5)
    useself.savevalues(x, MarioStatsPage.mSpeedScroll, 6)
    useself.savevalues(x, MarioStatsPage.mStacheScroll, 7)
    useself.savevalues(x, MarioStatsPage.mMaxHPBeanScroll, 8)
    useself.savevalues(x, MarioStatsPage.mMaxBPBeanScroll, 9)
    useself.savevalues(x, MarioStatsPage.mPowerBeanScroll, 10)
    useself.savevalues(x, MarioStatsPage.mDefenseBeanScroll, 11)
    useself.savevalues(x, MarioStatsPage.mSpeedBeanScroll, 12)
    useself.savevalues(x, MarioStatsPage.mStacheBeanScroll, 13)
    useself.savevalues(x, MarioStatsPage.mMaxHPLevelScroll, 14)
    useself.savevalues(x, MarioStatsPage.mMaxBPLevelScroll, 15)
    useself.savevalues(x, MarioStatsPage.mPowerLevelScroll, 16)
    useself.savevalues(x, MarioStatsPage.mDefenseLevelScroll, 17)
    useself.savevalues(x, MarioStatsPage.mSpeedLevelScroll, 18)
    useself.savevalues(x, MarioStatsPage.mStacheLevelScroll, 19)
    useself.savevalues(x, MarioStatsPage.mEXPScroll, 20)
    useself.savevalues(x, MarioStatsPage.mLevelScroll, 21)
    useself.saverankbonus(x, MarioStatsPage.mBonus1, 30)
    useself.saverankbonus(x, MarioStatsPage.mBonus2, 31)
    useself.saverankbonus(x, MarioStatsPage.mBonus3, 32)
    useself.saverankbonus(x, MarioStatsPage.mBonus4, 33)
    useself.saverankbonus(x, MarioStatsPage.mBonus5, 34)
    useself.saverank(x, MarioStatsPage.mRank, MarioStatsPage.mExtraGear, 23)
    useself.savevalues(x, MarioStatsPage.universalBadgeSlots, 35)
    useself.savevalues(x, LuigiStatsPage.mCurHPScroll, 36)
    useself.savevalues(x, LuigiStatsPage.mCurBPScroll, 37)
    useself.savevalues(x, LuigiStatsPage.mMaxHPScroll, 38)
    useself.savevalues(x, LuigiStatsPage.mMaxBPScroll, 39)
    useself.savevalues(x, LuigiStatsPage.mPowerScroll, 40)
    useself.savevalues(x, LuigiStatsPage.mDefenseScroll, 41)
    useself.savevalues(x, LuigiStatsPage.mSpeedScroll, 42)
    useself.savevalues(x, LuigiStatsPage.mStacheScroll, 43)
    useself.savevalues(x, LuigiStatsPage.mMaxHPBeanScroll, 44)
    useself.savevalues(x, LuigiStatsPage.mMaxBPBeanScroll, 45)
    useself.savevalues(x, LuigiStatsPage.mPowerBeanScroll, 46)
    useself.savevalues(x, LuigiStatsPage.mDefenseBeanScroll, 47)
    useself.savevalues(x, LuigiStatsPage.mSpeedBeanScroll, 48)
    useself.savevalues(x, LuigiStatsPage.mStacheBeanScroll, 49)
    useself.savevalues(x, LuigiStatsPage.mMaxHPLevelScroll, 50)
    useself.savevalues(x, LuigiStatsPage.mMaxBPLevelScroll, 51)
    useself.savevalues(x, LuigiStatsPage.mPowerLevelScroll, 52)
    useself.savevalues(x, LuigiStatsPage.mDefenseLevelScroll, 53)
    useself.savevalues(x, LuigiStatsPage.mSpeedLevelScroll, 54)
    useself.savevalues(x, LuigiStatsPage.mStacheLevelScroll, 55)
    useself.savevalues(x, LuigiStatsPage.mEXPScroll, 56)
    useself.savevalues(x, LuigiStatsPage.mLevelScroll, 57)
    useself.saverankbonus(x, LuigiStatsPage.mBonus1, 66)
    useself.saverankbonus(x, LuigiStatsPage.mBonus2, 67)
    useself.saverankbonus(x, LuigiStatsPage.mBonus3, 68)
    useself.saverankbonus(x, LuigiStatsPage.mBonus4, 69)
    useself.saverankbonus(x, LuigiStatsPage.mBonus5, 70)
    useself.saverank(x, LuigiStatsPage.mRank, LuigiStatsPage.mExtraGear, 59)
    useself.savevalues(x, LuigiStatsPage.universalBadgeSlots, 35)
    useself.saveflags(x, Flag_AbilityPage.owHammerVar, 0)
    useself.saveflags(x, Flag_AbilityPage.owHammerMiniVar, 1)
    useself.saveflags(x, Flag_AbilityPage.owHammerMoleVar, 2)
    useself.saveflags(x, Flag_AbilityPage.owSpinJumpVar, 3)
    useself.saveflags(x, Flag_AbilityPage.owSideDrillVar, 4)
    useself.saveflags(x, Flag_AbilityPage.owBallHopVar, 5)
    useself.saveflags(x, Flag_AbilityPage.dwBButtonVar, 7)
    useself.saveflags(x, Flag_AbilityPage.dwStackVar, 8)
    useself.saveflags(x, Flag_AbilityPage.dwStackGroundPoundVar, 11)
    useself.saveflags(x, Flag_AbilityPage.dwStackSpingJumpVar, 12)
    useself.saveflags(x, Flag_AbilityPage.dwConeVar, 9)
    useself.saveflags(x, Flag_AbilityPage.dwConeJumpVar, 13)
    useself.saveflags(x, Flag_AbilityPage.dwConeTornadoVar, 14)
    useself.saveflags(x, Flag_AbilityPage.dwBallVar, 10)
    useself.saveflags(x, Flag_AbilityPage.dwBallSlingshotVar, 15)
    useself.saveflags(x, Flag_AbilityPage.dwBallHammerVar, 16)
    useself.saveflags(x, Flag_AbilityPage.dwDropVar, 17)
    useself.saveflags(x, Flag_AbilityPage.dwWallkickVar, 18)
    useself.saveflags(x, Flag_BattlePage.atkRedShellVar, 24)
    useself.saveflags(x, Flag_BattlePage.atkByeByeCannonVar, 30)
    useself.saveflags(x, Flag_BattlePage.atkBombDerbyVar, 28)
    useself.saveflags(x, Flag_BattlePage.atkJetBoardBashVar, 29)
    useself.saveflags(x, Flag_BattlePage.atkZeeEggVar, 33)
    useself.saveflags(x, Flag_BattlePage.atkGreenShellVar, 25)
    useself.saveflags(x, Flag_BattlePage.atkFireFlowerVar, 27)
    useself.saveflags(x, Flag_BattlePage.atkDropchopperVar, 26)
    useself.saveflags(x, Flag_BattlePage.atkSlingsniperVar, 31)
    useself.saveflags(x, Flag_BattlePage.atkStarRocketVar, 32)
    useself.saveflags(x, Flag_BattlePage.atkLuiginaryBallVar, 34)
    useself.saveflags(x, Flag_BattlePage.atkLuiginaryStackVar, 35)
    useself.saveflags(x, Flag_BattlePage.atkLuiginaryHammerVar, 36)
    useself.saveflags(x, Flag_BattlePage.atkLuiginaryFlameVar, 37)
    useself.saveflags(x, Flag_BattlePage.atkLuiginaryWallVar, 38)
    useself.saveflags(x, Flag_BattlePage.atkLuiginaryTyphoonVar, 39)
    useself.saveflags(x, Flag_BattlePage.flagBrosAttackVar, 20)
    useself.saveflags(x, Flag_BattlePage.flagLuiginaryAttackVar, 21)
    useself.saveflags(x, Flag_BattlePage.flagItemBlocksBattleVar, 22)
    useself.saveflags(x, Flag_BattlePage.flagBadgesInBattleVar, 23)
    useself.saveflags(x, MiscellaneousPage.miscShopFlagDozingVar, 40)
    useself.saveflags(x, MiscellaneousPage.miscShopFlagDriftwVar, 41)
    useself.saveflags(x, MiscellaneousPage.miscShopFlagSomnomVar, 42)
    useself.saveflags(x, MiscellaneousPage.miscHardModeVar, 6)
    useself.saveflags(x, MiscellaneousPage.miscAllowPausingVar, 19)
    useself.savevalues(x, MiscellaneousPage.miscCoins, 72)
    useself.savefilenumber()

def readall():
    readSRAMx = ReadSavex()
    readSRAMx.readvalues(MarioStatsPage.mCurHPScroll, 0)
    readSRAMx.readvalues(MarioStatsPage.mCurBPScroll, 1)
    readSRAMx.readvalues(MarioStatsPage.mMaxHPScroll, 2)
    readSRAMx.readvalues(MarioStatsPage.mMaxBPScroll, 3)
    readSRAMx.readvalues(MarioStatsPage.mPowerScroll, 4)
    readSRAMx.readvalues(MarioStatsPage.mDefenseScroll, 5)
    readSRAMx.readvalues(MarioStatsPage.mSpeedScroll, 6)
    readSRAMx.readvalues(MarioStatsPage.mStacheScroll, 7)
    readSRAMx.readvalues(MarioStatsPage.mMaxHPBeanScroll, 8)
    readSRAMx.readvalues(MarioStatsPage.mMaxBPBeanScroll, 9)
    readSRAMx.readvalues(MarioStatsPage.mPowerBeanScroll, 10)
    readSRAMx.readvalues(MarioStatsPage.mDefenseBeanScroll, 11)
    readSRAMx.readvalues(MarioStatsPage.mSpeedBeanScroll, 12)
    readSRAMx.readvalues(MarioStatsPage.mStacheBeanScroll, 13)
    readSRAMx.readvalues(MarioStatsPage.mMaxHPLevelScroll, 14)
    readSRAMx.readvalues(MarioStatsPage.mMaxBPLevelScroll, 15)
    readSRAMx.readvalues(MarioStatsPage.mPowerLevelScroll, 16)
    readSRAMx.readvalues(MarioStatsPage.mDefenseLevelScroll, 17)
    readSRAMx.readvalues(MarioStatsPage.mSpeedLevelScroll, 18)
    readSRAMx.readvalues(MarioStatsPage.mStacheLevelScroll, 19)
    readSRAMx.readvalues(MarioStatsPage.mEXPScroll, 20)
    readSRAMx.readvalues(MarioStatsPage.mLevelScroll, 21)
    # readSRAMx.readvalues(MarioStatsPage.mEXPNextScroll, 22) #TODO: add "EXP to next level" label that automatically adjusts
    readSRAMx.readrankbonus(MarioStatsPage.mBonus1, 30)
    readSRAMx.readrankbonus(MarioStatsPage.mBonus2, 31)
    readSRAMx.readrankbonus(MarioStatsPage.mBonus3, 32)
    readSRAMx.readrankbonus(MarioStatsPage.mBonus4, 33)
    readSRAMx.readrankbonus(MarioStatsPage.mBonus5, 34)
    readSRAMx.readvalues(MarioStatsPage.universalBadgeSlots, 35)
    readSRAMx.readrank(MarioStatsPage.mExtraGear, 23, "Gear")
    readSRAMx.readrank(MarioStatsPage.mRank, 23, "Rank")
    readSRAMx.readvalues(LuigiStatsPage.mCurHPScroll, 36)
    readSRAMx.readvalues(LuigiStatsPage.mCurBPScroll, 37)
    readSRAMx.readvalues(LuigiStatsPage.mMaxHPScroll, 38)
    readSRAMx.readvalues(LuigiStatsPage.mMaxBPScroll, 39)
    readSRAMx.readvalues(LuigiStatsPage.mPowerScroll, 40)
    readSRAMx.readvalues(LuigiStatsPage.mDefenseScroll, 41)
    readSRAMx.readvalues(LuigiStatsPage.mSpeedScroll, 42)
    readSRAMx.readvalues(LuigiStatsPage.mStacheScroll, 43)
    readSRAMx.readvalues(LuigiStatsPage.mMaxHPBeanScroll, 44)
    readSRAMx.readvalues(LuigiStatsPage.mMaxBPBeanScroll, 45)
    readSRAMx.readvalues(LuigiStatsPage.mPowerBeanScroll, 46)
    readSRAMx.readvalues(LuigiStatsPage.mDefenseBeanScroll, 47)
    readSRAMx.readvalues(LuigiStatsPage.mSpeedBeanScroll, 48)
    readSRAMx.readvalues(LuigiStatsPage.mStacheBeanScroll, 49)
    readSRAMx.readvalues(LuigiStatsPage.mMaxHPLevelScroll, 50)
    readSRAMx.readvalues(LuigiStatsPage.mMaxBPLevelScroll, 51)
    readSRAMx.readvalues(LuigiStatsPage.mPowerLevelScroll, 52)
    readSRAMx.readvalues(LuigiStatsPage.mDefenseLevelScroll, 53)
    readSRAMx.readvalues(LuigiStatsPage.mSpeedLevelScroll, 54)
    readSRAMx.readvalues(LuigiStatsPage.mStacheLevelScroll, 55)
    readSRAMx.readvalues(LuigiStatsPage.mEXPScroll, 56)
    readSRAMx.readvalues(LuigiStatsPage.mLevelScroll, 57)
    readSRAMx.readrankbonus(LuigiStatsPage.mBonus1, 66)
    readSRAMx.readrankbonus(LuigiStatsPage.mBonus2, 67)
    readSRAMx.readrankbonus(LuigiStatsPage.mBonus3, 68)
    readSRAMx.readrankbonus(LuigiStatsPage.mBonus4, 69)
    readSRAMx.readrankbonus(LuigiStatsPage.mBonus5, 70)
    readSRAMx.readrank(LuigiStatsPage.mRank, 59, "Rank")
    readSRAMx.readrank(LuigiStatsPage.mExtraGear, 59, "Gear")
    readSRAMx.readvalues(LuigiStatsPage.universalBadgeSlots, 35)
    readSRAMx.readflags(Flag_AbilityPage.owHammers, 0)
    readSRAMx.readflags(Flag_AbilityPage.owHammerMini, 1)
    readSRAMx.readflags(Flag_AbilityPage.owHammerMole, 2)
    readSRAMx.readflags(Flag_AbilityPage.owSpinJump, 3)
    readSRAMx.readflags(Flag_AbilityPage.owSideDrill, 4)
    readSRAMx.readflags(Flag_AbilityPage.owBallHop, 5)
    readSRAMx.readflags(Flag_AbilityPage.dwBButton, 7)
    readSRAMx.readflags(Flag_AbilityPage.dwStack, 8)
    readSRAMx.readflags(Flag_AbilityPage.dwStackGroundPound, 11)
    readSRAMx.readflags(Flag_AbilityPage.dwStackSpingJump, 12)
    readSRAMx.readflags(Flag_AbilityPage.dwCone, 9)
    readSRAMx.readflags(Flag_AbilityPage.dwConeJump, 13)
    readSRAMx.readflags(Flag_AbilityPage.dwConeTornado, 14)
    readSRAMx.readflags(Flag_AbilityPage.dwBall, 10)
    readSRAMx.readflags(Flag_AbilityPage.dwBallSlingshot, 15)
    readSRAMx.readflags(Flag_AbilityPage.dwBallHammer, 16)
    readSRAMx.readflags(Flag_AbilityPage.dwDrop, 17)
    readSRAMx.readflags(Flag_AbilityPage.dwWallkick, 18)
    readSRAMx.readflags(Flag_BattlePage.atkRedShell, 24)
    readSRAMx.readflags(Flag_BattlePage.atkByeByeCannon, 30)
    readSRAMx.readflags(Flag_BattlePage.atkBombDerby, 28)
    readSRAMx.readflags(Flag_BattlePage.atkJetBoardBash, 29)
    readSRAMx.readflags(Flag_BattlePage.atkZeeEgg, 33)
    readSRAMx.readflags(Flag_BattlePage.atkGreenShell, 25)
    readSRAMx.readflags(Flag_BattlePage.atkFireFlower, 27)
    readSRAMx.readflags(Flag_BattlePage.atkDropchopper, 26)
    readSRAMx.readflags(Flag_BattlePage.atkSlingsniper, 31)
    readSRAMx.readflags(Flag_BattlePage.atkStarRocket, 32)
    readSRAMx.readflags(Flag_BattlePage.atkLuiginaryBall, 34)
    readSRAMx.readflags(Flag_BattlePage.atkLuiginaryStack, 35)
    readSRAMx.readflags(Flag_BattlePage.atkLuiginaryHammer, 36)
    readSRAMx.readflags(Flag_BattlePage.atkLuiginaryFlame, 37)
    readSRAMx.readflags(Flag_BattlePage.atkLuiginaryWall, 38)
    readSRAMx.readflags(Flag_BattlePage.atkLuiginaryTyphoon, 39)
    readSRAMx.readflags(Flag_BattlePage.flagBrosAttack, 20)
    readSRAMx.readflags(Flag_BattlePage.flagLuiginaryAttack, 21)
    readSRAMx.readflags(Flag_BattlePage.flagItemBlocksBattle, 22)
    readSRAMx.readflags(Flag_BattlePage.flagBadgesInBattle, 23)
    readSRAMx.readfilenumber(MiscellaneousPage.miscFileNumber, 74)
    readSRAMx.readflags(MiscellaneousPage.miscShopFlagDozing, 40)
    readSRAMx.readflags(MiscellaneousPage.miscShopFlagDriftw, 41)
    readSRAMx.readflags(MiscellaneousPage.miscShopFlagSomnom, 42)
    readSRAMx.readflags(MiscellaneousPage.miscHardMode, 6)
    readSRAMx.readflags(MiscellaneousPage.miscAllowPausing, 19)
    readSRAMx.readvalues(MiscellaneousPage.miscCoins, 72)


def resetstatsmario():
    MarioStatsPage.mCurHPScroll.delete(0, "end")
    MarioStatsPage.mCurHPScroll.insert(0, 24)
    MarioStatsPage.mMaxHPScroll.delete(0, "end")
    MarioStatsPage.mMaxHPScroll.insert(0, 24)
    MarioStatsPage.mCurBPScroll.delete(0, "end")
    MarioStatsPage.mCurBPScroll.insert(0, 8)
    MarioStatsPage.mMaxBPScroll.delete(0, "end")
    MarioStatsPage.mMaxBPScroll.insert(0, 8)
    MarioStatsPage.mPowerScroll.delete(0, "end")
    MarioStatsPage.mPowerScroll.insert(0, 20)
    MarioStatsPage.mDefenseScroll.delete(0, "end")
    MarioStatsPage.mDefenseScroll.insert(0, 13)
    MarioStatsPage.mSpeedScroll.delete(0, "end")
    MarioStatsPage.mSpeedScroll.insert(0, 16)
    MarioStatsPage.mStacheScroll.delete(0, "end")
    MarioStatsPage.mStacheScroll.insert(0, 20)
    MarioStatsPage.mLevelScroll.delete(0, "end")
    MarioStatsPage.mLevelScroll.insert(0, 1)
    MarioStatsPage.mEXPScroll.delete(0, "end")
    MarioStatsPage.mEXPScroll.insert(0, 0)
    MarioStatsPage.mMaxHPBeanScroll.delete(0, "end")
    MarioStatsPage.mMaxHPBeanScroll.insert(0, 0)
    MarioStatsPage.mMaxBPBeanScroll.delete(0, "end")
    MarioStatsPage.mMaxBPBeanScroll.insert(0, 0)
    MarioStatsPage.mPowerBeanScroll.delete(0, "end")
    MarioStatsPage.mPowerBeanScroll.insert(0, 0)
    MarioStatsPage.mDefenseBeanScroll.delete(0, "end")
    MarioStatsPage.mDefenseBeanScroll.insert(0, 0)
    MarioStatsPage.mSpeedBeanScroll.delete(0, "end")
    MarioStatsPage.mSpeedBeanScroll.insert(0, 0)
    MarioStatsPage.mStacheBeanScroll.delete(0, "end")
    MarioStatsPage.mStacheBeanScroll.insert(0, 0)
    MarioStatsPage.mMaxHPLevelScroll.delete(0, "end")
    MarioStatsPage.mMaxHPLevelScroll.insert(0, 0)
    MarioStatsPage.mMaxBPLevelScroll.delete(0, "end")
    MarioStatsPage.mMaxBPLevelScroll.insert(0, 0)
    MarioStatsPage.mPowerLevelScroll.delete(0, "end")
    MarioStatsPage.mPowerLevelScroll.insert(0, 0)
    MarioStatsPage.mDefenseLevelScroll.delete(0, "end")
    MarioStatsPage.mDefenseLevelScroll.insert(0, 0)
    MarioStatsPage.mSpeedLevelScroll.delete(0, "end")
    MarioStatsPage.mSpeedLevelScroll.insert(0, 0)
    MarioStatsPage.mStacheLevelScroll.delete(0, "end")
    MarioStatsPage.mStacheLevelScroll.insert(0, 0)


def maxstatsmario():
    MarioStatsPage.mCurHPScroll.delete(0, "end")
    MarioStatsPage.mCurHPScroll.insert(0, 999)
    MarioStatsPage.mMaxHPScroll.delete(0, "end")
    MarioStatsPage.mMaxHPScroll.insert(0, 999)
    MarioStatsPage.mCurBPScroll.delete(0, "end")
    MarioStatsPage.mCurBPScroll.insert(0, 999)
    MarioStatsPage.mMaxBPScroll.delete(0, "end")
    MarioStatsPage.mMaxBPScroll.insert(0, 999)
    MarioStatsPage.mPowerScroll.delete(0, "end")
    MarioStatsPage.mPowerScroll.insert(0, 999)
    MarioStatsPage.mDefenseScroll.delete(0, "end")
    MarioStatsPage.mDefenseScroll.insert(0, 999)
    MarioStatsPage.mSpeedScroll.delete(0, "end")
    MarioStatsPage.mSpeedScroll.insert(0, 999)
    MarioStatsPage.mStacheScroll.delete(0, "end")
    MarioStatsPage.mStacheScroll.insert(0, 999)
    MarioStatsPage.mLevelScroll.delete(0, "end")
    MarioStatsPage.mLevelScroll.insert(0, 100)
    MarioStatsPage.mEXPScroll.delete(0, "end")
    MarioStatsPage.mEXPScroll.insert(0, 3000000)
    MarioStatsPage.mMaxHPBeanScroll.delete(0, "end")
    MarioStatsPage.mMaxHPBeanScroll.insert(0, 999)
    MarioStatsPage.mMaxBPBeanScroll.delete(0, "end")
    MarioStatsPage.mMaxBPBeanScroll.insert(0, 999)
    MarioStatsPage.mPowerBeanScroll.delete(0, "end")
    MarioStatsPage.mPowerBeanScroll.insert(0, 999)
    MarioStatsPage.mDefenseBeanScroll.delete(0, "end")
    MarioStatsPage.mDefenseBeanScroll.insert(0, 999)
    MarioStatsPage.mSpeedBeanScroll.delete(0, "end")
    MarioStatsPage.mSpeedBeanScroll.insert(0, 999)
    MarioStatsPage.mStacheBeanScroll.delete(0, "end")
    MarioStatsPage.mStacheBeanScroll.insert(0, 999)
    MarioStatsPage.mMaxHPLevelScroll.delete(0, "end")
    MarioStatsPage.mMaxHPLevelScroll.insert(0, 999)
    MarioStatsPage.mMaxBPLevelScroll.delete(0, "end")
    MarioStatsPage.mMaxBPLevelScroll.insert(0, 999)
    MarioStatsPage.mPowerLevelScroll.delete(0, "end")
    MarioStatsPage.mPowerLevelScroll.insert(0, 999)
    MarioStatsPage.mDefenseLevelScroll.delete(0, "end")
    MarioStatsPage.mDefenseLevelScroll.insert(0, 999)
    MarioStatsPage.mSpeedLevelScroll.delete(0, "end")
    MarioStatsPage.mSpeedLevelScroll.insert(0, 999)
    MarioStatsPage.mStacheLevelScroll.delete(0, "end")
    MarioStatsPage.mStacheLevelScroll.insert(0, 999)

def resetstatsluigi():
    LuigiStatsPage.mCurHPScroll.delete(0, "end")
    LuigiStatsPage.mCurHPScroll.insert(0, 30)
    LuigiStatsPage.mMaxHPScroll.delete(0, "end")
    LuigiStatsPage.mMaxHPScroll.insert(0, 30)
    LuigiStatsPage.mCurBPScroll.delete(0, "end")
    LuigiStatsPage.mCurBPScroll.insert(0, 6)
    LuigiStatsPage.mMaxBPScroll.delete(0, "end")
    LuigiStatsPage.mMaxBPScroll.insert(0, 6)
    LuigiStatsPage.mPowerScroll.delete(0, "end")
    LuigiStatsPage.mPowerScroll.insert(0, 16)
    LuigiStatsPage.mDefenseScroll.delete(0, "end")
    LuigiStatsPage.mDefenseScroll.insert(0, 17)
    LuigiStatsPage.mSpeedScroll.delete(0, "end")
    LuigiStatsPage.mSpeedScroll.insert(0, 10)
    LuigiStatsPage.mStacheScroll.delete(0, "end")
    LuigiStatsPage.mStacheScroll.insert(0, 30)
    LuigiStatsPage.mLevelScroll.delete(0, "end")
    LuigiStatsPage.mLevelScroll.insert(0, 1)
    LuigiStatsPage.mEXPScroll.delete(0, "end")
    LuigiStatsPage.mEXPScroll.insert(0, 0)
    LuigiStatsPage.mMaxHPBeanScroll.delete(0, "end")
    LuigiStatsPage.mMaxHPBeanScroll.insert(0, 0)
    LuigiStatsPage.mMaxBPBeanScroll.delete(0, "end")
    LuigiStatsPage.mMaxBPBeanScroll.insert(0, 0)
    LuigiStatsPage.mPowerBeanScroll.delete(0, "end")
    LuigiStatsPage.mPowerBeanScroll.insert(0, 0)
    LuigiStatsPage.mDefenseBeanScroll.delete(0, "end")
    LuigiStatsPage.mDefenseBeanScroll.insert(0, 0)
    LuigiStatsPage.mSpeedBeanScroll.delete(0, "end")
    LuigiStatsPage.mSpeedBeanScroll.insert(0, 0)
    LuigiStatsPage.mStacheBeanScroll.delete(0, "end")
    LuigiStatsPage.mStacheBeanScroll.insert(0, 0)
    LuigiStatsPage.mMaxHPLevelScroll.delete(0, "end")
    LuigiStatsPage.mMaxHPLevelScroll.insert(0, 0)
    LuigiStatsPage.mMaxBPLevelScroll.delete(0, "end")
    LuigiStatsPage.mMaxBPLevelScroll.insert(0, 0)
    LuigiStatsPage.mPowerLevelScroll.delete(0, "end")
    LuigiStatsPage.mPowerLevelScroll.insert(0, 0)
    LuigiStatsPage.mDefenseLevelScroll.delete(0, "end")
    LuigiStatsPage.mDefenseLevelScroll.insert(0, 0)
    LuigiStatsPage.mSpeedLevelScroll.delete(0, "end")
    LuigiStatsPage.mSpeedLevelScroll.insert(0, 0)
    LuigiStatsPage.mStacheLevelScroll.delete(0, "end")
    LuigiStatsPage.mStacheLevelScroll.insert(0, 0)

def maxstatsluigi():
    LuigiStatsPage.mCurHPScroll.delete(0, "end")
    LuigiStatsPage.mCurHPScroll.insert(0, 999)
    LuigiStatsPage.mMaxHPScroll.delete(0, "end")
    LuigiStatsPage.mMaxHPScroll.insert(0, 999)
    LuigiStatsPage.mCurBPScroll.delete(0, "end")
    LuigiStatsPage.mCurBPScroll.insert(0, 999)
    LuigiStatsPage.mMaxBPScroll.delete(0, "end")
    LuigiStatsPage.mMaxBPScroll.insert(0, 999)
    LuigiStatsPage.mPowerScroll.delete(0, "end")
    LuigiStatsPage.mPowerScroll.insert(0, 999)
    LuigiStatsPage.mDefenseScroll.delete(0, "end")
    LuigiStatsPage.mDefenseScroll.insert(0, 999)
    LuigiStatsPage.mSpeedScroll.delete(0, "end")
    LuigiStatsPage.mSpeedScroll.insert(0, 999)
    LuigiStatsPage.mStacheScroll.delete(0, "end")
    LuigiStatsPage.mStacheScroll.insert(0, 999)
    LuigiStatsPage.mLevelScroll.delete(0, "end")
    LuigiStatsPage.mLevelScroll.insert(0, 100)
    LuigiStatsPage.mEXPScroll.delete(0, "end")
    LuigiStatsPage.mEXPScroll.insert(0, 3250000)
    LuigiStatsPage.mMaxHPBeanScroll.delete(0, "end")
    LuigiStatsPage.mMaxHPBeanScroll.insert(0, 999)
    LuigiStatsPage.mMaxBPBeanScroll.delete(0, "end")
    LuigiStatsPage.mMaxBPBeanScroll.insert(0, 999)
    LuigiStatsPage.mPowerBeanScroll.delete(0, "end")
    LuigiStatsPage.mPowerBeanScroll.insert(0, 999)
    LuigiStatsPage.mDefenseBeanScroll.delete(0, "end")
    LuigiStatsPage.mDefenseBeanScroll.insert(0, 999)
    LuigiStatsPage.mSpeedBeanScroll.delete(0, "end")
    LuigiStatsPage.mSpeedBeanScroll.insert(0, 999)
    LuigiStatsPage.mStacheBeanScroll.delete(0, "end")
    LuigiStatsPage.mStacheBeanScroll.insert(0, 999)
    LuigiStatsPage.mMaxHPLevelScroll.delete(0, "end")
    LuigiStatsPage.mMaxHPLevelScroll.insert(0, 999)
    LuigiStatsPage.mMaxBPLevelScroll.delete(0, "end")
    LuigiStatsPage.mMaxBPLevelScroll.insert(0, 999)
    LuigiStatsPage.mPowerLevelScroll.delete(0, "end")
    LuigiStatsPage.mPowerLevelScroll.insert(0, 999)
    LuigiStatsPage.mDefenseLevelScroll.delete(0, "end")
    LuigiStatsPage.mDefenseLevelScroll.insert(0, 999)
    LuigiStatsPage.mSpeedLevelScroll.delete(0, "end")
    LuigiStatsPage.mSpeedLevelScroll.insert(0, 999)
    LuigiStatsPage.mStacheLevelScroll.delete(0, "end")
    LuigiStatsPage.mStacheLevelScroll.insert(0, 999)


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
#filemenu.add_command(label="Open fresh file", command=openfresh)
filemenu.add_command(label="Save", command=savefile, state=DISABLED) #command=savefile
filemenu.add_command(label="Save as...", command=savefileas, state=DISABLED)
filemenu.add_command(label="Close file", command=closefile, state=DISABLED)
mainWindow.config(menu=menubar)


################################
########## List frames #########
################################
def tab_switch(event):
    currenttab = event.widget.select()
    tab = event.widget.tab(currenttab, "text")
    if tab == "Minimap ":
        mainWindow.geometry("720x600")
        #print("Minimap!!!!!!")
    else:
        mainWindow.geometry("500x390")
        #print("Not minimap......")

tkstyle = ttk.Style()

### Main Window
frameMain = Frame(mainWindow)
frameMain.pack(fill="both", expand=True)
frameML000 = Frame(mainWindow)  # Frame for title screen save editing
frameML00x = Frame(mainWindow)  # Frame for main save file editing
notebML00x = ttk.Notebook(frameML00x)

### Stats Mario
frameML00x_StatsMario = Frame(notebML00x, padx=10, pady=10, background="white")
frameML00x_StatsMarioBeans = LabelFrame(frameML00x_StatsMario, text="Bean Uses", background="white", padx=7)
frameML00x_StatsMarioBeans.place(x=130, y=170, width=110, height=170)
frameML00x_StatsMarioLevels = LabelFrame(frameML00x_StatsMario, text="Level-Up Bonuses", background="white", padx=7)
frameML00x_StatsMarioLevels.place(x=10, y=170, width=110, height=170)
frameML00x_StatsMarioRanks = LabelFrame(frameML00x_StatsMario, text="Ranks", background="white", padx=1)
frameML00x_StatsMarioRanks.place(x=250, y=120, width=220, height=220)

### Stats Luigi
frameML00x_StatsLuigi = Frame(notebML00x, padx=10, pady=10, background="white")
frameML00x_StatsLuigiBeans = LabelFrame(frameML00x_StatsLuigi, text="Bean Uses", background="white", padx=7)
frameML00x_StatsLuigiBeans.place(x=130, y=170, width=110, height=170)
frameML00x_StatsLuigiLevels = LabelFrame(frameML00x_StatsLuigi, text="Level-Up Bonuses", background="white", padx=7)
frameML00x_StatsLuigiLevels.place(x=10, y=170, width=110, height=170)
frameML00x_StatsLuigiRanks = LabelFrame(frameML00x_StatsLuigi, text="Ranks", background="white", padx=1)
frameML00x_StatsLuigiRanks.place(x=250, y=120, width=220, height=220)

### Flags
frameML00x_Flags = Frame(notebML00x)
notebML00x_Flags = ttk.Notebook(frameML00x_Flags)
frameML00x_Flags_Abilities = Frame(frameML00x_Flags, background="white")
frameML00x_Flags_Abilities_OW = LabelFrame(frameML00x_Flags_Abilities, text="Real World Abilities", background="white")
frameML00x_Flags_Abilities_OW.place(x=10, y=10, width=160, height=175)
frameML00x_Flags_Abilities_DW = LabelFrame(frameML00x_Flags_Abilities, text="Dream World Abilities", background="white")
frameML00x_Flags_Abilities_DW.place(x=180, y=10, width=210, height=325)

frameML00x_Flags_Battle = Frame(frameML00x_Flags, bg="#FFFFFF")
frameML00x_Flags_Battle_Mario = LabelFrame(frameML00x_Flags_Battle, text="Mario's Bros. Attacks", bg="#FFFFFF")
frameML00x_Flags_Battle_Luigi = LabelFrame(frameML00x_Flags_Battle, text="Luigi's Bros. Attacks", bg="#FFFFFF")
frameML00x_Flags_Battle_Luiginary = LabelFrame(frameML00x_Flags_Battle, text="Luiginary Attacks", bg="#FFFFFF")
frameML00x_Flags_Battle_Other = LabelFrame(frameML00x_Flags_Battle, text="Miscellaneous", bg="#FFFFFF")
frameML00x_Flags_Battle_Mario.place(x=10, y=10, width=150, height=150)
frameML00x_Flags_Battle_Luigi.place(x=170, y=10, width=150, height=150)
frameML00x_Flags_Battle_Luiginary.place(x=330, y=10, width=160, height=180)
frameML00x_Flags_Battle_Other.place(x=10, y=170, width=310, height=150)

### Miscellaneous
frameML00x_Misc = Frame(notebML00x, padx=10, pady=10)

### Minimaps
frameML00x_Minimap = Frame(notebML00x)
notebML00x_Minimap = ttk.Notebook(frameML00x_Minimap)
minimapBlockBlimport = Frame(frameML00x_Minimap)
notebML00x.bind("<<NotebookTabChanged>>", tab_switch)

##### Tabs
notebML00x.add(frameML00x_StatsMario, text="Mario ")
notebML00x.add(frameML00x_StatsLuigi, text="Luigi ")
#notebML00x.add(frameML00x_Minimap, text="Minimap ")
notebML00x.add(frameML00x_Flags, text="Flags ")
notebML00x.add(frameML00x_Misc, text="Miscellaneous ")
notebML00x_Flags.add(frameML00x_Flags_Abilities, text="Abilities ")
notebML00x_Flags.add(frameML00x_Flags_Battle, text="Battle ")
notebML00x_Minimap.add(minimapBlockBlimport, text="Pi'illo Blimport ")
notebML00x.pack(ipadx=500, ipady=500)
notebML00x_Minimap.pack(ipadx=500, ipady=500)
notebML00x_Flags.pack(ipadx=500, ipady=500)

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
Spinlam = lambda a, b, c, d: Spinbox(a, from_=b, to=c, width=d, relief="flat", highlightthickness=1, highlightbackground="#999999", buttondownrelief=SUNKEN)
# ^^^^^^ Refer to https://discord.com/channels/267624335836053506/1195368132076896326 for more methods ^^^^^^
Checklam = lambda a, b, c: Checkbutton(a, text=b, variable=c, background="#FFFFFF", activebackground="#FFFFFF", activeforeground="#666666")
class MarioStatsPage:
    ##### Mario Stats Page
    mCurHPText = Labellam(frameML00x_StatsMario, "Current HP")
    mMaxHPText = Labellam(frameML00x_StatsMario, "Max HP")
    mCurBPText = Labellam(frameML00x_StatsMario, "Current BP")
    mMaxBPText = Labellam(frameML00x_StatsMario, "Max BP")
    mPowerText = Labellam(frameML00x_StatsMario, "Pow")
    mDefenseText = Labellam(frameML00x_StatsMario, "Defense")
    mSpeedText = Labellam(frameML00x_StatsMario, "Speed")
    mStacheText = Labellam(frameML00x_StatsMario, "Stache")
    mLevelText = Labellam(frameML00x_StatsMario, "Level")
    mEXPText = Labellam(frameML00x_StatsMario, "EXP")
    mMaxHPBeanText = Labellam(frameML00x_StatsMarioBeans, "Max HP")
    mMaxBPBeanText = Labellam(frameML00x_StatsMarioBeans, "Max BP")
    mPowerBeanText = Labellam(frameML00x_StatsMarioBeans, "Power")
    mDefenseBeanText = Labellam(frameML00x_StatsMarioBeans, "Defense")
    mSpeedBeanText = Labellam(frameML00x_StatsMarioBeans, "Speed")
    mStacheBeanText = Labellam(frameML00x_StatsMarioBeans, "Stache")
    mMaxHPLevelText = Labellam(frameML00x_StatsMarioLevels, "Max HP")
    mMaxBPLevelText = Labellam(frameML00x_StatsMarioLevels, "Max BP")
    mPowerLevelText = Labellam(frameML00x_StatsMarioLevels, "Power")
    mDefenseLevelText = Labellam(frameML00x_StatsMarioLevels, "Defense")
    mSpeedLevelText = Labellam(frameML00x_StatsMarioLevels, "Speed")
    mStacheLevelText = Labellam(frameML00x_StatsMarioLevels, "Stache")
    mRankBonus1Text = Labellam(frameML00x_StatsMarioRanks, "Shell Rank...")
    mRankBonus2Text = Labellam(frameML00x_StatsMarioRanks, "Flower Rank...")
    mRankBonus3Text = Labellam(frameML00x_StatsMarioRanks, "Star Rank...")
    mRankBonus4Text = Labellam(frameML00x_StatsMarioRanks, "Rainbow Rank...")
    mRankBonus5Text = Labellam(frameML00x_StatsMarioRanks, "Extra Bonus...")

    mCurHPScroll = Spinlam(frameML00x_StatsMario, 1, 999, 4)
    mMaxHPScroll = Spinlam(frameML00x_StatsMario, 1, 999, 4)
    mCurBPScroll = Spinlam(frameML00x_StatsMario, 1, 999, 4)
    mMaxBPScroll = Spinlam(frameML00x_StatsMario, 1, 999, 4)
    mPowerScroll = Spinlam(frameML00x_StatsMario, 1, 999, 4)
    mDefenseScroll = Spinlam(frameML00x_StatsMario, 1, 999, 4)
    mSpeedScroll = Spinlam(frameML00x_StatsMario, 1, 999, 4)
    mStacheScroll = Spinlam(frameML00x_StatsMario, 1, 999, 4)
    mLevelScroll = Spinlam(frameML00x_StatsMario, 1, 100, 4)
    mEXPScroll = Spinlam(frameML00x_StatsMario, 0, 9999999, 8)
    mMaxHPBeanScroll = Spinlam(frameML00x_StatsMarioBeans, 0, 999, 4)
    mMaxBPBeanScroll = Spinlam(frameML00x_StatsMarioBeans, 0, 999, 4)
    mPowerBeanScroll = Spinlam(frameML00x_StatsMarioBeans, 0, 999, 4)
    mDefenseBeanScroll = Spinlam(frameML00x_StatsMarioBeans, 0, 999, 4)
    mSpeedBeanScroll = Spinlam(frameML00x_StatsMarioBeans, 0, 999, 4)
    mStacheBeanScroll = Spinlam(frameML00x_StatsMarioBeans, 0, 999, 4)
    mMaxHPLevelScroll = Spinlam(frameML00x_StatsMarioLevels, 0, 999, 4)
    mMaxBPLevelScroll = Spinlam(frameML00x_StatsMarioLevels, 0, 999, 4)
    mPowerLevelScroll = Spinlam(frameML00x_StatsMarioLevels, 0, 999, 4)
    mDefenseLevelScroll = Spinlam(frameML00x_StatsMarioLevels, 0, 999, 4)
    mSpeedLevelScroll = Spinlam(frameML00x_StatsMarioLevels, 0, 999, 4)
    mStacheLevelScroll = Spinlam(frameML00x_StatsMarioLevels, 0, 999, 4)
    mResetStatsButton = Button(frameML00x_StatsMario, text="Reset Stats (Level 1)", width=27, height=3, command=resetstatsmario)
    mMaxStatsButton = Button(frameML00x_StatsMario, text="Max Stats (level 100)", width=27, height=3, command=maxstatsmario)

    ### Mario Ranks
    varMarioRank = StringVar()
    varMarioBonus1 = StringVar()
    varMarioBonus2 = StringVar()
    varMarioBonus3 = StringVar()
    varMarioBonus4 = StringVar()
    varMarioBonus5 = StringVar()
    mRank = ttk.Combobox(frameML00x_StatsMarioRanks, textvariable=varMarioRank, width=15)
    mRank["values"] = allRanks; mRank["state"] = "readonly"
    mRankText = Labellam(frameML00x_StatsMarioRanks, "Current Rank: ")
    mBonus1 = ttk.Combobox(frameML00x_StatsMarioRanks, textvariable=varMarioBonus1, width=15)
    mBonus1["values"] = allBonuses; mBonus1["state"] = "readonly"
    mBonus2 = ttk.Combobox(frameML00x_StatsMarioRanks, textvariable=varMarioBonus2, width=15)
    mBonus2["values"] = allBonuses; mBonus2["state"] = "readonly"
    mBonus3 = ttk.Combobox(frameML00x_StatsMarioRanks, textvariable=varMarioBonus3, width=15)
    mBonus3["values"] = allBonuses; mBonus3["state"] = "readonly"
    mBonus4 = ttk.Combobox(frameML00x_StatsMarioRanks, textvariable=varMarioBonus4, width=15)
    mBonus4["values"] = allBonuses; mBonus4["state"] = "readonly"
    mBonus5 = ttk.Combobox(frameML00x_StatsMarioRanks, textvariable=varMarioBonus5, width=15)
    mBonus5["values"] = allBonuses; mBonus5["state"] = "readonly"
    mExtraGear = Spinlam(frameML00x_StatsMarioRanks, 1, 3, 2)
    mExtraGearText = Labellam(frameML00x_StatsMarioRanks, "No. Gear Slots")
    mExtraGearText.grid(row=0, column=0, sticky=E)
    mExtraGear.grid(row=0, column=1, sticky=W)
    universalBadgeSlots = Spinlam(frameML00x_StatsMarioRanks, 2, 4, 2)
    universalBadgeSlotsText = Labellam(frameML00x_StatsMarioRanks, "No. Badge Slots")
    universalBadgeSlotsText.grid(row=1, column=0, sticky=E)
    universalBadgeSlots.grid(row=1, column=1, sticky=W)
    mRankText.grid(row=2, column=0, sticky=E)
    mRank.grid(row=2, column=1, sticky=W, pady=(2, 6))
    mRankBonus1Text.grid(row=3, column=0, sticky=E, padx=(3,0))
    mRankBonus2Text.grid(row=4, column=0, sticky=E, padx=(3,0))
    mRankBonus3Text.grid(row=5, column=0, sticky=E, padx=(3,0))
    mRankBonus4Text.grid(row=6, column=0, sticky=E, padx=(3,0))
    mRankBonus5Text.grid(row=7, column=0, sticky=E, padx=(3,0))
    mBonus1.grid(row=3, column=1, sticky=W, pady=2)
    mBonus2.grid(row=4, column=1, sticky=W, pady=2)
    mBonus3.grid(row=5, column=1, sticky=W, pady=2)
    mBonus4.grid(row=6, column=1, sticky=W, pady=2)
    mBonus5.grid(row=7, column=1, sticky=W, pady=2)
    ### End Mario Ranks

    mResetStatsButton.place(x=260, y=2)
    mMaxStatsButton.place(x=260, y=64)
    mCurHPText.grid(row=0, column=0, sticky=E)
    mMaxHPText.grid(row=1, column=0, sticky=E)
    mCurBPText.grid(row=2, column=0, sticky=E)
    mMaxBPText.grid(row=3, column=0, sticky=E)
    mPowerText.grid(row=0, column=4, sticky=E, padx=(20,0))
    mDefenseText.grid(row=1, column=4, sticky=E, padx=(20,0))
    mSpeedText.grid(row=2, column=4, sticky=E, padx=(20,0))
    mStacheText.grid(row=3, column=4, sticky=E, padx=(20,0))
    mLevelText.grid(row=4, column=0, sticky=E, padx=(20,0))
    mEXPText.grid(row=4, column=4, sticky=E)
    mMaxHPBeanText.grid(row=0, column=0, sticky=E)
    mMaxBPBeanText.grid(row=1, column=0, sticky=E)
    mPowerBeanText.grid(row=2, column=0, sticky=E)
    mDefenseBeanText.grid(row=3, column=0, sticky=E)
    mSpeedBeanText.grid(row=4, column=0, sticky=E)
    mStacheBeanText.grid(row=5, column=0, sticky=E)
    mMaxHPLevelText.grid(row=0, column=0, sticky=E)
    mMaxBPLevelText.grid(row=1, column=0, sticky=E)
    mPowerLevelText.grid(row=2, column=0, sticky=E)
    mDefenseLevelText.grid(row=3, column=0, sticky=E)
    mSpeedLevelText.grid(row=4, column=0, sticky=E)
    mStacheLevelText.grid(row=5, column=0, sticky=E)

    mCurHPScroll.grid(row=0, column=1, sticky=W, pady=2)
    mMaxHPScroll.grid(row=1, column=1, sticky=W, pady=2)
    mCurBPScroll.grid(row=2, column=1, sticky=W, pady=2)
    mMaxBPScroll.grid(row=3, column=1, sticky=W, pady=2)
    mPowerScroll.grid(row=0, column=5, sticky=W, pady=2)
    mDefenseScroll.grid(row=1, column=5, sticky=W, pady=2)
    mSpeedScroll.grid(row=2, column=5, sticky=W, pady=2)
    mStacheScroll.grid(row=3, column=5, sticky=W, pady=2)
    mLevelScroll.grid(row=4, column=1, sticky=W, pady=6)
    mEXPScroll.grid(row=4, column=5, sticky=W, pady=6)
    mMaxHPBeanScroll.grid(row=0, column=1, sticky=W, pady=2)
    mMaxBPBeanScroll.grid(row=1, column=1, sticky=W, pady=2)
    mPowerBeanScroll.grid(row=2, column=1, sticky=W, pady=2)
    mDefenseBeanScroll.grid(row=3, column=1, sticky=W, pady=2)
    mSpeedBeanScroll.grid(row=4, column=1, sticky=W, pady=2)
    mStacheBeanScroll.grid(row=5, column=1, sticky=W, pady=2)
    mMaxHPLevelScroll.grid(row=0, column=1, sticky=W, pady=2)
    mMaxBPLevelScroll.grid(row=1, column=1, sticky=W, pady=2)
    mPowerLevelScroll.grid(row=2, column=1, sticky=W, pady=2)
    mDefenseLevelScroll.grid(row=3, column=1, sticky=W, pady=2)
    mSpeedLevelScroll.grid(row=4, column=1, sticky=W, pady=2)
    mStacheLevelScroll.grid(row=5, column=1, sticky=W, pady=2)

class LuigiStatsPage:
    ##### Mario Stats Page
    mCurHPText = Labellam(frameML00x_StatsLuigi, "Current HP")
    mMaxHPText = Labellam(frameML00x_StatsLuigi, "Max HP")
    mCurBPText = Labellam(frameML00x_StatsLuigi, "Current BP")
    mMaxBPText = Labellam(frameML00x_StatsLuigi, "Max BP")
    mPowerText = Labellam(frameML00x_StatsLuigi, "Pow")
    mDefenseText = Labellam(frameML00x_StatsLuigi, "Defense")
    mSpeedText = Labellam(frameML00x_StatsLuigi, "Speed")
    mStacheText = Labellam(frameML00x_StatsLuigi, "Stache")
    mLevelText = Labellam(frameML00x_StatsLuigi, "Level")
    mEXPText = Labellam(frameML00x_StatsLuigi, "EXP")
    mMaxHPBeanText = Labellam(frameML00x_StatsLuigiBeans, "Max HP")
    mMaxBPBeanText = Labellam(frameML00x_StatsLuigiBeans, "Max BP")
    mPowerBeanText = Labellam(frameML00x_StatsLuigiBeans, "Power")
    mDefenseBeanText = Labellam(frameML00x_StatsLuigiBeans, "Defense")
    mSpeedBeanText = Labellam(frameML00x_StatsLuigiBeans, "Speed")
    mStacheBeanText = Labellam(frameML00x_StatsLuigiBeans, "Stache")
    mMaxHPLevelText = Labellam(frameML00x_StatsLuigiLevels, "Max HP")
    mMaxBPLevelText = Labellam(frameML00x_StatsLuigiLevels, "Max BP")
    mPowerLevelText = Labellam(frameML00x_StatsLuigiLevels, "Power")
    mDefenseLevelText = Labellam(frameML00x_StatsLuigiLevels, "Defense")
    mSpeedLevelText = Labellam(frameML00x_StatsLuigiLevels, "Speed")
    mStacheLevelText = Labellam(frameML00x_StatsLuigiLevels, "Stache")
    mRankBonus1Text = Labellam(frameML00x_StatsLuigiRanks, "Shell Rank...")
    mRankBonus2Text = Labellam(frameML00x_StatsLuigiRanks, "Flower Rank...")
    mRankBonus3Text = Labellam(frameML00x_StatsLuigiRanks, "Star Rank...")
    mRankBonus4Text = Labellam(frameML00x_StatsLuigiRanks, "Rainbow Rank...")
    mRankBonus5Text = Labellam(frameML00x_StatsLuigiRanks, "Extra Bonus...")

    mCurHPScroll = Spinlam(frameML00x_StatsLuigi, 1, 999, 4)
    mMaxHPScroll = Spinlam(frameML00x_StatsLuigi, 1, 999, 4)
    mCurBPScroll = Spinlam(frameML00x_StatsLuigi, 1, 999, 4)
    mMaxBPScroll = Spinlam(frameML00x_StatsLuigi, 1, 999, 4)
    mPowerScroll = Spinlam(frameML00x_StatsLuigi, 1, 999, 4)
    mDefenseScroll = Spinlam(frameML00x_StatsLuigi, 1, 999, 4)
    mSpeedScroll = Spinlam(frameML00x_StatsLuigi, 1, 999, 4)
    mStacheScroll = Spinlam(frameML00x_StatsLuigi, 1, 999, 4)
    mLevelScroll = Spinlam(frameML00x_StatsLuigi, 1, 100, 4)
    mEXPScroll = Spinlam(frameML00x_StatsLuigi, 0, 9999999, 8)
    mMaxHPBeanScroll = Spinlam(frameML00x_StatsLuigiBeans, 0, 999, 4)
    mMaxBPBeanScroll = Spinlam(frameML00x_StatsLuigiBeans, 0, 999, 4)
    mPowerBeanScroll = Spinlam(frameML00x_StatsLuigiBeans, 0, 999, 4)
    mDefenseBeanScroll = Spinlam(frameML00x_StatsLuigiBeans, 0, 999, 4)
    mSpeedBeanScroll = Spinlam(frameML00x_StatsLuigiBeans, 0, 999, 4)
    mStacheBeanScroll = Spinlam(frameML00x_StatsLuigiBeans, 0, 999, 4)
    mMaxHPLevelScroll = Spinlam(frameML00x_StatsLuigiLevels, 0, 999, 4)
    mMaxBPLevelScroll = Spinlam(frameML00x_StatsLuigiLevels, 0, 999, 4)
    mPowerLevelScroll = Spinlam(frameML00x_StatsLuigiLevels, 0, 999, 4)
    mDefenseLevelScroll = Spinlam(frameML00x_StatsLuigiLevels, 0, 999, 4)
    mSpeedLevelScroll = Spinlam(frameML00x_StatsLuigiLevels, 0, 999, 4)
    mStacheLevelScroll = Spinlam(frameML00x_StatsLuigiLevels, 0, 999, 4)
    mResetStatsButton = Button(frameML00x_StatsLuigi, text="Reset Stats (Level 1)", width=27, height=3, command=resetstatsluigi)
    mMaxStatsButton = Button(frameML00x_StatsLuigi, text="Max Stats (level 100)", width=27, height=3, command=maxstatsluigi)

    ### Mario Ranks
    varLuigiRank = StringVar()
    varLuigiBonus1 = StringVar()
    varLuigiBonus2 = StringVar()
    varLuigiBonus3 = StringVar()
    varLuigiBonus4 = StringVar()
    varLuigiBonus5 = StringVar()
    mRank = ttk.Combobox(frameML00x_StatsLuigiRanks, textvariable=varLuigiRank, width=15)
    mRank["values"] = allRanks; mRank["state"] = "readonly"
    mRankText = Labellam(frameML00x_StatsLuigiRanks, "Current Rank: ")
    mBonus1 = ttk.Combobox(frameML00x_StatsLuigiRanks, textvariable=varLuigiBonus1, width=15)
    mBonus1["values"] = allBonuses; mBonus1["state"] = "readonly"
    mBonus2 = ttk.Combobox(frameML00x_StatsLuigiRanks, textvariable=varLuigiBonus2, width=15)
    mBonus2["values"] = allBonuses; mBonus2["state"] = "readonly"
    mBonus3 = ttk.Combobox(frameML00x_StatsLuigiRanks, textvariable=varLuigiBonus3, width=15)
    mBonus3["values"] = allBonuses; mBonus3["state"] = "readonly"
    mBonus4 = ttk.Combobox(frameML00x_StatsLuigiRanks, textvariable=varLuigiBonus4, width=15)
    mBonus4["values"] = allBonuses; mBonus4["state"] = "readonly"
    mBonus5 = ttk.Combobox(frameML00x_StatsLuigiRanks, textvariable=varLuigiBonus5, width=15)
    mBonus5["values"] = allBonuses; mBonus5["state"] = "readonly"
    mExtraGear = Spinlam(frameML00x_StatsLuigiRanks, 1, 3, 2)
    mExtraGearText = Labellam(frameML00x_StatsLuigiRanks, "No. Gear Slots")
    mExtraGearText.grid(row=0, column=0, sticky=E)
    mExtraGear.grid(row=0, column=1, sticky=W)
    universalBadgeSlots = Spinlam(frameML00x_StatsLuigiRanks, 2, 4, 2)
    universalBadgeSlotsText = Labellam(frameML00x_StatsLuigiRanks, "No. Badge Slots")
    universalBadgeSlotsText.grid(row=1, column=0, sticky=E)
    universalBadgeSlots.grid(row=1, column=1, sticky=W)
    mRankText.grid(row=2, column=0, sticky=E)
    mRank.grid(row=2, column=1, sticky=W, pady=(2, 6))
    mRankBonus1Text.grid(row=3, column=0, sticky=E, padx=(3,0))
    mRankBonus2Text.grid(row=4, column=0, sticky=E, padx=(3,0))
    mRankBonus3Text.grid(row=5, column=0, sticky=E, padx=(3,0))
    mRankBonus4Text.grid(row=6, column=0, sticky=E, padx=(3,0))
    mRankBonus5Text.grid(row=7, column=0, sticky=E, padx=(3,0))
    mBonus1.grid(row=3, column=1, sticky=W, pady=2)
    mBonus2.grid(row=4, column=1, sticky=W, pady=2)
    mBonus3.grid(row=5, column=1, sticky=W, pady=2)
    mBonus4.grid(row=6, column=1, sticky=W, pady=2)
    mBonus5.grid(row=7, column=1, sticky=W, pady=2)
    ### End Mario Ranks

    mResetStatsButton.place(x=260, y=2)
    mMaxStatsButton.place(x=260, y=64)
    mCurHPText.grid(row=0, column=0, sticky=E)
    mMaxHPText.grid(row=1, column=0, sticky=E)
    mCurBPText.grid(row=2, column=0, sticky=E)
    mMaxBPText.grid(row=3, column=0, sticky=E)
    mPowerText.grid(row=0, column=4, sticky=E, padx=(20,0))
    mDefenseText.grid(row=1, column=4, sticky=E, padx=(20,0))
    mSpeedText.grid(row=2, column=4, sticky=E, padx=(20,0))
    mStacheText.grid(row=3, column=4, sticky=E, padx=(20,0))
    mLevelText.grid(row=4, column=0, sticky=E, padx=(20,0))
    mEXPText.grid(row=4, column=4, sticky=E)
    mMaxHPBeanText.grid(row=0, column=0, sticky=E)
    mMaxBPBeanText.grid(row=1, column=0, sticky=E)
    mPowerBeanText.grid(row=2, column=0, sticky=E)
    mDefenseBeanText.grid(row=3, column=0, sticky=E)
    mSpeedBeanText.grid(row=4, column=0, sticky=E)
    mStacheBeanText.grid(row=5, column=0, sticky=E)
    mMaxHPLevelText.grid(row=0, column=0, sticky=E)
    mMaxBPLevelText.grid(row=1, column=0, sticky=E)
    mPowerLevelText.grid(row=2, column=0, sticky=E)
    mDefenseLevelText.grid(row=3, column=0, sticky=E)
    mSpeedLevelText.grid(row=4, column=0, sticky=E)
    mStacheLevelText.grid(row=5, column=0, sticky=E)

    mCurHPScroll.grid(row=0, column=1, sticky=W, pady=2)
    mMaxHPScroll.grid(row=1, column=1, sticky=W, pady=2)
    mCurBPScroll.grid(row=2, column=1, sticky=W, pady=2)
    mMaxBPScroll.grid(row=3, column=1, sticky=W, pady=2)
    mPowerScroll.grid(row=0, column=5, sticky=W, pady=2)
    mDefenseScroll.grid(row=1, column=5, sticky=W, pady=2)
    mSpeedScroll.grid(row=2, column=5, sticky=W, pady=2)
    mStacheScroll.grid(row=3, column=5, sticky=W, pady=2)
    mLevelScroll.grid(row=4, column=1, sticky=W, pady=6)
    mEXPScroll.grid(row=4, column=5, sticky=W, pady=6)
    mMaxHPBeanScroll.grid(row=0, column=1, sticky=W, pady=2)
    mMaxBPBeanScroll.grid(row=1, column=1, sticky=W, pady=2)
    mPowerBeanScroll.grid(row=2, column=1, sticky=W, pady=2)
    mDefenseBeanScroll.grid(row=3, column=1, sticky=W, pady=2)
    mSpeedBeanScroll.grid(row=4, column=1, sticky=W, pady=2)
    mStacheBeanScroll.grid(row=5, column=1, sticky=W, pady=2)
    mMaxHPLevelScroll.grid(row=0, column=1, sticky=W, pady=2)
    mMaxBPLevelScroll.grid(row=1, column=1, sticky=W, pady=2)
    mPowerLevelScroll.grid(row=2, column=1, sticky=W, pady=2)
    mDefenseLevelScroll.grid(row=3, column=1, sticky=W, pady=2)
    mSpeedLevelScroll.grid(row=4, column=1, sticky=W, pady=2)
    mStacheLevelScroll.grid(row=5, column=1, sticky=W, pady=2)

class Flag_AbilityPage:
    owHammerVar = IntVar()
    owHammerMiniVar = IntVar()
    owHammerMoleVar = IntVar()
    owSpinJumpVar = IntVar()
    owSideDrillVar = IntVar()
    owBallHopVar = IntVar()
    dwBButtonVar = IntVar()
    dwStackVar = IntVar()
    dwStackGroundPoundVar = IntVar()
    dwStackSpingJumpVar = IntVar()
    dwConeVar = IntVar()
    dwConeJumpVar = IntVar()
    dwConeTornadoVar = IntVar()
    dwBallVar = IntVar()
    dwBallSlingshotVar = IntVar()
    dwBallHammerVar = IntVar()
    dwDropVar = IntVar()
    dwWallkickVar = IntVar()
    owHammers = Checklam(frameML00x_Flags_Abilities_OW, "Hammers", owHammerVar)
    owHammerMini = Checklam(frameML00x_Flags_Abilities_OW, "Hammers: Mini Mario", owHammerMiniVar)
    owHammerMole = Checklam(frameML00x_Flags_Abilities_OW, "Hammers: Mole Mario", owHammerMoleVar)
    owSpinJump = Checklam(frameML00x_Flags_Abilities_OW, "Spin Jump", owSpinJumpVar)
    owSideDrill = Checklam(frameML00x_Flags_Abilities_OW, "Side Drill", owSideDrillVar)
    owBallHop = Checklam(frameML00x_Flags_Abilities_OW, "Ball Hop", owBallHopVar)
    dwBButton = Checklam(frameML00x_Flags_Abilities_DW, "Enter Luiginary Works (B Button)", dwBButtonVar)
    dwDrop = Checklam(frameML00x_Flags_Abilities_DW, "Luiginary Generator: Drop", dwDropVar)
    dwStack = Checklam(frameML00x_Flags_Abilities_DW, "Luiginary Stack", dwStackVar)
    dwStackGroundPound = Checklam(frameML00x_Flags_Abilities_DW, "Luiginary Stack: Ground Pound", dwStackGroundPoundVar)
    dwStackSpingJump = Checklam(frameML00x_Flags_Abilities_DW, "Luiginary Stack: Spring Jump", dwStackSpingJumpVar)
    dwCone = Checklam(frameML00x_Flags_Abilities_DW, "Luiginary Cone", dwConeVar)
    dwConeJump = Checklam(frameML00x_Flags_Abilities_DW, "Luiginary Cone: Jump", dwConeJumpVar)
    dwConeTornado = Checklam(frameML00x_Flags_Abilities_DW, "Luiginary Cone: Tornado", dwConeTornadoVar)
    dwBall = Checklam(frameML00x_Flags_Abilities_DW, "Luiginary Ball", dwBallVar)
    dwBallSlingshot = Checklam(frameML00x_Flags_Abilities_DW, "Luiginary Ball: Slingshot", dwBallSlingshotVar)
    dwBallHammer = Checklam(frameML00x_Flags_Abilities_DW, "Luiginary Ball: Hammer", dwBallHammerVar)
    dwWallkick = Checklam(frameML00x_Flags_Abilities_DW, "Luiginary Antigravity: Wallkick", dwWallkickVar)

    owHammers.grid(row=0, column=0, sticky=W)
    owHammerMini.grid(row=1, column=0, sticky=W)
    owHammerMole.grid(row=2, column=0, sticky=W)
    owSpinJump.grid(row=3, column=0, sticky=W)
    owSideDrill.grid(row=4, column=0, sticky=W)
    owBallHop.grid(row=5, column=0, sticky=W)
    dwBButton.grid(row=5, column=0, sticky=W)
    dwDrop.grid(row=6, column=0, sticky=W)
    dwStack.grid(row=7, column=0, sticky=W)
    dwStackGroundPound.grid(row=8, column=0, sticky=W)
    dwStackSpingJump.grid(row=9, column=0, sticky=W)
    dwCone.grid(row=10, column=0, sticky=W)
    dwConeJump.grid(row=11, column=0, sticky=W)
    dwConeTornado.grid(row=12, column=0, sticky=W)
    dwBall.grid(row=13, column=0, sticky=W)
    dwBallSlingshot.grid(row=14, column=0, sticky=W)
    dwBallHammer.grid(row=15, column=0, sticky=W)
    dwWallkick.grid(row=17, column=0, sticky=W)

class Flag_BattlePage:
    atkRedShellVar = IntVar()
    atkByeByeCannonVar = IntVar()
    atkBombDerbyVar = IntVar()
    atkJetBoardBashVar = IntVar()
    atkZeeEggVar = IntVar()
    atkGreenShellVar = IntVar()
    atkFireFlowerVar = IntVar()
    atkDropchopperVar = IntVar()
    atkSlingsniperVar = IntVar()
    atkStarRocketVar = IntVar()
    atkLuiginaryBallVar = IntVar()
    atkLuiginaryStackVar = IntVar()
    atkLuiginaryHammerVar = IntVar()
    atkLuiginaryFlameVar = IntVar()
    atkLuiginaryWallVar = IntVar()
    atkLuiginaryTyphoonVar = IntVar()
    flagBrosAttackVar = IntVar()
    flagLuiginaryAttackVar = IntVar()
    flagItemBlocksBattleVar = IntVar()
    flagBadgesInBattleVar = IntVar()

    atkRedShell = Checklam(frameML00x_Flags_Battle_Mario, "3D Red Shell", atkRedShellVar)
    atkByeByeCannon = Checklam(frameML00x_Flags_Battle_Mario, "Bye-Bye Cannon", atkByeByeCannonVar)
    atkBombDerby = Checklam(frameML00x_Flags_Battle_Mario, "Bomb Derby", atkBombDerbyVar)
    atkJetBoardBash = Checklam(frameML00x_Flags_Battle_Mario, "Jet Board Bash", atkJetBoardBashVar)
    atkZeeEgg = Checklam(frameML00x_Flags_Battle_Mario, "Zee Egg", atkZeeEggVar)
    atkGreenShell = Checklam(frameML00x_Flags_Battle_Luigi, "2D Green Shell", atkGreenShellVar)
    atkFireFlower = Checklam(frameML00x_Flags_Battle_Luigi, "Fire Flower", atkFireFlowerVar)
    atkDropchopper = Checklam(frameML00x_Flags_Battle_Luigi, "Dropchopper", atkDropchopperVar)
    atkSlingsniper = Checklam(frameML00x_Flags_Battle_Luigi, "Slingsniper", atkSlingsniperVar)
    atkStarRocket = Checklam(frameML00x_Flags_Battle_Luigi, "Star Rocket", atkStarRocketVar)
    atkLuiginaryBall = Checklam(frameML00x_Flags_Battle_Luiginary, "Luiginary Ball", atkLuiginaryBallVar)
    atkLuiginaryStack = Checklam(frameML00x_Flags_Battle_Luiginary, "Luiginary Stack", atkLuiginaryStackVar)
    atkLuiginaryHammer = Checklam(frameML00x_Flags_Battle_Luiginary, "Luiginary Hammer", atkLuiginaryHammerVar)
    atkLuiginaryFlame = Checklam(frameML00x_Flags_Battle_Luiginary, "Luiginary Flame", atkLuiginaryFlameVar)
    atkLuiginaryWall = Checklam(frameML00x_Flags_Battle_Luiginary, "Luiginary Wall", atkLuiginaryWallVar)
    atkLuiginaryTyphoon = Checklam(frameML00x_Flags_Battle_Luiginary, "Luiginary Typhoon", atkLuiginaryTyphoonVar)
    flagBrosAttack = Checklam(frameML00x_Flags_Battle_Other, "Enable Bros. Attacks in-battle", flagBrosAttackVar)
    flagLuiginaryAttack = Checklam(frameML00x_Flags_Battle_Other, "Enable Luiginary Attacks in-battle", flagLuiginaryAttackVar)
    flagItemBlocksBattle = Checklam(frameML00x_Flags_Battle_Other, "Enable Items in-battle", flagItemBlocksBattleVar)
    flagBadgesInBattle = Checklam(frameML00x_Flags_Battle_Other, "Enable Badges in-battle", flagBadgesInBattleVar)
    atkWarningText = Label(frameML00x_Flags_Battle, text="""    WARNING: Giving yourself
    Bros. Attacks and
    Luiginary Attacks before
    actually obtaining them in
    the game can break the
    game. Until this text is
    gone, USE THESE SETTINGS
    WITH CAUTION.
    Please backup your save!""", foreground="red", justify=LEFT, bg="#FFFFFF")
    atkWarningText.place(x=321, y=195)
    atkRedShell.grid(row=0, column=0, sticky=W)
    atkByeByeCannon.grid(row=1, column=0, sticky=W)
    atkBombDerby.grid(row=2, column=0, sticky=W)
    atkJetBoardBash.grid(row=3, column=0, sticky=W)
    atkZeeEgg.grid(row=4, column=0, sticky=W)
    atkGreenShell.grid(row=0, column=0, sticky=W)
    atkFireFlower.grid(row=1, column=0, sticky=W)
    atkDropchopper.grid(row=2, column=0, sticky=W)
    atkSlingsniper.grid(row=3, column=0, sticky=W)
    atkStarRocket.grid(row=4, column=0, sticky=W)
    atkLuiginaryBall.grid(row=0, column=0, sticky=W)
    atkLuiginaryStack.grid(row=1, column=0, sticky=W)
    atkLuiginaryHammer.grid(row=2, column=0, sticky=W)
    atkLuiginaryFlame.grid(row=3, column=0, sticky=W)
    atkLuiginaryWall.grid(row=4, column=0, sticky=W)
    atkLuiginaryTyphoon.grid(row=5, column=0, sticky=W)
    flagBrosAttack.grid(row=0, column=0, sticky=W)
    flagLuiginaryAttack.grid(row=1, column=0, sticky=W)
    flagItemBlocksBattle.grid(row=2, column=0, sticky=W)
    flagBadgesInBattle.grid(row=3, column=0, sticky=W)

class MiscellaneousPage:
    miscFileNumberVar = StringVar()
    miscFileNumberText = Labellam(frameML00x_Misc, "File Number: ")
    miscFileNumber = ttk.Combobox(frameML00x_Misc, textvariable=miscFileNumberVar, width=7)
    miscFileNumber["values"] = file1or2; miscFileNumber["state"]="readonly"
    miscFileNumberText.grid(row=0, column=1, sticky="E", padx=(10,0))
    miscFileNumber.grid(row=0, column=2, sticky="W")

    miscHardModeVar = IntVar()
    miscHardMode = Checklam(frameML00x_Misc, "Hard Mode?", miscHardModeVar)
    miscHardMode.grid(row=0, column=0, sticky="W")

    miscAllowPausingVar = IntVar()
    miscAllowPausing = Checklam(frameML00x_Misc, "Allow Pausing?", miscAllowPausingVar)
    miscAllowPausing.grid(row=1, column=0, sticky="W")

    miscShopFlagDozingVar = IntVar()
    miscShopFlagDriftwVar = IntVar()
    miscShopFlagSomnomVar = IntVar()
    miscShopFlagDozing = Checklam(frameML00x_Misc, "Shop Flag: Reached Dozing Sands", miscShopFlagDozingVar)
    miscShopFlagDriftw = Checklam(frameML00x_Misc, "Shop Flag: Reached Driftwood Shore", miscShopFlagDriftwVar)
    miscShopFlagSomnom = Checklam(frameML00x_Misc, "Shop Flag: Reached Somnom Woods", miscShopFlagSomnomVar)
    miscShopFlagDozing.grid(row=2, column=0, sticky="W")
    miscShopFlagDriftw.grid(row=3, column=0, sticky="W")
    miscShopFlagSomnom.grid(row=4, column=0, sticky="W")

    miscCoins = Spinlam(frameML00x_Misc, 0, 999999, 8)
    miscCoinsText = Labellam(frameML00x_Misc, "Coins: ")
    miscCoinsText.grid(row=1, column=1, sticky="E")
    miscCoins.grid(row=1, column=2, sticky="W")

################################
##### Minimap Editing Area #####
################################
imgs = []
class Maps: #Everything Minimap Related
    def minimapimage(canvasimport, image_, width, height):
        image = Image.open(image_)
        newimage = image.resize((width, height), Image.Resampling.BILINEAR)
        placement = (580-height)/2
        img = ImageTk.PhotoImage(newimage)
        imgs.append(img)
        canvasimport.create_image(3, 3, anchor=NW, image=img)
        canvasimport.place(x=0, y=placement)

    canvasBlimport = Canvas(minimapBlockBlimport, width=700, height=580)


def canvclick(canvasfind):
    #backg = canvasfind.cget("background")
    #if backg == "#FFFFFF":
    canvasfind.config(bg="Yellow")
    #    backgn = canvasfind.cget('bg')
    #    print(backgn)

class MapEdits:
    class MinimapBlimport:


        Maps.minimapimage(Maps.canvasBlimport, "Images/Minimaps/0.0 PiilloBlimport.png", 700, 400)
        block1Var = IntVar()
        block2Var = IntVar()
        block3Var = IntVar()
        block4Var = IntVar()
        block5Var = IntVar()
        block6Var = IntVar()
        block7Var = IntVar()
        block8Var = IntVar()
        block9Var = IntVar()
        block10Var = IntVar()
        block11Var = IntVar()
        block12Var = IntVar()

        block1 = Checkbutton(Maps.canvasBlimport)
        block2 = Checkbutton(Maps.canvasBlimport)
        block3 = Checkbutton(Maps.canvasBlimport)
        block4 = Checkbutton(Maps.canvasBlimport)
        block5 = Checkbutton(Maps.canvasBlimport)
        block6 = Checkbutton(Maps.canvasBlimport)
        block7 = Checkbutton(Maps.canvasBlimport)
        block8 = Checkbutton(Maps.canvasBlimport)
        block9 = Checkbutton(Maps.canvasBlimport)
        block10 = Checkbutton(Maps.canvasBlimport)
        block11 = Checkbutton(Maps.canvasBlimport)
        block12 = Checkbutton(Maps.canvasBlimport)

        canvasLine = Canvas(Maps.canvasBlimport, width=8, height=8, bg="black")
        canvasLnew = Canvas(Maps.canvasBlimport, width=8, height=8, bg="black")
        canvasLine.place(x=227, y=190)
        #canvasLine.tag_bind(canvasLnew, '<1>', canvclick(canvasLine))
        #canvasLine.create_line(10,10, 150, 170)
        block1.place(x=10, y=30)
        block2.place(x=10, y=30)
        block3.place(x=10, y=30)
        block4.place(x=10, y=30)
        block5.place(x=10, y=30)
        block6.place(x=10, y=30)
        block7.place(x=10, y=30)
        block8.place(x=10, y=30)
        block9.place(x=10, y=30)
        block10.place(x=10, y=30)
        block11.place(x=10, y=30)
        block12.place(x=10, y=30)

mainWindow.mainloop()
