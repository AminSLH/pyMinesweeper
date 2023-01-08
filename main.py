# Created by Amine Bouslah in 2021
# In the "squares" list, I track the number of mines surrounding each square.
# The squares are indexed from 0 to n-1, from left to right and from top to bottom.
# Squares are "active" by default and become inactive after clicking them.
from tkinter import *
from random import randint
from pathlib import Path
import time
import winsound


# create base variables
a = 10  # board side length
n = a * a  # number of squares on board
m = 10  # number of mines on board


# function to that returns the set of surrounding squares
def setofneighbors(ind, a):
    r = set()
    n = a * a
    if ind == 0:
        r.add(ind + 1)
        r.add(ind + a)
        r.add(ind + a + 1)
    elif ind == a - 1:
        r.add(ind - 1)
        r.add(ind + a - 1)
        r.add(ind + a)
    elif ind == n - a:
        r.add(ind - a)
        r.add(ind - a + 1)
        r.add(ind + 1)
    elif ind == n - 1:
        r.add(ind - 1)
        r.add(ind - a)
        r.add(ind - a - 1)
    elif ind < a - 1:
        offsets = {-1, 1, a - 1, a, a + 1}
        for e in offsets:
            r.add(ind + e)
    elif ind % a == 0:
        offsets = {-a, 1 - a, 1, a, a + 1}
        for e in offsets:
            r.add(ind + e)
    elif ind > n - a:
        offsets = {-1 - a, -a, 1 - a, -1, 1}
        for e in offsets:
            r.add(ind + e)
    elif ind % a == (a - 1):
        offsets = {-a - 1, -a, -1, a - 1, a}
        for e in offsets:
            r.add(ind + e)
    else:
        offsets = {1, -1, a, -a, a + 1, -1 - a, a - 1, 1 - a}
        for e in offsets:
            r.add(ind + e)
    return r


# function that creates new variables to track the board
def initializefnc():
    global n, a, m, squares, isactive, issafe, isflagged, mines
    squares = [0] * n
    mines = []
    # Place unique mines on the board
    for i in range(m):
        rng = randint(0, n - 1)
        while rng in mines:
            rng = randint(0, n - 1)
        mines.append(rng)
        for e in setofneighbors(mines[i], a):
            squares[e] += 1

    # track whether or not each square is active
    isactive = [True] * n

    # track whether or not a square is flagged
    isflagged = [False] * n

    # track whether or not each square if safe
    issafe = []
    for i in range(n):
        if i in mines:
            issafe.append(False)
        else:
            issafe.append(True)


# function to check for loss/win
def checkwin(a):
    global win, loss, mines, isflagged, button_identities
    if loss:
        winsound.PlaySound("resources/boom1.wav", winsound.SND_FILENAME)
        Label(sf, image=YouLose, borderwidth=0, anchor="w").pack()
        f1.update_idletasks()
        time.sleep(0.2)
        for e in mines:
            if not isflagged[e]:
                transformsq(e)
    else:
        i = 0
        win = True
        while (i < a * a) and win:
            if isactive[i] and (not (i in mines)):
                win = False
            i += 1
        if win:
            Label(sf, image=YouWin, borderwidth=0, anchor="w").pack()
            for e in mines:
                if not isflagged[e]:
                    button_identities[e].configure(bg="#00D607")
            winsound.PlaySound("resources/win.wav", winsound.SND_FILENAME)
    if win or loss:
        setofflagged = set()
        for i in range(a**2):
            if isflagged[i]:
                setofflagged.add(i)
        for e in setofflagged:
            if e in mines:
                button_identities[e].configure(bg="#00D607")
                f1.update_idletasks()



# function that presses a square
def transformsq(cbi):
    isactive[cbi] = False
    if issafe[cbi]:
        if squares[cbi] == 0:
            button_identities[cbi].configure(
                bg="#8489b9",
                text=" ",
                width=root.winfo_fpixels("1c"),
                height=root.winfo_fpixels("1c"),
                relief="sunken",
                borderwidth=1,
            )
        else:
            button_identities[cbi].configure(
                bg="#8489b9",
                text=str(squares[cbi]),
                width=root.winfo_fpixels("1c"),
                height=root.winfo_fpixels("1c"),
                relief="sunken",
                borderwidth=1,
            )
    else:
        global MineImg
        button_identities[cbi].configure(
            image=MineImg,
            compound="none",
            bg="red",
            width=root.winfo_fpixels("1c"),
            height=root.winfo_fpixels("1c"),
            relief="groove",
            borderwidth=1,
        )
    f1.update_idletasks()


# function that presses a "0" squares' neighbors
def transformsurrounding(cbi, a):
    transformsq(cbi)
    SoN = setofneighbors(cbi, a)
    SoR = set()
    for current_square in SoN:
        if isactive[current_square]:
            transformsq(current_square)
            if squares[current_square] == 0:
                SoR.add(current_square)
    for current_square in SoR:
        transformsurrounding(current_square, a)


