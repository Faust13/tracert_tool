# Traceroute2Fluentd

## About

This tool just repeat `traceroute` in cycle, parse results and send it to **FluentD**.
Also, you can filter strings of `traceroute` output, if you need only specific nodes. 

## How to start

You can use [Docker-image](https://hub.docker.com/r/drf4ust/tracert2fluent) and mount your config file as volume.
Example `docker-compose.yml`:

```yaml
version: '3'

services:

  fluentd:
    build: ./build/fluentd
    container_name: fluentd
    restart: always
    volumes:
      - ./conf/fluentd:/fluentd/etc
    ports:
      - "24224:24224"

  tracert:
    image: drf4ust/tracert2fluent:latest
    container_name: tracert
    restart: always
    volumes:
      - ./conf/tracert/conf.yml:/app/conf.yml
    depends_on:
      - fluentd
 ```

## Configuration

Just create `conf.yml`:

```yaml
general:
  period: 15        # wait for x seconds and repeat traceroute
  host: ya.ru       # target host to traceroute
  log_level: info   # log level. U can set it to info/debug/warning/critical/etc
  filter: something # filter, if you need only specific nodes. If not - just delete this string

fluent: #fluentd settings
  host: localhost 
  port: 24224
  tag: tracert 
```


## Bugs and features

### Tracroute output format
If traceroute format look like:
```
...
12  172.253.51.223 (172.253.51.223)  23.430 ms
    172.253.51.239 (172.253.51.239)  22.798 ms
    172.253.51.237 (172.253.51.237)  23.714 ms
...
```
Then data what send to Fluent will look like:
```
{... 'hop_12': {'hostname': '172.253.51.237', 'ip': '172.253.51.237', '1st packet': '23.714', '2nd packet': '999', '3rd packet': '999'}, 'hop_13': {}, 'hop_14': {} ...}
```
Also, if format will be like:
```
...
6  108.170.250.83 (108.170.250.83)  15.531 ms 108.170.250.130 (108.170.250.130)  15.862 ms 108.170.250.83 (108.170.250.83)  14.189 ms
...
```
This string will be parsed wrong way.

Script works correct only with results like:

```
...
  3  aurora.yndx.net (194.226.100.90)  0.437 ms  0.438 ms  0.425 ms
  4  ya.ru (87.250.250.242)  10.831 ms  10.826 ms  10.791 ms
  ...
```
In other worlds, script works correct only if every result of traceroute match regexp:
```regexp
/^[-+]?[0-9]+ [^ ]* \([-+]?[0-9]*\.?[0-9]*\.?[0-9]*\.?[0-9]*\.?[0-9]+\) [-+]?[0-9]*\.?[0-9]+ ms [-+]?[0-9]*\.?[0-9]+ ms [-+]?[0-9]*\.?[0-9]+ ms$/
```
### If traceroute return `* * *`
If traceroute results look like 
```
13  * * *
```
or
```
6  10.222.77.29 (10.222.77.29)  9.459 ms *
```
values of `1st/2nd/3rd_packet` will be set to `999`.

## Example output

```log
2020-05-19 00:09:34,564  [INFO]: Message {'hop_1': {'hostname': '192.168.0.1', 'ip': '192.168.0.1', '1st packet': '0.008', '2nd packet': '0.007', '3rd packet': '0.004'}, 'hop_2': {'hostname': 'vds-cp43345.timeweb.ru', 'ip': '2.59.44.5', '1st packet': '0.369', '2nd packet': '0.456', '3rd packet': '0.288'}, 'hop_3': {'hostname': '*', 'ip': '*', '1st packet': '999', '2nd packet': '999', '3rd packet': '999'}, 'hop_4': {'hostname': 'aurora.yndx.net', 'ip': '194.226.100.90', '1st packet': '0.495', '2nd packet': '0.399', '3rd packet': '0.314'}, 'hop_5': {'hostname': 'ya.ru', 'ip': '87.250.250.242', '1st packet': '14.394', '2nd packet': '10.930', '3rd packet': '10.917'}} was sent!
```