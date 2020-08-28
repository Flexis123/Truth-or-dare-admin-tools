from frames.frames import windows, init_app
from tkinter import Tk, BOTH
from frames.activation_frame import ActivationFrame
import constants
from api.wrappers import props


class Main(Tk):
    def __init__(self, windows: dict):
        Tk.__init__(self)
        self.windows = windows

    def open_frame(self, frame):
        if frame in self.windows or frame.__class__ in self.windows:
            remove = []
            for children in self.children.values():
                ch = str(children)
                if ch != str(frame) and ch != ".!menu":
                    remove.append(children)

            for children in remove:
                children.destroy()

            if isinstance(frame, type):
                frameRef = self.windows[frame]

                args = frameRef['args'] if frameRef.get("args") is not None else ()
                kwargs = frameRef['kwargs'] if frameRef.get('kwargs') is not None else {}

                frame = frame(self, *args, **kwargs)

            try:
                frame.pack(fill=BOTH, expand=True)
            except Exception:
                frame.grid(row=0, column=0)

            frame.tkraise()


if __name__ == "__main__":
    master = Main(windows)

    conf = props.get_config()

    constants.TOKEN_HEADER = conf["mod.tokenHeader"]
    constants.USER_HEADER = conf["mod.userHeader"]
    constants.ADMIN = conf["admin.username"]
    constants.MAX_PAGE_LENGTH_MOD = int(conf["pagination.modPageLength"])
    constants.MAX_PAGES_LENGTH_TOD = int(conf["pagination.pageLength"])

    with open('token.txt') as f:
        lines = [line.strip() for line in f.readlines()]
        if len(lines) < 2:
            constants.auth_body = {constants.TOKEN_HEADER: "", constants.USER_HEADER: ""}
        else:
            constants.auth_body = {constants.TOKEN_HEADER: lines[0], constants.USER_HEADER: lines[1]}

    from api.wrappers import mod

    if not mod.login():
        master.open_frame(ActivationFrame)
    else:
        init_app(master)

    master.mainloop()



