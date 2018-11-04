import time
import os
import subprocess

condition = "ip_address"
effect = "N/A"
decision = "False"
reports = "N/A"

cmd = "nc -l 3002"
p = subprocess.Popen(cmd,shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)

class agent:
  def send_report(self, port):
    cmd = "echo '" + "location" + "," + effect + "," + decision + "," + reports + "' | nc 192.168.56.102 " + port
    p = subprocess.Popen(cmd,shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)

  def check_blacklist(self, data):
    with open('black.list') as f:
      for line in f:
        ipAddr = line.replace('\n', '').replace('\r', '')
        if (data.replace('\n', '').replace('\r', '') == ipAddr):
          decision = "True"
          effect = "blacklisted"
          print("[+] Data found to be malicious")
          # make decision
        else:
          decision = "False"
          effect = "whitelisted"
          print("[+] Data found to be safe")
          # make decision

while (True):
  msg = p.stdout.readline()
  data = msg.split(',') # [condition, value, decision]
  print("Recieved repprt: " + msg)

  if (data[0] == condition):
    print("[+] condition satisfied")
    print(data[1])
    a = agent()
    a.check_location(data[1])
  else:
    print("[-] condition not satisfied")
    p.kill()
    p = subprocess.Popen(cmd,shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
  
  if (len(msg) == 0):
    time.sleep(1)




