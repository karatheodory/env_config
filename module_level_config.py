from our_config.env import IntVar


class Config:
    COUNTER = IntVar()


_config = Config()


def __getattr__(name):
    return getattr(_config, name)
