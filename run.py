
from timeloop import Timeloop
from fluent import sender
import config as conf
from datetime import timedelta


if __name__ == '__main__':

    sender.setup(conf.FLUENT_TAG, host=conf.FLUENT_HOST, port=conf.FLUENT_PORT)
    import logic
