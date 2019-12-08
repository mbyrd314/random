import requests
from bs4 import BeautifulSoup
import time

if __name__ == '__main__':
    resp = requests.get('http://10.0.0.1')
    soup = BeautifulSoup(resp.text, 'html.parser')
    rows = soup.findAll('tr')
    hostnames = []
    t = time.ctime()
    ts = t.split()
    day = ts[0]
    hour_min = ts[3]
    hour_min = hour_min.split(':')
    hour = int(hour_min[0])
    minutes = int(hour_min[1])
    idx = hour
    for row in rows:
        td = row.findAll('td')
        if len(td) > 2:
            td = td[1]
            hostnames.append(td.get_text())
    hostnames.sort()
    print('Connected Hosts: {}'.format(hostnames))
    filename = 'hosts.txt'
    with open(filename, 'r') as f:
        lines = f.readlines()
        count = 0
        if lines:
            line = lines[0]
            lines = lines[1:]
            count = int(line.split()[0])
        host_dict = {}
        for line in lines:
            ls = line.split()
            host = ls[0]
            counts = [int(x) for x in ls[1:]]
            #count = int(count)
            host_dict[host] = counts
        for hostname in hostnames:
            if hostname in host_dict:
                host_dict[hostname][idx] += 1
            else:
                host_dict[hostname] = [0]*24
                host_dict[hostname][idx] = 1
    with open(filename, 'w') as f:
        f.write('{}\n'.format(count+1))
        for host, counts in host_dict.items():
            c = [str(x) for x in counts]
            f.write('{0:30} {1}\n'.format(host, ' '.join(c)))
                
