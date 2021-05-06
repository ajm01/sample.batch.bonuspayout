import subprocess
import time
import threading
import sys, os

def timedOut():
    print("Did not find the liberty server start success message in the alloted time...exiting")
    #sys.exit()
    os._exit(0)

def startServer():
    print ("Lets start the Liberty Server")
    subprocess.run(["/opt/ol/wlp/bin/server", "start"])
    print ("i've started the Liberty Server")

def stopServer():
    print ("Stopping Liberty Server")
    subprocess.run(['/opt/ol/wlp/bin/server', 'stop'])

def readlines_then_tail(fin, searchStr):
    print("Iterate through lines and then tail for further lines.")
    while True:
        line = fin.readline()
        print("AJM: line -> " + line)
        if searchStr in line:
            print("AJM: yield line -> ")
            yield line
        else:
            print("AJM: tail line ->")
            tail(fin)

def tail(fin):
    print("Listen for new lines added to file.")

    while True:
        where = fin.tell()
        line = fin.readline()
        if not line:
            time.sleep(1)
            fin.seek(where)
        else:
            yield line

def searchLogForString(messageID):
    print("Searching log for messageID: " + messageID)
    with open('/logs/messages.log', 'r') as fin:
        print("setting timer")
        timer = threading.Timer(.01, timedOut)
        timer.start()
        for line in readlines_then_tail(fin, messageID):
            print(line)
            if line.find(messageID):
                print("cancel timer")
                timer.cancel()
                print ("AJM: found it in logline? -> " + line)
                print ("Liberty Server is started ... will now stop it")
                fin.close()
                break

def submitBatchJob():
    subprocess.run(['/opt/ol/wlp/bin/batchManager', 'submit', '--trustSslCertificates','--batchManager=localhost:9443', '--user=bob', '--password=bobpwd', '--pollingInterval_s=2', '--applicationName=BonusPayout', '--jobXMLName=BonusPayoutJob', '--wait'])

startServer()
searchLogForString("CWWKF0011I")
#searchLogForString("CWPKI0803A")
submitBatchJob()
stopServer()
