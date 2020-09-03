from tkinter import Frame, Label, Entry, LEFT, TOP, END
from api.wrappers import mod
from frames.abstract import PaginatedActionListFrame, AddRecordsFrame
import constants


class ModeratorAddFrame(AddRecordsFrame):
    def __init__(self, master, calling_frame):
        super().__init__(master, calling_frame, ["username"])

    def _build_add_record_frame(self, frame: Frame):
        self.__username_label = Label(frame, text="username")
        self.__username_label.pack(side=LEFT)

        self.__username_entry = Entry(frame)
        self.__username_entry.pack(side=LEFT)

    def _get_record_to_be_added(self) -> dict:
        record = {"username": self.__username_entry.get()}
        self.__username_entry.delete(0, END)
        return record

    def _confirm_changes(self, objs):
        mod.add_new_moderators([m['username'] for m in self.all])



class ModeratorListFrame(PaginatedActionListFrame):
    def __init__(self, master):
        super().__init__(master,  constants.MAX_PAGE_LENGTH_MOD,[
            "username",
            "token",
        ],  add_records_frame=ModeratorAddFrame)

    def _fetch_elements(self, page) -> list:
        return mod.get_moderators(page)

    def _remove_records(self, obj):
        mod.remove_moderators(obj)


class AdminFrame(Frame):
    def __init__(self, master, *args, **kwargs):
        Frame.__init__(self, master, *args, **kwargs)
        ModeratorListFrame(self).pack()





