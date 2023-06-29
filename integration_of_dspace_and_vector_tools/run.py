import time, os
from win32com.client import *
from win32com.client.connect import *

class IntegrateCanoe(object):
    Started = False
    Stopped = False
    ConfigPath = ""
    def __init__(self):
        app = DispatchEx('CANoe.Application')    
        app.Configuration.Modified = False
        ver = app.Version
        print('Loaded CANoe version ', 
            ver.major, '.', 
            ver.minor, '.', 
            ver.Build, '...', sep='')
        self.App = app
        self.Measurement = app.Measurement  
        self.Running = lambda : self.Measurement.Running
        self.WaitForStart = lambda: DoEventsUntil(lambda: IntegrateCanoe.Started)
        self.WaitForStop = lambda: DoEventsUntil(lambda: IntegrateCanoe.Stopped)
        WithEvents(self.App.Measurement, CanoeMeasurementEvents)

    def Load(self, cfgPath):
        cfg = os.path.dirname(os.path.realpath(__file__))
        cfg = os.path.join (cfg, cfgPath)
        print('Opening: ', cfg)
        self.ConfigPath = os.path.dirname(cfg)
        self.Configuration = self.App.Configuration
        self.App.Open(cfg)

    def Start(self): 
        if not self.Running():
            self.Measurement.Start()
            self.WaitForStart()
        

    def Stop(self):
        if self.Running():
            self.Measurement.Stop()
            self.WaitForStop()
       

class CanoeMeasurementEvents(object):
    def OnStart(self): 
        IntegrateCanoe.Started = True
        IntegrateCanoe.Stopped = False
        print("< measurement started >")
    def OnStop(self) : 
        IntegrateCanoe.Started = False
        IntegrateCanoe.Stopped = True
        print("< measurement stopped >")

def DoEvents():
    pythoncom.PumpWaitingMessages()
    time.sleep(.1)
def DoEventsUntil(cond):
    while not cond():
        DoEvents()

app = IntegrateCanoe()

app.Load(r"com_api.cfg")

app.Start()    

time.sleep(5)

app.Stop()