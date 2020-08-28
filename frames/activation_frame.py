from tkinter import Frame, Button, Label, Entry, W, E, N, S, Menu
from api.wrappers import mod
import constants
from frames.admin_frame import AdminFrame
from frames.tod_frame import TodFrame
from frames.decorators import ui_confirmatiom
from tkinter.messagebox import showwarning


class ActivationFrame(Frame):
    def __init__(self, master, *args, **kwargs):
        Frame.__init__(self, master, *args, *kwargs)

        self.username_label = Label(self, text="enter username: ")
        self.username_entry = Entry(self)

        self.username_label.grid(row=0, column=0)
        self.username_entry.grid(row=0, column=1)

        self.tokenLabel = Label(self, text="enter token: ")
        self.tokenEntry = Entry(self)
        self.activateBtn = Button(self, text="activate")

        self.tokenLabel.grid(row=1, column=0)
        self.tokenEntry.grid(row=1, column=1)

        self.activateBtn.grid(row=2, columnspan=2, sticky=W+E+N+S)
        self.activateBtn.bind("<Button-1>", self.__activate)

        try:
            menu = self.master.children[self.master.cget("menu").replace(".", "")]
            menu.destroy()
        except KeyError:
            pass

    def __activate(self, event):
        token = self.tokenEntry.get()
        username = self.username_entry.get()

        constants.auth_body[constants.TOKEN_HEADER] = token
        constants.auth_body[constants.USER_HEADER] = username

        if mod.login():
            with open('token.txt', 'w') as f:
                f.write(f"{token}\n{username}")
            init_app(self.master)


def init_app(master):
    menubar = Menu(master, tearoff=False)

    @ui_confirmatiom
    def log_off():
        with open('token.txt', 'w') as f:
            f.write("")
        master.open_frame(ActivationFrame)

    def open_admin_panel():
        if constants.auth_body[constants.USER_HEADER] == constants.ADMIN:
            master.open_frame(AdminFrame)
        else:
            showwarning("Acces denied", "cannnot acces admin panel as mod")

    menubar.add_command(label="Log off", command=log_off)
    menubar.add_command(label="Truth and dares", command=lambda: master.open_frame(TodFrame))
    menubar.add_command(label="Admin panel", command=open_admin_panel)

    master.config(menu=menubar)

    master.open_frame(TodFrame)








