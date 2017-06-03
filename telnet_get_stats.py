# from telnetlib import Telnet

# with Telnet('localhost', 6023) as tn:
#   tn.interact()
#   #print(dir(tn))
#   print(tn.write(b"est()\n"))
#   #print(dir(tn))
#   #print(p(stats.get_stats()))

import sys
import getpass
import telnetlib

HOST = "localhost"
ports = ['6023']


def main():
    ports = ['6023']
    print(sys.argv)
    if len(sys.argv) > 1:
        ports = sys.argv[1].split(',')

    for port in ports:
        get_stats(port)

def get_stats(port):
    tn = telnetlib.Telnet(HOST, port)
    tn.read_until(b'>>>')
    tn.write(b"stats.get_stats()\n")
    stats = tn.read_until(b'>>>').decode()
    print(stats)
    print(type(stats))
    tn.close()

if __name__ == '__main__':
    #main()
    get_stats(ports[0])
