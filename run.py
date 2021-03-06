#!/usr/bin/env python3

import os
import re
import config as conf
from timeloop import Timeloop
from fluent import event, sender
import logging
import sys


if __name__ == '__main__':
    tl = Timeloop()

    log = logging.getLogger()
    log.setLevel(level=conf.LOG_LEVEL)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        '%(asctime)s  [%(levelname)s]: %(message)s')
    handler.setFormatter(formatter)
    log.addHandler(handler)

    def transform_to_dict(line) -> dict:
        regex = re.compile(r'\s+')
        regex.split(line)
        line_trasformed = regex.split(line)
        line_trasformed = list(filter(None, line_trasformed))
        matchObj = re.match(r"^[-+]?[0-9]+$", line_trasformed[0])
        tracert = {}
        log.debug(line_trasformed)
        if not matchObj:
            log.debug(
                'String %s doesnt match with pattern and replaced with empty data' % line_trasformed)
            pass
        else:
            tracert['hostname'] = line_trasformed[1]
            tracert['ip'] = line_trasformed[2].strip('()')
            if line_trasformed[3] != "*":
                tracert['1st packet'] = line_trasformed[3]
            else:
                tracert['1st packet'] = '999'
            try:
                if line_trasformed[5] != "*":
                    tracert['2nd packet'] = line_trasformed[5]
                else:
                    tracert['2nd packet'] = '999'
            except IndexError:
                tracert['2nd packet'] = '999'
            try:
                if line_trasformed[7] != "*":
                    tracert['3rd packet'] = line_trasformed[7]
                else:
                    tracert['3nd packet'] = '999'
            except IndexError:
                tracert['3rd packet'] = '999'
        return tracert

    @tl.job(conf.SCRAPE_INTERVAL)
    def trace_to_log():
        output = {}
        n = 1
        result = os.popen('traceroute '+conf.TARGET_HOST)
        for line in iter(result):
            if ("traceroute" or "Warning") in line:
                pass
            elif conf.FILTER != '':
                if conf.FILTER in line:
                    output['hop_'+str(n)] = transform_to_dict(line)
                    n += 1
                else:
                    pass
            else:
                output['hop_'+str(n)] = transform_to_dict(line)
                n += 1

        sender.setup(conf.FLUENT_TAG, host=conf.FLUENT_HOST,
                     port=conf.FLUENT_PORT)
        subtag = conf.TARGET_HOST.replace(".", "")
        event.Event(subtag, output)
        log.info("Message %s was sent!" % output)

    tl.start(block=True)
