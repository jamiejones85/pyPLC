
# For serial (including USB-to-serial) interfaces:
# https://pyserial.readthedocs.io/en/latest/pyserial.html
# Install pyserial library:
#   python -m pip install pyserial
# List ports:
#   python -m serial.tools.list_ports

import serial # the pyserial
from serial.tools.list_ports import comports
from time import sleep

class hardwareInterface():
    def findSerialPort(self):
        ports = []
        self.addToTrace('Available serial ports:')
        for n, (port, desc, hwid) in enumerate(sorted(comports()), 1):
            self.addToTrace('{:2}: {:20} {!r}'.format(n, port, desc))
            ports.append(port)
        if (len(ports)<1):
            self.addToTrace("ERROR: No serial ports found. No hardware interaction possible.")
            self.ser = None
            self.isInterfaceOk = False
        else:
            self.addToTrace("ok, we take the first port, " + ports[0])
            try:
                self.ser = serial.Serial(ports[0], 19200, timeout=0)
                self.isInterfaceOk = True
            except:
                self.addToTrace("ERROR: Could not open serial port.")
                self.ser = None
                self.isInterfaceOk = False

    def addToTrace(self, s):
        self.callbackAddToTrace("[HARDWAREINTERFACE] " + s)            

    def setStateB(self):
        self.addToTrace("Setting CP line into state B.")
        self.outvalue = 0
        
    def setStateC(self):
        self.addToTrace("Setting CP line into state C.")
        self.outvalue = 1
        
    def __init__(self, callbackAddToTrace=None):
        self.callbackAddToTrace = callbackAddToTrace
        self.loopcounter = 0
        self.outvalue = 0
        self.findSerialPort()

    def close(self):
        if (self.isInterfaceOk):        
            self.ser.close()
    
    def mainfunction(self):
        self.loopcounter+=1
        if (self.isInterfaceOk):
            if (self.loopcounter>15):
                self.loopcounter=0
                # self.ser.write(b'hello world\n')
                self.ser.write(bytes("out"+str(self.outvalue)+"\n", "utf-8"))
            s = self.ser.read(100)
            if (len(s)>0):
                self.addToTrace(str(len(s)) + " bytes received: " + str(s, 'utf-8').strip())
        
def myPrintfunction(s):
    print("myprint " + s)

if __name__ == "__main__":
    print("Testing hardwareInterface...")
    hw = hardwareInterface(myPrintfunction)
    for i in range(0, 300):
        hw.mainfunction()
        if (i==100):
            hw.setStateC()
        if (i==200):
            hw.setStateB()
        if (i==250):
            hw.setStateC()
        if (i==280):
            hw.setStateB()
        sleep(0.03)
    hw.close()    
    print("finished.")