# Left click a square
def sqfunc(event):
    global loss, a, button_identities
    cbi = button_identities.index(event.widget)
    if isactive[cbi] and (not loss) and (not win) and (not isflagged[cbi]):
        transformsq(cbi)
        if cbi in mines:
            loss = True
        else:
            global squares
            transformsq(cbi)
            if squares[cbi] == 0:
                transformsurrounding(cbi, a)
        checkwin(a)


# Right click a square
def flagfn(event):
    global blank, win, loss
    if (not win) and (not loss):
        global isflagged, isactive, button_identities
        cbi = button_identities.index(event.widget)
        if isactive[cbi]:
            if isflagged[cbi]:
                isflagged[cbi] = False
                button_identities[cbi].configure(
                    image=blank,
                    compound="center",
                    bg="#4A74E2",
                    width=root.winfo_fpixels("1c"),
                    height=root.winfo_fpixels("1c"),
                    relief="raised",
                )
            else:
                isflagged[cbi] = True
                button_identities[cbi].configure(
                    image=FlagImg,
                    compound="none",
                    bg="#4A74E2",
                    width=root.winfo_fpixels("1c"),
                    height=root.winfo_fpixels("1c"),
                    relief="raised",
                )


# middle click a square
def middleclick(event):
    global squares, isflagged, button_identities, a, mines, loss
    cbi = button_identities.index(event.widget)
    for e in setofneighbors(cbi, a):
        if not isflagged[e] and not win and not loss:
            transformsq(e)
            if e in mines:
                loss = True
                checkwin(a)
                break
            checkwin(a)
            if squares[e] == 0 and not loss and not win:
                transformsurrounding(e, a)
                checkwin(a)


# make new GUI Board
def startgame():
    global f1, sf, loss, win, start, button_identities, first_time
    initializefnc()
    f1.destroy()
    f1 = Frame(root, relief="solid")
    f1.grid(row=0, column=0, sticky="n")
    sf.destroy()
    sf = Frame(f2, width=300)
    sf.grid(row=1, sticky="n")

    button_identities = []
    for i in range(a):
        for j in range(a):
            sq = Label(
                f1,
                image=blank,
                compound="center",
                bg="#436AD0",
                fg="#FFA216",
                width=root.winfo_fpixels("1c"),
                height=root.winfo_fpixels("1c"),
                relief="raised",
                font="TkIconFont 16 bold",
            )
            sq.grid(row=i, column=j)
            button_identities.append(sq)
            sq.bind("<Button-1>", sqfunc)
            sq.bind("<Button-3>", flagfn)
            sq.bind("<Button-2>", middleclick)

    loss = False
    win = False
    start = False
    if first_time:
        time.sleep(2)
    winsound.PlaySound("resources/start.wav", winsound.SND_FILENAME)
    first_time = False


# Prompt GUI
def popup():
    global start, a, m, n
    prompt = Tk()
    prompt.minsize(width=230, height=220)
    prompt.title("Options")

    def startfnc():
        global start, a, m, n
        ta = abox.get()
        tm = mbox.get()
        if (
            ta.isdigit()
            and tm.isdigit()
            and int(tm) > 0
            and int(ta) > 1
            and int(tm) < (int(ta) ** 2)
        ):
            start = True
            a = int(ta)
            m = int(tm)
            n = a**2
            startgame()
            prompt.destroy()
        else:
            ErrorLabel.configure(text="Error: Invalid values")

    Label(prompt, text="Board size:").pack()
    abox = Entry(prompt, relief="solid", width=10)
    abox.pack()
    Label(prompt, text="Mines:").pack()
    mbox = Entry(prompt, relief="solid", width=10)
    mbox.pack()
    okbutton = Button(
        prompt, text="Ok", relief="solid", borderwidth=1, command=startfnc
    )
    okbutton.pack(pady=20)
    ErrorLabel = Label(prompt, text=" ")
    ErrorLabel.pack()
    prompt.mainloop()


# Game GUI
root = Tk()
# Read Images from script path
ScriptPath = Path(__file__).parent  # get the game script path
MineImg = PhotoImage(file=ScriptPath / "resources" / "mine.gif")
FlagImg = PhotoImage(file=ScriptPath / "resources" / "flag.gif")
YouWin = PhotoImage(file=ScriptPath / "resources" / "win.gif")
YouLose = PhotoImage(file=ScriptPath / "resources" / "lose.gif")
blank = PhotoImage(file=ScriptPath / "resources" / "blue.gif")
# create window elements
root.title("Minesweeper by Amine Bouslah")
root.iconphoto(True, FlagImg)  # set window icon
f1 = Frame(root, relief="solid")
f2 = Frame(root, relief="solid")
sf = Frame(f2, width=300)
bf = Frame(f2, width=300)
OptionsButton = Button(bf, text="Options", command=popup, relief="solid", borderwidth=1)
RestartButton = Button(
    bf, text="Restart", command=startgame, relief="solid", borderwidth=1
)
f1.grid(row=0, column=0, sticky="n")
f2.grid(column=1, row=0, sticky="nw")
bf.grid(row=0, sticky="n")
sf.grid(row=1, sticky="n")
RestartButton.grid(sticky="n", padx=20, pady=30, row=0, column=0)
OptionsButton.grid(sticky="n", padx=20, pady=30, row=0, column=1)
first_time = True
startgame()
root.mainloop()
