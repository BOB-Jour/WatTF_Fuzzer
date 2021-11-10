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
import os
import sys
from queue import Queue

INPUT_PATH = './dir/input/'
INPUT_PATH2 = './dir/input2/'
INPUTLIST = []
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

        # initialize directories
        if os.path.isdir(CRASH_DIR) != True:
            os.mkdir(CRASH_DIR)
        for i in range(1, self.d+1):
            INPUTLIST.append(INPUT_PATH + str(i) + ".js")
            INPUTLIST2.append(INPUT_PATH2 + str(i) + ".js")

        # mutator and monitor
        self.mutator = mutator.Mutator(self.args)
        self.monitor = monitor.Monitor()

        # variables
        if len(os.listdir(SEEDDIR)) % 3 != 0:
            sys.exit("[!] Weird Seed files")
        self.SEEDCount = int(len(os.listdir(SEEDDIR))/3)
        self.itr = 1
        self.sem = threading.Semaphore(self.args.t)
        self.idx = 0
        self.q = Queue(maxsize = self.args.d * 2)

        # input initialize
        self.make_input()
        self.make_input()

        # monitor background
        monitor.BackGround()


    def make_input(self):
        DASHBOARD.seedIndex = self.itr
        
        self.mutator.Make(self.idx, self.itr)
        self.itr = (self.itr % self.SEEDCount) + 1
        self.idx = (self.idx+1)%2

        if self.itr == self.seedCount:
            DASHBOARD.seedCycle += 1
            if self.idx == 0:
                for input in INPUTLIST:
                    self.q.put(input)
            elif self.idx == 1:
                for input in INPUTLIST2:
                    self.q.put(input)


    def monitoring(self, input):
        DASHBOARD.TestcaseCount += 1
        monitor.run_and_crash_collecter(input, DASHBOARD)
        self.sem.release()


    def run(self):
        while self.q.empty() is False:
            if DASHBOARD.TestcaseCount % self.args.d == 0:
                self.make_input()
            self.sem.acquire()
            thread = threading.Thread(target = self.monitoring, args=(self.q.get(),))
            thread.start()
        
if __name__ == "__main__":
    args = arg_parse()
    watTF_fuzzer = watTF(args)
    DASHBOARD = Dashboard.Dashboard()
    # DASHBOARD.run_dashboard()
    DASHBOARD.seedTotalCount = watTF_fuzzer.SEEDCount
    watTF_fuzzer.run()