class Proxy:
    def __init__(self, ip, maxUseCount):
        self.ip = ip.split(":")[0]
        self.port = ip.split(":")[1]
        self.useCount = 0
        self.maxUseCount = maxUseCount
        self.used = False