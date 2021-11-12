import curses
import datetime
import threading

class Dashboard:
    def __init__(self):
        self.StartTime = datetime.datetime.now()
        self.LastCrashTime = 'None'
        self.TestcaseCount = 0
        self.DcheckCount = 0
        self.CrashCount = 0
        self.UniqueCrashCount = 0       # not yet
        self.V8pid = 0
        self.seedIndex = 0
        self.seedTotalCount = 0
        self.seedCycle = -1

    def dashboard(self):
        begin_x = 0
        begin_y = 0
        height = 30
        width = 80
        curses.initscr()
        curses.curs_set(0)
        field = curses.newwin(height, width, begin_y, begin_x)

        while(1):
            field.refresh()
            running_time = (datetime.datetime.now() - self.StartTime).seconds
            running_time = str(datetime.timedelta(seconds = running_time))
            dashboard_template = '''
############################################################
                        watTF Fuzzer
                          BOB-Jour
============================================================
  StartTime     :        %s
  RunTime       :        %s
  TestCase      :        %d
  Dcheck Failed :        %d
  Crash         :        %d
  Unique Crash  :        %d
  Latest Crash  :        %s
  V8 PID        :        %d
  Seed          :       (%d/%d)
  Seed Cycle    :        %d
############################################################''' % (self.StartTime, running_time, self.TestcaseCount, self.DcheckCount, self.CrashCount, self.UniqueCrashCount, self.LastCrashTime, self.V8pid, self.seedIndex, self.seedTotalCount, self.seedCycle)
            field.addstr(0, 0, dashboard_template)

    def run_dashboard(self):
        dashboard_thread = threading.Thread(target=self.dashboard, daemon=True).start()