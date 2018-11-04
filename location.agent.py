import time
import os
import subprocess

condition = "ip_address"
effect = "N/A"
decision = "False"
reports = "N/A"

cmd = "nc -l 3001"
p = subprocess.Popen(cmd,shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)

class agent:
  def send_report(self, port, effect):
    cmd = "echo '" + "location" + "," + effect + "," + decision + "," + reports + "' | nc 192.168.56.102 " + port
    p = subprocess.Popen(cmd,shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)

  def check_location(self, data):
    data = data.replace('\n', '').replace('\r', '')
    data = data[:3]

    if (len(data) > 0 and data == "192" or data == "10."):
        decision = "False"
        effect = "local"
        print("[+] Data found to be safe")
        a.send_report("3003", effect)
    else:
        decision = "True"
        effect = "remote"
        print("[+] Data found to be malicious: " + effect)
        a.send_report("3002", effect)

while (True):
  msg = p.stdout.readline()
  data = msg.split(',') # [condition, value, decision]
  print("Recieved repprt: " + msg)

  if (data[0] == condition):
    print("[+] condition satisfied")
    reports = msg
    a = agent()
    a.check_location(data[1])
  else:
    print("[-] condition not satisfied")
    p.kill()
    p = subprocess.Popen(cmd,shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
  
  if (len(msg) == 0):
    time.sleep(1)


