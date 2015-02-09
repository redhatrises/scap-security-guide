#!/usr/bin/python

class color():
    def __init__(self):
        self.head = '\033[95m'
        self.okblue = '\033[94m'
        self.okgreen = '\033[92m'
        self.warning = '\033[93m'
        self.fail = '\033[91m'
        self.endc = '\033[0m'
        self.bolden = '\033[1m'

    def header(self, msg):
        return(self.head + msg + self.endc)

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

print log.bold('\nSTIG INTEGRATION SUMMARY')
print log.bold('========================')
print log.header('TOTAL XCCDF REQUIREMENTS: ') + log.err('%s')
print log.header('TOTAL STIG REQUIREMENTS: ') + log.err('%s')
print log.header('TOTAL STIG CHECKS: ') + log.err('%s')
print log.header('TOTAL STIG FIXES: ') + log.err('%s')

print log.bold(log.info('test'))
print log.ok('ok')
print log.info('info')
print log.warn('warn')
print log.err('error')
