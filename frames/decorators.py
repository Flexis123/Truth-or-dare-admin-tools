from tkinter import messagebox


def ui_confirmatiom(func):
    def inner(*args, **kwargs):
        if messagebox.askyesno("Verify", "Are you sure you want to do this action?"):
            return func(*args, **kwargs)
    return inner