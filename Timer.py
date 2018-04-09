from tkinter import *
from datetime import *

class Window(object):

    def __init__(self, window):
        self.window = window
        self.window.title("Raterlabs Timer")
        self.isRunning = False
        self.timer_green = True
        self.timer_time = "00:00"
        self.description = {}
        self.sessioninfo = []

        lTimer = Label(window, text="Timer", font=('times', 20, 'bold'), fg='blue')
        lTimer.grid(row=0, column=0, rowspan=2)

        self.tTimer = Label(window, text=self.timer_time, font=('times', 20, 'bold'), fg='green')
        self.tTimer.grid(row=0, column=1, rowspan=2)

        bstart=Button(window, text="Start", command=self.start)
        bstart.grid(row=0, column=2)

        bstop=Button(window, text="Pause", command=self.stop)
        bstop.grid(row=1, column=2)

        bsubmit=Button(window, text="Submit", command=self.submit)
        bsubmit.grid(row=0, column=3)

        bclear=Button(window, text="Submit & Stop", command=self.stop)
        bclear.grid(row=1, column=3)

        self.task_type = StringVar(window)
        type_choices = {'EXP', 'SxS', 'EXP PQ', 'Local', 'GSA', 'Image'}
        self.task_type.set('EXP')
        task_typeMenu = OptionMenu(window, self.task_type, *type_choices)
        Label(window, text="Choose Task Type").grid(row=2, column=0)
        task_typeMenu.grid(row=2, column=1)
        self.task_type.trace('w', self.change_tasktype)

        self.task_duration = StringVar(window)
        time_choices = {'01:00', '01:18', '01:30', '02:00', '03:00', '03:36', '04:00',
             '04:48', '05:00', '06:00', '06:48', '07:00', '08:18', '09:00'}
        self.task_duration.set('01:00')
        task_timeMenu = OptionMenu(window, self.task_duration, *sorted(time_choices) )
        Label(window, text="Choose Task AET").grid(row=2, column=2)
        task_timeMenu.grid(row=2, column=3)
        self.task_duration.trace('w', self.change_taskduration)
        self.timer_time = self.task_duration.get()

        lsessionstart = Label(window, text="Session Start")
        lsessionstart.grid(row=3, column=0)

        self.tsessionstart = Text(window, height=1, width=20)
        self.tsessionstart.grid(row=3, column=1)

        lduration = Label(window, text="Duration")
        lduration.grid(row=3, column=2)

        self.tduration = Label(window, height=1, width=10)
        self.tduration.grid(row=3, column=3)

        lsurplus=Label(window, text="Surplus")
        lsurplus.grid(row=4, column=0)

        tsurplus = Text(window, height=1, width=10)
        tsurplus.grid(row=4, column=1)

        learnings = Label(window, text="Earnings")
        learnings.grid(row=4, column=2)

        tearnings = Text(window, height=1, width=10)
        tearnings.grid(row=4, column=3)

        ldescription = Label(window, text="Description")
        ldescription.grid(row=5, column=0)

        self.tdescription = Text(window, height=1, width=20)
        self.tdescription.grid(row=5, column=1)

        self.sessioninfo = Listbox(window, height=10, width=42)
        self.sessioninfo.grid(row=6, column=0, rowspan=10, columnspan=2)

        sb = Scrollbar(window)
        sb.grid(row=6, column=2, rowspan=10)

        self.sessioninfo.configure(yscrollcommand=sb.set)
        sb.configure(command=self.sessioninfo.yview)

        btoday=Button(window, text="Today", command=self.start)
        btoday.grid(row=6, column=3)

        bweek=Button(window, text="Week", command=self.start)
        bweek.grid(row=7, column=3)

        bperiod=Button(window, text="Period", command=self.start)
        bperiod.grid(row=8, column=3)

        bmonth=Button(window, text="Month", command=self.start)
        bmonth.grid(row=9, column=3)

        bclose=Button(window, text="Close", command=self.start)
        bclose.grid(row=10, column=3)

    def start(self):
        self.timer_run = True
        self.timer_time = self.task_duration.get()
        self.start_time = datetime.now()
        self.current_time = self.start_time
        self.timer_green = True
        self.timer()
        self.start_session()

    def stop(self):
        self.timer_run = False

    def submit(self):
        #taskchooser = Toplevel()
        #description = Label(taskchooser, text="Continue with the same AET?")
        #description.pack()

        self.start_time = datetime.now()
        self.update_description()
        self.update_db()
        self.update_surplus()

    def timer(self):
        if  self.timer_run:
            time2 = self.timer_time
            next_time = datetime.now()
            delta = next_time - self.start_time
            task_time = datetime.strptime(self.task_duration.get(), "%M:%S")
            time1 = timedelta(seconds=task_time.minute*60 + task_time.second)
            if ( delta.total_seconds() >= timedelta(seconds=task_time.minute*60 + task_time.second).total_seconds() ):
                self.timer_green = False
            else:
                self.timer_green = True
            if self.timer_green:
                time1 = time1 - delta
                time2 = str(time1)[:-7]
                self.tTimer.config(fg='green')
            else:
                time1 = delta - time1
                time2 = '-' + str(time1)[:-7]
                self.tTimer.config(fg='red')
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
        self.tsessionstart.insert(END, self.start_time.strftime("%Y-%m-%d %H:%M"))
        self.session_start = self.start_time
        self.session_duration = '00:00'
        self.tduration.config(text=self.session_duration)
        self.duration_timer()

    def update_surplus(self):
        print("surplus updated")

    def update_db(self):
        print("db updated")

    def update_description(self):
        task_name = self.task_type.get() + " " + self.task_duration.get()
        if task_name in self.description:
            self.description[task_name]+=1
        else:
            self.description[task_name] = 1
        print(self.description)
        self.sessioninfo.delete(0,END)
        for key, value in self.description.items():
            self.sessioninfo.insert(END, key+" "+str(value))

    def change_tasktype(self, *args):
        print(self.task_type.get())

    def change_taskduration(self, *args):
        print(self.task_duration.get())


window=Tk()
Window(window)
window.call('wm', 'attributes', '.', '-topmost', '1')
window.mainloop()
