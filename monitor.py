'''
    monitor.py
    1) run d8 
    2) collect crash 
''' 
import subprocess
import os
import datetime
import shutil
import time
import threading

#V8_PATH = './../../chromium/v8/out/asan/d8'
V8_PATH = './v8/out/asan/d8'

CRASH_DIR = "./crash_logs"

V8_PID = 0

class Monitor():
    def pkill_d8(self):
        subprocess.call('pkill -9 d8', shell=True)
        # print("[!!!!!] KILL")


    def run_and_crash_collecter(self, input, DASHBOARD):
        cmd = []
        cmd.append(V8_PATH)
        cmd.append(input)
        cmd = " ".join(cmd)
        # print(cmd)

        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True, shell=True, preexec_fn=os.setsid) 
        DASHBOARD.V8pid = p.pid
        # print("[+] V8_PID ::",  p.pid)
        
        while(p.poll() is None): 
            line = p.stderr.readline() 
            # AddressSanitizer or Dcheck Failed
            flag = False
            if b"AddressSanitizer".lower() in line.lower():
                DASHBOARD.CrashCount += 1
                flag = True
            if b"Fatal error in".lower() in line.lower():
                DASHBOARD.DcheckCount += 1
                flag = True
            if flag is True:
                DASHBOARD.LastCrashTime = datetime.datetime.now()
                now_time = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')

                # collect crash js 
                crash_js = CRASH_DIR+'/crash_'+ now_time +'_.js'
                shutil.copy2(input, crash_js) # copy metadata
                
                # collect crash log
                crash_log = CRASH_DIR+'/crash_'+ now_time +'_.log'
                with open(crash_log, 'wb') as fp:
                    fp.write(line) # first line
                    for line in p.stderr: # ... line
                        fp.write(line)             
                
                # print("[+] CRASH")

                # shutdown d8
                self.pkill_d8()

class BackGround(object):
    def __init__(self, interval=300):
        self.interval = interval
        thread = threading.Thread(target=self.restart_run, daemon = True)
        thread.start()         # Start the execution

    def restart_run(self):
        while True:
            time.sleep(self.interval)
            subprocess.call('pkill -9 d8', shell=True)
            


# if __name__ == "__main__":
#     monitor_main()

#     # make_dir()
#     # BackGround()
#     # while True:
#     #     run_and_crash_collecter()
#     #     #time.sleep(0.5)