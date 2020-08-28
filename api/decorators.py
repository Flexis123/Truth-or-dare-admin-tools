from tkinter.messagebox import showwarning
from requests import Response
from json.decoder import JSONDecodeError


def handle_not_ok_response(void=True):
    def wrapper(func):
        def inner(*args, **kwargs):
            r: Response = func(*args, **kwargs)
            if not r.ok:
                title = f"Err :{r.status_code}"
                try:
                    err = r.json()
                    showwarning(title, f"{err['error']}:{err['message']}")
                except (JSONDecodeError, KeyError):
                    showwarning(title, r.text)

                if not void:
                    return None
                else:
                    return False

            if not void:
                return r.json()
            else:
                return True

        return inner
    return wrapper

