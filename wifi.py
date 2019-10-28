import subprocess
import time
# This only works on windows for now, blame the fact that there isn't a maintained python wireless connection library that is cross platform


class Wifi:
    def __init__(self,ssid,password):
        self.ssid = ssid
        self.password = password
    def connect(self):
        print(subprocess.run(["netsh", "wlan", "connect", self.ssid],capture_output = True).stdout)
        time.sleep(1)
        print("Success in connecting to "+self.ssid)
        
        

    def __repr__(self):
        return "{'ssid': "+self.ssid+", 'password': "+self.password+"}"