from tkinter import *

master = Tk()

listbox = Listbox(master)
listbox.pack()

def c(ev):
    print(ev.widget.curselection())
    print(ev.widget.get(ACTIVE))

listbox.bind("<ButtonRelease>", c)

listbox.insert(END, "a list entry")

for item in ["one", "two", "three", "four"]:
    listbox.insert(END, item)

mainloop()
