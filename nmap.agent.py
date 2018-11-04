import time
import os
import subprocess

condition = "location"
effect = "N/A"
decision = "False"
reports = "N/A"
globDec = "N/A"

cmd = "nc -l 3003"
p = subprocess.Popen(cmd,shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)

class agent:
  def gen_final(self, reports, pid):
    reports
    data = reports.split(',')
    tallyTrue = 0
    tallyFalse = 0
    if (data[2] == "True"):
      tallyTrue += 1
    else:
      tallyFalse += 1
    if (data[5] == "True"):
      tallyTrue += 1
    else:
      tallyFalse += 1
    if (data[8] == "True"):
      tallyTrue += 1
    else:
      tallyFalse += 1

    if (tallyTrue >= tallyFalse):
      globDec = "True"
      
    else:
      globDec = "False"
      cmd4 = "sudo kill " + pid
      p = subprocess.Popen(cmd4,shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)

  def check_process(self, reports):
    cmd2 = "pidof nmap"
    p = subprocess.Popen(cmd2,shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    msg2 = p.stdout.readline()

    p.kill()

    cmd3 = "ps -o user= -p " + msg2
    p = subprocess.Popen(cmd3,shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    msg3 = p.stdout.readline()

    print("TESTING-" + msg3.replace('\n', '').replace('\r', '') + "-")

    if (msg3.replace('\n', '').replace('\r', '') == "root"):
      decision = "False"
      effect = "admin owned"
      print("[+] Data found to be safe")
      reports = "auth" + "," + effect + "," + decision + "," + reports
      print("Final Report: " + reports)
      a.gen_final(reports)
      # make decision
    else:
      decision = "True"
      effect = "user owned"
      print("[+] Data found to be malicious")
      reports = "auth" + "," + effect + "," + decision + "," + reports
      print("Final Report: " + reports)
      a.gen_final(reports, msg2)

while (True):
  msg = p.stdout.readline()
  data = msg.split(',') # [condition, value, decision]
  print("Recieved repprt: " + msg)

  if (data[0] == condition and data[1] == "local"):
    print("[+] condition satisfied")
    a = agent()
    a.check_process(msg)
  else:
    print("[-] condition not satisfied")
    p.kill()
    p = subprocess.Popen(cmd,shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
  
  if (len(msg) == 0):
    time.sleep(1)




