import os
import datetime


def successLog(pdfPath):
    logPath = os.getcwd() + "/log.txt"
    with open(logPath, "a") as logFile:
        currentTime = datetime.datetime.now()
        basename = os.path.basename(pdfPath)
        logFile.write(currentTime.strftime("%Y-%m-%d %H:%M:%S") + " " + basename + "\n")


def errorLog(pdfPath):
    logPath = os.getcwd() + "/errorLog.txt"
    with open(logPath, "a") as logFile:
        currentTime = datetime.datetime.now()
        basename = os.path.basename(pdfPath)
        logFile.write(currentTime.strftime("%Y-%m-%d %H:%M:%S") + " " + basename + "\n")
