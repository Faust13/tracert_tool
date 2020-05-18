
from timeloop import Timeloop

from fluent import sender
import functions as f
import config as conf
from datetime import timedelta

tl = Timeloop()
tl.start()

if __name__ == '__main__':
    
    sender.setup(conf.FLUENT_TAG, host=conf.FLUENT_HOST, port=conf.FLUENT_PORT)

    @tl.job(timedelta(seconds=2))
    def dosomething():
        print(f.trace_to_log(conf.TARGET_HOST))
    
    
    dosomething()