import can
import time

startTime_ms = round(time.time()*1000)
def addToTrace(s):
    currentTime_ms = round(time.time()*1000)
    dT_ms = currentTime_ms - startTime_ms
    print("[" + str(dT_ms) + "ms] " + s)

filters = [
    {"can_id": 0x355, "can_mask": 0x7FF, "extended": False},
    {"can_id": 0x356, "can_mask": 0x7FF, "extended": False},
    {"can_id": 0x522, "can_mask": 0x7FF, "extended": False}]

canbus = can.interface.Bus(bustype='socketcan', channel="can0", can_filters = filters)

while(1):
    message = canbus.recv(0)
    if message:
        #simpbms SoC
        if message.arbitration_id == 0x355:
            soc = (message.data[1] << 8) + message.data[0]
            addToTrace("PI: Set capacity to %d" % soc)

        #simbms Voltage
        if message.arbitration_id == 0x356:
            vtg = ((message.data[1]<< 8) + message.data[0]) / 100
            addToTrace("PI: Set battery voltage to %d V" % vtg)
        #shunt Voltage
        if message.arbitration_id == 0x522:
            shuntVtg = ((message.data[2] << 24) + (message.data[3] << 16) + (message.data[4] << 8) + message.data[5]) / 1000 
            addToTrace("PI: Shunt set battery voltage to %d V" % shuntVtg)

