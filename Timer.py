from tkinter import *
from datetime import *
from time import *
from backend import Database

database = Database("sessions.db")
class Window(object):

    def __init__(self, window):
        self.window = window
        self.window.title("Raterlabs Timer")
        self.isRunning = False
        self.timer_time = "00:00"
        self.session_duration = "00:00"
        self.description = {}
        self.description_text = ""
        self.sessioninfo = []
        self.surplus = 0
        lTimer = Label(window, text="Timer", font=('times', 20, 'bold'), fg='blue')
        lTimer.grid(row=0, column=0, rowspan=2)

        self.tTimer = Label(window, text=self.timer_time, font=('times', 20, 'bold'), fg='green')
        self.tTimer.grid(row=0, column=1, rowspan=2)

        bstart=Button(window, text="Start", command=self.start)
        bstart.grid(row=0, column=2)

        bstop=Button(window, text="Stop", command=self.stop)
        bstop.grid(row=1, column=2)

        bsubmit=Button(window, text="Submit", command=self.submit)
        bsubmit.grid(row=0, column=3)

        bclear=Button(window, text="Submit & Stop", command=self.submit_stop)
        bclear.grid(row=1, column=3)

        self.task_type = StringVar(window)
        type_choices = {'EXP', 'SxS', 'EXP PQ', 'Local', 'GSA', 'Image', 'YouTube'}
        self.task_type.set('EXP')
        task_typeMenu = OptionMenu(window, self.task_type, *type_choices)
        Label(window, text="Task Type").grid(row=2, column=0)
        task_typeMenu.grid(row=2, column=1)
        self.task_type.trace('w', self.change_tasktype)

        self.task_minutes = StringVar(window)
        self.task_seconds = StringVar(window)
        time_choices = {'00', '01', '02', '03', '04', '05', '06', '07', '08', '09',
             '10', '11', '12', '13', '14', '15'}
        sec_choices = {'00', '06', '12', '18', '24', '30', '36', '42', '48', '54'}
        self.task_minutes.set("01")
        self.task_seconds.set("00")
        task_timeMenu = OptionMenu(window, self.task_minutes, *sorted(time_choices) )
        task_secMenu = OptionMenu(window, self.task_seconds, *sorted(sec_choices) )
        Label(window, text="Task AET").grid(row=2, column=2)
        task_timeMenu.grid(row=2, column=3)
        Label(window, text = "min").grid(row=2, column=4)
        task_secMenu.grid(row=2, column=5)
        Label(window, text = "sec").grid(row=2, column=6)
        self.task_minutes.trace('w', self.change_taskduration)
        self.task_seconds.trace('w', self.change_taskduration)
        self.task_duration = self.task_minutes.get() + ":" + self.task_seconds.get()
        self.timer_time = self.task_duration

        lsessionstart = Label(window, text="Session Start")
        lsessionstart.grid(row=3, column=0)

        self.tsessionstart = Label(window, text="")
        self.tsessionstart.grid(row=3, column=1)

        lduration = Label(window, text="Duration")
        lduration.grid(row=3, column=2)

        self.tduration = Label(window, text=self.session_duration)
        self.tduration.grid(row=3, column=3)

        lsurplus=Label(window, text="Surplus")
        lsurplus.grid(row=4, column=0)

        self.tsurplus = Label(window, text="00:00")
        self.tsurplus.grid(row=4, column=1)

        learnings = Label(window, text="Earnings")
        learnings.grid(row=4, column=2)

        tearnings = Text(window, height=1, width=10)
        tearnings.grid(row=4, column=3)

        ldescription = Label(window, text="Description")
        ldescription.grid(row=5, column=0)

        self.tdescription = Label(window, text="")
        self.tdescription.grid(row=5, column=1)

        self.sessioninfo = Listbox(window, height=10, width=42)
        self.sessioninfo.grid(row=6, column=0, rowspan=10, columnspan=2)

        sb = Scrollbar(window)
        sb.grid(row=6, column=2, rowspan=10)

        self.sessioninfo.configure(yscrollcommand=sb.set)
        sb.configure(command=self.sessioninfo.yview)

        btoday=Button(window, text="Today", command=self.today)
        btoday.grid(row=6, column=3)

        bweek=Button(window, text="Week", command=self.week)
        bweek.grid(row=7, column=3)

        bperiod=Button(window, text="Period", command=self.period)
        bperiod.grid(row=8, column=3)

        bmonth=Button(window, text="Month", command=self.month)
        bmonth.grid(row=9, column=3)

        bclose=Button(window, text="Close", command=self.start)
        bclose.grid(row=10, column=3)

    def start(self):
        self.timer_run = True
        self.timer_time = self.task_duration
        self.start_time = datetime.now()
        self.current_time = self.start_time
        self.surplus_time = self.timer_time
        self.surplus = 0
        self.timer()
        self.start_session()

    def stop(self):
        self.update_db()
        self.timer_run = False

    def submit(self):
        self.update_surplus()
        self.current_time = datetime.now()
        self.save_tofile()
        self.start_time = datetime.now()
        self.update_description()

    def submit_stop(self):
        self.update_surplus()
        self.current_time = datetime.now()
        self.save_tofile()
        self.update_description()
        self.update_db()
        self.timer_run = False

    def timer(self):
        if  self.timer_run:
            time2 = self.timer_time
            next_time = datetime.now()
            delta = next_time - self.start_time
            task_time = datetime.strptime(self.task_duration, "%M:%S")
            task_sec = task_time.minute*60 + task_time.second
            time1 = timedelta(seconds=task_sec)
            surplus_delta = self.surplus - delta.total_seconds() + task_sec
            new_surplus = str( timedelta( seconds=abs(surplus_delta) ) )[:-7]
            if (surplus_delta < 0):
                new_surplus = "-" + new_surplus
            if  new_surplus != self.surplus_time:
                if surplus_delta < 0:
                    self.tsurplus.config(fg='red')
                else:
                    self.tsurplus.config(fg='green')
                self.surplus_time = new_surplus
                self.tsurplus.config(text=self.surplus_time)

            if ( delta.total_seconds() >= timedelta(seconds=task_time.minute*60 + task_time.second).total_seconds() ):
                time1 = delta - time1
                time2 = '-' + str(time1)[:-7]
                self.tTimer.config(fg='red')
            else:
                time1 = time1 - delta
                time2 = str(time1)[:-7]
                self.tTimer.config(fg='green')

            if time2 != self.timer_time:
                self.timer_time = time2
                self.tTimer.config(text=self.timer_time)
        self.tTimer.after(50, self.timer)

    def duration_timer(self):
        time1 = '00:00'
        if self.timer_run:
            next_time = datetime.now()
            delta = next_time - self.session_start
            time1 = str(delta)[:7]
        if time1 != self.session_duration:
            self.session_duration = time1
            self.tduration.config(text=self.session_duration)
        self.tduration.after(50, self.duration_timer)

    def start_session(self):

        self.tsessionstart.config( text=self.start_time.strftime("%Y-%m-%d %H:%M:%S") )
        self.session_start = self.start_time
        self.session_duration = '00:00'
        self.tduration.config( text=self.session_duration )
        self.tsurplus.config(text = self.surplus)
        self.duration_timer()

    def update_surplus(self):
        surplus_time = datetime.strptime(self.timer_time[-5:], "%M:%S")
        surplus_sec = surplus_time.minute*60 + surplus_time.second
        if self.timer_time[0] == "-":
            self.surplus -= surplus_sec
        else:
            self.surplus += surplus_sec
        print( "surplus updated " + str(self.surplus) )

    def update_db(self):
        if self.description_text != "":
            database.insert(self.session_start.strftime("%Y-%m-%d %H:%M:%S") , self.current_time.strftime("%Y-%m-%d %H:%M:%S"),
                self.description_text, self.session_duration, self.surplus )
            print("db updated")

    def update_description(self):
        task_name = self.task_type.get() + " " + self.task_duration
        if task_name in self.description:
            self.description[task_name]+=1
        else:
            self.description[task_name] = 1
        self.description_text = ""
        for key, value in self.description.items():
            self.description_text += str(value) + " " + key + ", "
        self.tdescription.config(text = self.description_text)
        print(self.description)
        self.sessioninfo.delete(0,END)
        for key, value in self.description.items():
            self.sessioninfo.insert(END, key+" "+str(value))

    def change_tasktype(self, *args):
        print(self.task_type.get())

    def change_taskduration(self, *args):
        self.task_duration = self.task_minutes.get() + ":" + self.task_seconds.get()
        #print(self.task_duration)

    def save_tofile(self):
        time = datetime.now().strftime("%H:%M:%S")
        file_name = datetime.now().strftime("%Y-%m-%d")
        backupfile = open(file_name + ".csv", "a")
        tuple = (self.start_time.strftime("%H:%M:%S") + ", " +  time + ", " +
         self.task_type.get() + ", " + self.task_duration + ", " + self.surplus_time  )
        tuple = tuple + ", " + self.session_duration
        backupfile.write(tuple + "\n")
        backupfile.close()

    def week(self):
        week_start = datetime.now() - timedelta( days=( datetime.isoweekday( datetime.now() ) % 7 ) )
        rows = database.view_since(week_start.strftime("%Y-%m-%d") + " 00:00:00")
        total = timedelta(seconds=0)
        self.sessioninfo.delete(0,END)
        for item in rows:
            row = str(item[0]) + " " + item[1] + " " + item[2][-8:] + " " + item[4] + " " + str(item[5])
            duration =  datetime.strptime(item[4], "%H:%M:%S")
            total = total + timedelta(hours=duration.hour, minutes=duration.minute, seconds=duration.second)
            self.sessioninfo.insert(END, row)
        print( "total: " + str(total) )

    def today(self):
        today = datetime.now().strftime("%Y-%m-%d") + " 00:00:00"
        rows = database.view_since(today)
        self.sessioninfo.delete(0,END)
        total = timedelta(seconds=0)
        total_surplus = 0
        for item in rows:
            row = item[1] + " " + item[2][-8:] + " " + item[4]
            duration =  datetime.strptime(item[4], "%H:%M:%S")
            total_surplus += item[5]
            total = total + timedelta(hours=duration.hour, minutes=duration.minute, seconds=duration.second)
            self.sessioninfo.insert(END, row)
        self.sessioninfo.insert(END, "total: " + str(total))
        surplus_str = str( timedelta( seconds=abs(total_surplus) ) )
        if total_surplus < 0:
            surplus_str = "-" + surplus_str
        print ( surplus_str )

    def month(self):
        month = datetime.now().strftime("%Y-%m") + "-01 00:00:00"
        rows = database.view_since(month)
        self.sessioninfo.delete(0,END)
        total = timedelta(seconds=0)
        for item in rows:
            row = item[1] + " " + item[2][-8:] + " " + item[4]
            duration =  datetime.strptime(item[4], "%H:%M:%S")
            total = total + timedelta(hours=duration.hour, minutes=duration.minute, seconds=duration.second)
            self.sessioninfo.insert(END, row)
        print( "total: " + str(total) )

    def period(self):
        today = datetime.now()
        period_start=datetime.strptime("2018-04-01", "%Y-%m-%d")
        total = timedelta(seconds=0)
        while period_start <= today <= period_start + timedelta(days=14):
            period_start = period_start + timedelta(days=14)
        rows = database.view_since(period_start)
        self.sessioninfo.delete(0,END)
        for item in rows:
            row = item[1] + " " + item[2][-8:] + " " + item[4]
            duration =  datetime.strptime(item[4], "%H:%M:%S")
            total = total + timedelta(hours=duration.hour, minutes=duration.minute, seconds=duration.second)
            self.sessioninfo.insert(END, row)
        print( "total: " + str(total) )


window=Tk()
Window(window)
window.call('wm', 'attributes', '.', '-topmost', '1')
window.mainloop()
