from json import loads
from threading import Thread
from Requester import Requester
from Proxy import Proxy

class RequestHandler:
    def __init__(self):
        with open("Tasks.json", "r") as configFile:
            self.config = loads(configFile.read())
        self.proxyList = []
        try: self.config["Proxy_File"]
        except: self.config["Proxy_File"] = ""
        if self.config["Proxy_File"] != "":
            with open(self.config["Proxy_File"], "r") as Proxy_File:
                for proxy in Proxy_File.readlines():
                    self.proxyList.append(Proxy(proxy.replace("\n", ""), self.config["Proxy_Use_Count"]))
        else: self.proxyList = None
        self.requesterList, self.taskList = [], self.config["Tasks"]
    def start(self):
        self.threads = []
        for x in range(0, self.config["Requester_Count"]):
            self.threads.append(Thread(target=self.generateRequester,args=(x+1,)))
        for thread in self.threads: thread.start()
    def generateRequester(self, id):
        print(f"Generating Requester #{id}")
        requester = Requester(id, self.proxyList, self.taskList)
        self.requesterList.append(requester)
        requester.performTask(list(self.taskList)[0])
if __name__ == "__main__":
    rh = RequestHandler()
    rh.start()