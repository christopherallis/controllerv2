import re
import time
import paramiko
import subprocess
import os

from wifi import Wifi

wifis = {}

# TODO: Maybe integrate Device with Wifi?
class Device:
    devices = {}

    def __init__(self, name, ip, username, password):
        self.name = name
        self.ip = ip
        self.username = username
        self.password = password

        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        Device.devices[name] = self
    
    #def __repr__(self):
    #    return "{'name': "+self.name+", 'ip': "+self.ip+", 'username': "+self.username+", 'password': "+self.password+"}"

    # def checkActiveConnection(self):
    #     try:
    #         t = self.ssh.get_transport()
    #         t.send_ignore()
    #         return True
    #     except Exception as e:
    #         print(self.name+" is not active... " + str(e))
    #         return False

    def connect(self):
        self.ssh.connect(self.ip,username=self.username,password=self.password)
        return self
    
    def runCommand(self, command):
        #assert self.checkActiveConnection(), "Could not run command for device " + self.name + ". Not connected."
        self.ssh.exec_command(command)

class Command:
    commands = []

    @classmethod
    def add(cls,command):
        cls.commands.append(command)

    @classmethod
    def run(cls):
        for cmd in cls.commands:
            cmd.action()

class WifiCommand(Command):
    def __init__(self, wifi):
        super().__init__()
        self.wifi = wifi

        super().add(self)
        
    def action(self):
        self.wifi.connect()

class WaitCommand(Command):
    def __init__(self, time):
        self.time = time
        super().add(self)
    
    def action(self):
        time.sleep(self.time)

class RemoteCommand(Command):
    def __init__(self, device, command):
        self.device = device
        self.command = command

        super().add(self)

    def action(self):
        self.device.connect()
        self.device.runCommand(self.command)

class SystemCommand(Command):
    def __init__(self,command):
        self.command = command

        super().add(self)
    
    def action(self):
        os.system(self.command)


def readWifiFromFile(f):
    line = f.readline()
    while line and line[0] != "#":
        if not line.isspace():
            info = re.findall(r'^(.+),(.+)$',line)[0]

            wifis[info[0]] = Wifi(info[0],info[1])

        line = f.readline()

    return line

def readDevicesFromFile(f):
    line = f.readline()
    while line and line[0] != "#":
        if not line.isspace():
            line = line.strip()
            info = re.findall(r'^([\w\s.]+),([\w\s.]+),([\w\s.]+),([\w\s.]+)$',line)[0]

            Device(info[0],info[1],info[2],info[3])

        line = f.readline()

    return line

def readCommandsFromFile(f):
    line = f.readline()
    while line and line[0] != "#":
        if not line.isspace():
            info = re.findall(r'^(.+):\s?(.+)$',line)[0]
            if info[0] == "remote":
                info2 = re.findall(r'(\w+) "(.+)"',info[1])[0]
                RemoteCommand(Device.devices[info2[0]],info2[1])
            elif info[0] == "wifi":
                assert wifis.get(info[1].strip()) != None, "Wifi Interface ["+info[1].strip()+"] does not exist."
                WifiCommand(wifis[info[1].strip()])
            elif info[0] == "wait":
                WaitCommand(int(info[1].strip()))
            elif info[0] == "exe":
                SystemCommand(info[1].strip())

        line = f.readline()

    return line


if __name__ == "__main__":
    filename = "samplefile.txt"
    f = open(filename,"r")
    if f.mode == 'r':
        
        assert f.readline() == "##autocmd\n", "Not a valid file type."
        
        line = f.readline()

        while line:
            
            if line == "#devices\n":
                line = readDevicesFromFile(f)
            elif line == "#wifi\n":
                line = readWifiFromFile(f)
            elif line == "#commands\n":
                line = readCommandsFromFile(f)
            else:
                line = f.readline()

        
        f.close()
    
    # Now run commands
    Command.run()

    

    

