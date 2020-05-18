import os
import re
import config as conf
from timeloop import Timeloop
from fluent import event, sender


tl = Timeloop()


def transform_to_dict(line) -> dict:
    regex = re.compile(r'\s+')
    regex.split(line)
    line_trasformed = regex.split(line)
    line_trasformed = list(filter(None, line_trasformed))
    matchObj = re.match(r"^[-+]?[0-9]+$", line_trasformed[0])
    tracert = {}
    if not matchObj:
        pass
    else:
        tracert['hostname'] = line_trasformed[1]
        tracert['ip'] = line_trasformed[2].strip('()')
        if line_trasformed[3] != "*":
            tracert['1st packet'] = line_trasformed[3]
        else:
            tracert['1st packet'] = 100
        try:
            if line_trasformed[5] != "*":
                tracert['2nd packet'] = line_trasformed[5]
            else:
                tracert['2nd packet'] = 100
        except IndexError:
            tracert['2nd packet'] = 100
        try:
            if line_trasformed[7] != "*":
                tracert['3rd packet'] = line_trasformed[7]
            else:
                tracert['3nd packet'] = 100
        except IndexError:
            tracert['3rd packet'] = 100
    return tracert


@tl.job(conf.SCRAPE_INTERVAL)
def trace_to_log():
    output = {}
    n = 1
    result = os.popen('traceroute '+conf.TARGET_HOST)
    for line in iter(result):
        if ("traceroute" or "Warning") in line:
            pass
        else:
            output['hop_'+str(n)] = transform_to_dict(line)
            n += 1

    sender.setup(conf.FLUENT_TAG, host=conf.FLUENT_HOST, port=conf.FLUENT_PORT)
    event.Event('follow', output)

tl.start(block=True)
