import serial
import os
import time
import msvcrt


def cls():
    os.system(['clear', 'cls'][os.name == 'nt'])


def connect():
    ser = serial.Serial(
        port='COM3',
        baudrate=9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=0,
        writeTimeout=0
    )

    print("connected to: " + ser.portstr)

    return ser


def startLog(ser):
    ser.write('\r')
    time.sleep(5)

    ser.write('viewLog\r')
    time.sleep(1)
    ser.write('viewLog\r')# seems to be more reliable to write viewLog twice than once


def detectPID(ser):
    print('Detecting PIDs')

    start = time.time()
    timeout = 5
    n = 0
    enable = False
    pidList = []
    while time.time() < start + timeout:
        pidLine = ser.readline()
        pid = pidLine.split(',')
        currentPid = pid[0]

        if currentPid not in pidList and enable and 'GPS' not in currentPid:
            print(currentPid)
            pidList.append(currentPid)

        if 'Starting logging mode.' in pid[0]:
            enable = True

    pidList.sort()

    return pidList


def readPID(ser, pidList):
    textarray = [' ']*len(pidList)
    lastupdate = time.time()
    while True:
        if msvcrt.kbhit():
            if msvcrt.getch() == 'q':
                break
        line = ser.readline()
        currentPid = line.split(',')

        if currentPid[0] in pidList:
            pidPosition = pidList.index(currentPid[0])
            textarray[pidPosition] = line

        if time.time() > lastupdate+0.2:
            cls()
            print '\n'.join(textarray)
            lastupdate = time.time()


def exitSerial():
    ser.write('q\r\n')
    ser.write('q\r\n')
    ser.write('q\r\n')
    ser.write('q\r\n')# just to be extra sure, I didn't test with fewer 'q's and the serial buffer flush,but this config does exit gracefully
    ser.flushInput()
    ser.close()

    print('exiting')

ser = connect()

startLog(ser)

pidList = detectPID(ser)

readPID(ser, pidList)

exitSerial()