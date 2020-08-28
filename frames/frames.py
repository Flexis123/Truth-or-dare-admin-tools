from frames.activation_frame import ActivationFrame, init_app
from frames.admin_frame import AdminFrame, ModeratorAddFrame
from frames.tod_frame import TodFrame

windows = {
    ActivationFrame: {},
    AdminFrame: {},
    ModeratorAddFrame: {
        'args': (AdminFrame,)
    },
    TodFrame: {}

}

