from numpy import true_divide
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time


class Requester:
    def __init__(self, id, proxies, tasks, headless="True"):
        self.id = id
        self.proxies = proxies
        self.objects = {}
        if headless.lower() == "true": self.headless = True
        elif headless.lower() == "false": self.headless = False
        if self.proxies is not None:
            for proxy in proxies:
                if not proxy.used:
                    self.proxy = proxy
                    break
        self.tasks = tasks
        # Special Tasks being defined here so we can reference them when calling the Requester.performTask() function.
        self.tasks["NEXT"] = {"SPECIAL"}
        self.tasks["PREVIOUS"] = {"SPECIAL"}
        self.tasks["LAST"] = {"SPECIAL"}
        self.tasks["FIRST"] = {"SPECIAL"}
        self.tasks["REFRESH_PROXY"] = {"SPECIAL"}
        self.reloadDriver()
    def refreshProxy(self):
        '''
        Iterates through `self.proxies` to find an unused `Proxy` object, then reloads the Selenium driver
        using `self.reloadDriver()`
        '''
        if self.proxies is not None:
            for proxy in self.proxies:
                if not proxy.used:
                    self.proxy = proxy
                    self.proxy.used = True
                    break
        else: print("Requester.refreshProxy() was run without defined proxies. Continuing.")
        self.reloadDriver()
    def performTask(self, task, prevTask = ""):
        '''
        Runs a task with key `task` from `self.tasks`. Subsequent calls should
        include a `prevTask` value for compatibility with special task names:\n
        `REFRESH_PROXY` - Simply runs `self.refreshProxy()`\n
        `FIRST` - Runs the first task in `self.tasks`\n
        `NEXT` - Runs the task 1 position after the index of `prevTask` in `self.tasks`\n
        `PREVIOUS` - Runs the task 1 position before the index of `prevTask` in `self.tasks`\n
        '''
        specialTask = False
        tasks_ = list(self.tasks)
        if prevTask != "": 
            if self.proxies is not None:
                self.proxy.useCount += 1
                if self.proxy.useCount >= self.proxy.maxUseCount: self.refreshProxy()
        match task:
            case "STOP":
                print(f"Requester #{self.id} | STOP Task has been run | Origin: {prevTask}")
                self.driver.quit()
                exit()
            case "REFRESH_PROXY":
                specialTask = True
                self.refreshProxy()
            case "FIRST":
                specialTask = True
                self.performTask(tasks_[0], prevTask=prevTask)
            case "NEXT":
                specialTask = True
                self.performTask(tasks_[tasks_.index(prevTask)+1], prevTask=prevTask)
            case "PREVIOUS":
                specialTask = True
                self.performTask(tasks_[tasks_.index(prevTask)-1], prevTask=prevTask)
        if not specialTask:
            taskName = task
            print(f"Requester #{self.id} | Task: {taskName} | Origin: {prevTask}")
            task = self.tasks[task]
            type = task["TYPE"]
            match type:
                case "SELECT_FRAME":
                    Success = False
                    try:
                        frame = self.waitForElement(bywhat=task["BY"],value=task["VALUE"])
                        self.driver.switch_to(frame)
                        Success = True
                    except:
                        self.performTask(task["ERROR_FINISH"], prevTask=taskName)
                    if Success: self.performTask(task["SUCCESS_FINISH"], prevTask=taskName)
                case "FIND_WITH_FRAME":
                    Success = False
                    try:
                        frame = self.waitForElement(bywhat=task["FRAME_BY"],value=task["FRAME_VALUE"])
                        self.driver.switch_to(frame)
                        Success = True
                    except:
                        self.performTask(task["ERROR_FINISH"], prevTask=taskName)
                    if Success: 
                        Success = False
                        try:
                            self.waitForElement(bywhat=task["BY"],value=task["VALUE"])
                            Success = True
                        except:
                            self.performTask(task["ERROR_FINISH"], prevTask=taskName)
                        if Success: self.performTask(task["SUCCESS_FINISH"], prevTask=taskName)
                case "FIND":
                    Success = False
                    try:
                        self.waitForElement(bywhat=task["BY"],value=task["VALUE"])
                        Success = True
                    except:
                        self.performTask(task["ERROR_FINISH"], prevTask=taskName)
                    if Success: self.performTask(task["SUCCESS_FINISH"], prevTask=taskName)
                case "GET":
                    Success = False
                    try:
                        self.driver.get(task["URL"])
                        Success = True
                    except:
                        self.performTask(self.tasks[task["ERROR_FINISH"]], prevTask=taskName)
                    if Success: self.performTask(task["SUCCESS_FINISH"], prevTask=taskName)
                case "DELAY":
                    Success = False
                    try:
                        time.sleep(task["VALUE"])
                        Success = True
                    except:
                        self.performTask(task["ERROR_FINISH"], prevTask=taskName)
                    if Success: self.performTask(task["SUCCESS_FINISH"], prevTask=taskName)
                case "FIND_AND_CLICK":
                    Success = False
                    try:
                        self.waitForElement(bywhat=task["BY"],value=task["VALUE"]).click()
                        Success = True
                    except:
                        self.performTask(task["ERROR_FINISH"], prevTask=taskName)
                    if Success: self.performTask(task["SUCCESS_FINISH"], prevTask=taskName)
                case "FIND_ELEMENT_OUTPUT_TO_VAR":
                    Success = False
                    try: 
                        element = self.waitForElement(byWhat=task["BY"],value=task["VALUE"])
                        Success = True
                        self.objects[task["VARIABLE_NAME"]] = element
                    except Exception as e:
                        print(e)
                        self.performTask(task["ERROR_FINISH"], prevTask=taskName)
                    if Success: self.performTask(task["SUCCESS_FINISH"], prevTask=taskName)
                case "GET_ELEMENT_ATTRIBUTE":
                    Success = False
                    try: 
                        element = self.objects[task["INPUT_VARIABLE_NAME"]]
                        print(element.get_attribute(task["ATTRIBUTE"]))
                        self.objects[task["OUTPUT_VARIABLE_NAME"]] = element.get_attribute(task["ATTRIBUTE"])
                        Success = True
                    except:
                        self.performTask(task["ERROR_FINISH"], prevTask=taskName)
                    if Success: self.performTask(task["SUCCESS_FINISH"], prevTask=taskName)
                case "APPEND_VARIABLE_TO_FILE":
                    Success = False
                    try:
                        with open(task["OUTPUT_FILE_NAME"], 'a') as outputFile:
                            if task["NEWLINE"] == "TRUE": outputFile.write(f"{self.objects[task['INPUT_VARIABLE_NAME']]}\n")
                            else: outputFile.write(f"{self.objects[task['INPUT_VARIABLE_NAME']]}")
                        Success = True
                    except:
                        self.performTask(task["ERROR_FINISH"], prevTask=taskName)
                    if Success: self.performTask(task["SUCCESS_FINISH"], prevTask=taskName)
                case "SEND_KEYS": 
                    Success = False
                    try:
                        element = self.objects[task["ELEMENT"]]
                        element.clear()
                        element.send_keys(task["VALUE"])
                        element.send_keys(Keys.ENTER)
                        Success = True
                    except:
                        self.performTask(task["ERROR_FINISH"], prevTask=taskName)
                    if Success: self.performTask(task["SUCCESS_FINISH"], prevTask=taskName)
    def waitForElement(self, byWhat, value, waitTime = 10):
        '''
        This function is called whenever the Requester wants to find something.\n
        Arguments are defined in `Tasks.json`'s task definitions: \n
        `BY`: `byWhat`
        `VALUE`: `value`
        '''
        match byWhat:
            case "XPATH":
                byWhat = By.XPATH
            case "CSS_SELECTOR":
                byWhat = By.CSS_SELECTOR
            case "ID":
                byWhat = By.ID
        try:
            element = WebDriverWait(self.driver, waitTime).until(
                EC.presence_of_element_located((byWhat, value))
            )
        finally:
            return element
    def reloadDriver(self):
        '''
        Reloads the Requester's Selenium `webdriver`, updating proxy information in the process.
        '''
        options = webdriver.FirefoxOptions()
        options.headless = False
        if self.proxies is not None:
            options.set_preference("network.proxy.type", 1)
            options.set_preference("network.proxy.http",self.proxy.ip)
            options.set_preference("network.proxy.http_port",self.proxy.port)
            options.set_preference("network.proxy.https",self.proxy.ip)
            options.set_preference("network.proxy.https_port",self.proxy.port)
            options.set_preference("network.proxy.ssl",self.proxy.ip)
            options.set_preference("network.proxy.ssl_port",self.proxy.port)  
            options.set_preference("network.proxy.ftp",self.proxy.ip)
            options.set_preference("network.proxy.ftp_port",self.proxy.port)
            options.set_preference("network.proxy.socks",self.proxy.ip)
            options.set_preference("network.proxy.socks_port",self.proxy.port)
        self.options = options
        self.driver = webdriver.Firefox(options=self.options)
