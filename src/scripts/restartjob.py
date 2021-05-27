import subprocess
import time
import threading
import sys, os, signal
import os.path
from os import path

def timedOut():
    print("Did not find the liberty server start success message in the alloted time...exiting")
    #sys.exit()
    os._exit(0)

def startServer():
    print ("Lets start the Liberty Server")
    subprocess.run(["/opt/ol/wlp/bin/server", "start"])
    print ("i've started the Liberty Server")

def stopServer():
    ps = subprocess.Popen(('ps', '-ef'), stdout=subprocess.PIPE)
    grep = subprocess.Popen(('grep', 'defaultServer'), stdin=ps.stdout, stdout=subprocess.PIPE)
    ps.stdout.close
    output = subprocess.Popen(('awk', '{print $2}'), stdin=grep.stdout, stdout=subprocess.PIPE)
    grep.stdout.close()
    head = subprocess.Popen(('head', '-1'), stdin=output.stdout, stdout=subprocess.PIPE)
    output.stdout.close()
    pid = head.communicate()[0]
    print("AJM: pid form call to head = ", pid)
    print("AJM: killing the server now")
    os.kill(int.from_bytes(pid.strip(), "big"), signal.SIGKILL)

def readlines_then_tail(fin, searchStr):
    print("Iterate through lines and then tail for further lines.")
    while True:
        line = fin.readline()
#        print("AJM: line -> " + line)
        if searchStr in line:
#            print("AJM: yield line -> ")
            yield line
        else:
#            print("AJM: tail line ->")
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
    subprocess.run(['ls', '-l', '/tmp/logs/'])
    print("AJM: doing a find")
    subprocess.run(['find', '/tmp/logs', '-name', '"*.*"'])
    print("AJM: done...")
    ##time.sleep(600)
    with open('/tmp/logs/messages.log', 'r') as fin:
        print("setting timer")
        timer = threading.Timer(.01, timedOut)
        timer.start()
        for line in readlines_then_tail(fin, messageID):
            print(line)
            if line.find(messageID):
                print("cancel timer")
                timer.cancel()
                print ("AJM: found it in logline? -> " + line)
                #print ("Liberty Server is started ... will now stop it")
                fin.close()
                break

def submitBatchJob():
    #hostname =os.environ['POSTGRES_HOSTNAME']
    #print(f'hostname is {hostname}')
    #subprocess.run(['/opt/ol/wlp/bin/batchManager', 'submit', '--trustSslCertificates','--batchManager=localhost:9443', '--user=bob', '--password=bobpwd', '--pollingInterval_s=2', '--applicationName=batch-bonuspayout-application', '--jobXMLName=BonusPayoutJob', '--wait'])

    # failure batch submission - need to parameterize this
	#'--jobPropertiesFile=/batchprops/forceFailureParms.txt'
    process = subprocess.Popen(['/opt/ol/wlp/bin/batchManager', 'restart', '--trustSslCertificates','--batchManager=localhost:9443', '--user=bob', '--password=bobpwd', '--jobInstanceId={}'.format(jobid), '--pollingInterval_s=2', '--wait'],
                               stderr=subprocess.PIPE, 
                               stdout=subprocess.PIPE)

    # successful batch submission - need to parameterize this
    #process = subprocess.Popen(['/opt/ol/wlp/bin/batchManager', 'submit', '--trustSslCertificates','--batchManager=localhost:9443', '--user=bob', '--password=bobpwd', '--jobPropertiesFile=/batchprops/forceFailureParms.txt', '--pollingInterval_s=2', '--applicationName=batch-bonuspayout-application', '--jobXMLName=BonusPayoutJob', '--wait'],
    #                           stderr=subprocess.PIPE, 
    #                           stdout=subprocess.PIPE)
    stdout, stderr = process.communicate()
    exit_code = process.wait()
    print(stdout, stderr, exit_code)
    return exit_code

def holdinplace():
    #keep this container alive while i try some things out
    while True:
        print(".", end = '')
        if path.exists("/tmp/.killmenow"):
            print("\nAJM: time to end this...")
            break

jobid = 0
# total arguments
n = len(sys.argv)
print("Total arguments passed:", n)
 
# Arguments passed
print("\nName of Python script:", sys.argv[0])
 
print("\nArguments passed:", end = " ")
for i in range(1, n):
    print(sys.argv[i], end = " ")

for i in range(1, n):
    jobid= int(sys.argv[i])
     
print("\n\njobid:", jobid)


#startServer()
print("AJM: sleep 30 seconds")
time.sleep(30)
searchLogForString("CWWKF0011I")
#searchLogForString("CWPKI0803A")
print("AJM: gonna restart the batch job")
rc = restartBatchJob(jobid)
print ("AJM: return code from batchJob =  ", rc)
if (rc == 35):
    print("AJM: Batch job submission completed successfully...shutting down server and exiting")
    rc = 0
    stopServer()
    # we want the script to exit with success, reflecting the batch job being successful, no need to set a rc here.
else:
    #print("AJM: Batch Job submission not successful - RC = ", rc)
#    print("AJM: shutting down server, exiting abnormally with rc! = ", rc)
    print("AJM: consider restarting job")
    stopServer()

sys.exit(rc)
