import os
import sys
import subprocess
#delays used on link
delay = [10, 50, 100]
#bandwidth combinations
ban = [5,10,15]
#packetloss combinations
ploss = [0.0]
#number of hosts (Nodes) to run
host = [5,10,15]
count = 1
for curr in range(count):
    for h in host:
        for b in ban:
           
            for d in delay:
                for p in ploss:
                    clear = 'sudo mn -c'
                    run_top_script = 'sudo python test3.py '+ str(h) + ' ' + str(b) + ' ' + str(d) + ' ' + str(p)        
                    subprocess.run(clear.split(' '))
                    print(run_top_script)
                    subprocess.run(run_top_script.split(' '))
