'''
    mutator.py
    1) seed_gen() ; 일단 X, wat 파일을 수동으로 넣어줄 계획
    2) make_input() ; mutator.py에 있는 함수를 호출하여 최종적으로 js가 생성됨
    3) monitoring() ; monitor.py에 있는 함수를 호출하여 최종적으로 ./d8 mutate.js 실행 및 크래시 수집
''' 
import Dashboard
import monitor
import mutator
import threading
import argparse
import signal
import os
import sys
import subprocess
from queue import Queue

INPUT_DIR1 = './dir/input/'
INPUT_DIR2 = './dir/input2/'
MUTATE_DIR = './dir/mutate'
DHARMA_OUTPUT_DIR = "./dir/dharma_output"
INPUTLIST1 = []
INPUTLIST2 = []
SEEDDIR = "./dir/seed/"
CRASH_DIR = "./crash_logs"

def arg_parse():
        parser = argparse.ArgumentParser(description = '[watTF description]')

        parser.add_argument('-m', required = False, type = int, default = 10, help = 'number of mutated wasm files')
        parser.add_argument('-d', required = False, type = int, default = 100, help = 'number of mutated js files')
        parser.add_argument('-t', required = False, type = int, default = 1, help = 'number of threads')

        return parser.parse_args()


class watTF():
    def __init__(self, args):
        # args
        self.args = args

        # input list
        for i in range(1, self.args.d+1):
            INPUTLIST1.append(INPUT_DIR1 + str(i) + ".js")
            INPUTLIST2.append(INPUT_DIR2 + str(i) + ".js")

        # signal
        signal.signal(signal.SIGINT, self.Exit)

        # initialize directories
        if os.path.isdir(CRASH_DIR) != True:
            os.mkdir(CRASH_DIR)
        if os.path.isdir(INPUT_DIR1) != True:
            os.mkdir(INPUT_DIR1)
        if os.path.isdir(INPUT_DIR2) != True:
            os.mkdir(INPUT_DIR2)
        if os.path.isdir(MUTATE_DIR) != True:
            os.mkdir(MUTATE_DIR)
        if os.path.isdir(DHARMA_OUTPUT_DIR) != True:
            os.mkdir(DHARMA_OUTPUT_DIR)

        # mutator and monitor
        self.mutator = mutator.Mutator(self.args)
        self.monitor = monitor.Monitor()

        # variables
        self.SEEDCount = int(len(os.listdir(SEEDDIR)))
        self.itr = 1
        self.sem = threading.Semaphore(self.args.t)
        self.idx = 0
        self.q = Queue(maxsize = self.args.d * 2)
        if(self.SEEDCount == 0):
            sys.exit('[!] There\'s no seed')

        # DASHBOARD
        self.DASHBOARD = Dashboard.Dashboard()
        self.DASHBOARD.run_dashboard()
        self.DASHBOARD.seedTotalCount = self.SEEDCount

        # input initialize
        self.make_input()

        # monitor background
        monitor.BackGround()


    def Exit(self, signum, frame):
        os.system('rm -r ' + INPUT_DIR1)
        os.system('rm -r ' + INPUT_DIR2)
        os.system('rm -r ' + MUTATE_DIR)
        os.system('rm -r ' + DHARMA_OUTPUT_DIR)
        os.system('rm ./dir/seed/exports.txt')
        subprocess.call('pkill -9 d8', shell=True)
        sys.exit('[*] watTF fuzzer is over')    


    def make_input(self):
        self.DASHBOARD.seedIndex = self.itr
        
        self.mutator.Make(self.idx, self.itr)
        self.itr = (self.itr % self.SEEDCount) + 1
        self.idx = (self.idx+1)%2

        if self.itr == self.SEEDCount:
            self.DASHBOARD.seedCycle += 1

        if self.idx == 0:
            for input in INPUTLIST1:
                self.q.put(input)
        elif self.idx == 1:
            for input in INPUTLIST2:
                self.q.put(input)
        print(self.q.qsize())


    def monitoring(self, input):
        self.DASHBOARD.TestcaseCount += 1
        self.monitor.run_and_crash_collecter(input, self.DASHBOARD)
        self.sem.release()


    def run(self):
        while self.q.empty() is False:
            if self.DASHBOARD.TestcaseCount % self.args.d == 0:
                self.make_input()
            self.sem.acquire()
            thread = threading.Thread(target=self.monitoring, args=(self.q.get(),), daemon=True)
            thread.start()
        
if __name__ == "__main__":
    args = arg_parse()
    watTF_fuzzer = watTF(args)
    watTF_fuzzer.run()