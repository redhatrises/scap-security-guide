#!/usr/bin/python

class color():
    def __init__(self):
        self.header = '\033[95m'
        self.okblue = '\033[94m'
        self.okgreen = '\033[92m'
        self.warning = '\033[93m'
        self.fail = '\033[91m'
        self.endc = '\033[0m'
        self.bolden = '\033[1m'

    def head(self, msg):
        return(self.header + msg + self.endc)

    def bold(self, msg):
        return(self.bolden + msg + self.endc)

    def ok(self, msg):
        return(self.okgreen + msg + self.endc)

    def info(self, msg):
        return(self.okblue + msg + self.endc)

    def warn(self, msg):
        return(self.warning + msg + self.endc)

    def err(self, msg):
        return(self.fail + msg + self.endc)

log = color()

r = ['M', 'R', 'Y', 'C', 'R', 'S', 'M', 'S']
g = ['E', 'R', ' ', 'H', 'I', 'T', 'A', '!']

msg = ''
for i in range(len(r)):
    msg += log.err(r[i]) + log.ok(g[i])
print msg




