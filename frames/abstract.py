from abc import ABC, abstractmethod
from tkinter import Frame, Button, Label, TOP, BOTTOM, Listbox, W, MULTIPLE
from typing import List, Type, Iterable
from frames.decorators import ui_confirmatiom


class ListFrame(Frame):
    def __init__(self, master, titles: List[str], max_size=None, select_mode=MULTIPLE):
        Frame.__init__(self, master)
        self._columns = {}
        self.__selected = ()
        self.__max_size = max_size if max_size is not None else -1
        self.__size = 0

        listboxes_frame = Frame(self, name="listbox_frame")
        listboxes_frame.pack(side=TOP)

        for col in range(0, len(titles)):
            title = titles[col]

            Label(listboxes_frame, text=title).grid(row=0, column=col, sticky=W)

            ls = Listbox(listboxes_frame, selectmode=select_mode, name=f"col-{col}")
            ls.grid(row=1, column=col)
            ls.bind("<ButtonRelease>", lambda x: self.__activate_rows(x))
            self._columns[title] = ls

    def add_row(self, obj):
        if self.__size <= self.max_size or self.max_size == -1:
            for title, column in self._columns.items():
                column.insert(0, obj[title])
            self.__size += 1
        else:
            raise KeyError("cant add more records")

    def remove_row(self, index):
        if self.__size <= 0:
            self.__do_for_each_row((index,), lambda col, i: col.delete(i))
            self.__size -= 1

    def clear(self):
        for column in self._columns.values():
            column.delete(0, self.max_size)
        self.__size = 0

    def __activate_rows(self, ev):
        self.__selected = ev.widget.curselection()
        self._on_row_select(self.__selected)

    def __do_for_each_row(self, indexes: Iterable, func=None):
        objs = []
        for index in indexes:
            obj = {}
            for tittle, column in self._columns.items():
                obj[tittle] = column.get(index)

                if func is not None:
                    func(column, index)
            objs.append(obj)

        return objs

    def _do_for_each_row_selected(self, func=None):
        return self.__do_for_each_row(self.__selected, func=func)

    def _on_row_select(self, selected):
        pass

    @property
    def titles(self):
        return self._columns.keys()

    @property
    def max_size(self):
        return self.__max_size

    @property
    def selected(self):
        return self._do_for_each_row_selected()[0]

    @property
    def selected_rows(self):
        return self._do_for_each_row_selected()

    @property
    def all(self):
        return self.__do_for_each_row([i for i in range(0, self.__size)])

    def __len__(self):
        return self.__size


class PaginatedListFrame(ABC, ListFrame):
    def __init__(self, master, titles: List[str], max_size=None):
        ABC.__init__(self)
        ListFrame.__init__(self, master, titles, max_size)
        self.__cur_page = -1

        paginationButtonFrame = Frame(self)
        paginationButtonFrame.pack(side=BOTTOM)

        self.pageCountLabel = Label(paginationButtonFrame, text="0")
        self.pageCountLabel.grid(row=0, column=1)

        self.nextPageBtn = Button(paginationButtonFrame, text="next", command=self.next_page)
        self.nextPageBtn.grid(row=0, column=2, columnspan=1)

        self.prevPageBtn = Button(paginationButtonFrame, text="prev", command=self.previous_page)

        self.next_page()

    def next_page(self):
        self.__cur_page += 1
        if self.__cur_page == 1:
            self.prevPageBtn.grid(row=0, column=0, columnspan=1)
        self.__display_page()

    def previous_page(self):
        if self.__cur_page != 0:
            self.__cur_page -= 1
            if self.__cur_page == 0:
                self.prevPageBtn.grid_forget()

            self.__display_page()

    def __display_page(self):
        self.clear()

        for obj in self._fetch_elements(self.__cur_page):
            self.add_row(obj)

        self.pageCountLabel['text'] = str(self.__cur_page)
        self.__selected = ()

    @property
    def current_page(self):
        return self.__cur_page

    @abstractmethod
    def _fetch_elements(self, page) -> list:
        pass


class AddRecordsFrame(ABC, ListFrame):
    def __init__(self, master, calling_frame: Type[Frame],init_fields: List[str]):
        ABC.__init__(self)
        ListFrame.__init__(self, master, init_fields)
        self.__calling_frame = calling_frame

        self.__buttonsFrame = Frame(self, name="add_record_btn_frame")
        self.__addRecordFrame = Frame(self, name="add_record_frame")

        self.__addRecordBtn = Button(self.__buttonsFrame, text="add", command=self.__add_record)
        self.__addRecordBtn.grid(row=0)

        self.__confirmBtn = Button(self.__buttonsFrame, text="confirm changes", command=self.__confirm_changes)
        self.__confirmBtn.grid(row=1)

        self._build_add_record_frame(self.__addRecordFrame)

        self.__buttonsFrame.pack(side=BOTTOM)
        self.__addRecordFrame.pack(side=BOTTOM)

    def __add_record(self):
        record = self._get_record_to_be_added()
        self.add_row(record)

    def __confirm_changes(self):
        self._confirm_changes(self.all)
        self.master.open_frame(self.__calling_frame)

    @abstractmethod
    def _build_add_record_frame(self, frame: Frame):
        pass

    @abstractmethod
    def _get_record_to_be_added(self) -> dict:
        pass

    def _confirm_changes(self, objs):
        pass


class EditRecordsFrame(PaginatedListFrame):
    def __init__(self, master, titles: List[str], max_size=None):
        super().__init__(master, titles, max_size)

        self.__edit_frame = Frame(self)
        self._build_edit_frame(self.__edit_frame)
        self.__edit_frame.pack(side=BOTTOM)

    def __on_record_click(self):
        self._on_record_click(self.selected)

    @abstractmethod
    def _build_edit_frame(self, frame: Frame):
        pass

    @abstractmethod
    def _on_record_click(self, record):
        pass


class PaginatedActionListFrame(PaginatedListFrame):
    def __init__(self, master, max_size, titles: List[str], delete_action=True,
                 add_records_frame: Type[AddRecordsFrame] = None, ):

        PaginatedListFrame.__init__(self, master, titles, max_size)

        actionButtonFrame = Frame(self)
        actionButtonFrame.pack(side=BOTTOM)

        if delete_action:
            actionButtonFrame = Frame(self)
            actionButtonFrame.pack(side=BOTTOM)

            self.removeSelectedBtn = Button(actionButtonFrame, text="remove selected", command=self.__remove_rows)
            self.removeSelectedBtn.grid(row=0, column=0)

        if add_records_frame is not None:
            self.__add_records_frame = add_records_frame
            self.addRecordsButton = Button(actionButtonFrame, text="add records",
                                           command=self.__open_add_frame)

            self.addRecordsButton.grid(row=0, column=1)

    def __open_add_frame(self):
        self.master.master.open_frame(self.add_records_frame)

    @ui_confirmatiom
    def __remove_rows(self):
        objs = self._do_for_each_row_selected(lambda col, i: col.delete(i))
        self._remove_records(objs)

    @property
    def add_records_frame(self):
        return self.__add_records_frame

    def _remove_records(self, objs: list):
        pass













