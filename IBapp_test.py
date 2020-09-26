from tkinter import *
import tkinter as tk
from tkinter import ttk
import pickle
from tkcalendar import Calendar
from tkinter import messagebox
import os.path
from babel.dates import format_date, parse_date, get_day_names, get_month_names
from babel.numbers import *

LARGE_FONT = ("Verdana", 12)


class IBApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.wm_title(self, "Organiser")
        tk.Tk.wm_geometry(self, '600x600')

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (HomePage, ToDo, Timetable, Homework, Calendarf):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(HomePage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        lbl = tk.Label(self, text="Home Page", font=LARGE_FONT)
        lbl.pack(pady=10, padx=10)

        btntodolist = ttk.Button(self, text="To Do List",
                                 command=lambda: controller.show_frame(ToDo))
        btntodolist.pack()

        btntimetable = ttk.Button(self, text="Timetable",
                                  command=lambda: controller.show_frame(Timetable))
        btntimetable.pack()

        btnhomework = ttk.Button(self, text="Homework",
                                 command=lambda: controller.show_frame(Homework))
        btnhomework.pack()

        btntocalendar = ttk.Button(self, text="Calendar",
                                   command=lambda: controller.show_frame(Calendarf))
        btntocalendar.pack()


class ToDo(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        lbl = ttk.Label(self, text="To do List", font=LARGE_FONT)
        lbl.grid(row=0, column=0)

        exist = os.path.isfile("tasks.data")
        if exist:
            pass
        else:
            with open('tasks.data', 'wb'):
                pickle.load('[sample task]')

        if os.path.getsize('tasks.data') > 0:
            with open('tasks.data', 'rb') as f:
                unpickler = pickle.Unpickler(f)
                tasks = unpickler.load()
        else:
            tasks = []

        def update_list_box():
            clear_listbox()
            for task in tasks:
                lb_tasks.insert("end", task)

        def clear_listbox():
            lb_tasks.delete(0, "end")

        def add_task():
            task = txt_input.get()
            if task != "":
                tasks.append(task)
                update_list_box()
                update_file()
            else:
                tk.messagebox.showinfo("Information", "Please add a task in the text box to the top right before "
                                                      "you add task")
            txt_input.delete(0, "end")

        def del_task():
            task = lb_tasks.get("active")
            confirm = tk.messagebox.askyesno("Please Confirm", "Do you really want to delete this task?")
            if confirm:
                if task in tasks:
                    tasks.remove(task)
                    update_list_box()
                    update_file()
                else:
                    tk.messagebox.showinfo("Information", "Please select a task from the list before you do that!")

        def sort_asc():
            tasks.sort()
            update_list_box()

        def sort_desc():
            tasks.sort()
            tasks.reverse()
            update_list_box()

        def number_of_tasks():
            num_tasks = str(len(tasks))
            msg = ("Number of tasks: " + num_tasks)
            lbl_Display["text"] = msg

        def update_file():
            with open('tasks.data', 'wb') as filehandle:
                pickle.dump(tasks, filehandle)

        lbl_Display = ttk.Label(self, text="")
        lbl_Display.grid(row=0, column=1)

        txt_input = ttk.Entry(self, width=15)
        txt_input.grid(row=1, column=1)

        btn_add_task = ttk.Button(self, text="Add task", command=add_task)
        btn_add_task.grid(row=1, column=0)

        btn_del_task = ttk.Button(self, text="Delete Task", command=del_task)
        btn_del_task.grid(row=3, column=0)

        btn_sort_asc = ttk.Button(self, text="Sort Ascending", command=sort_asc)
        btn_sort_asc.grid(row=4, column=0)

        btn_sort_desc = ttk.Button(self, text="Sort Descending", command=sort_desc)
        btn_sort_desc.grid(row=5, column=0)

        btn_number_of_tasks = ttk.Button(self, text="Number of tasks", command=number_of_tasks)
        btn_number_of_tasks.grid(row=7, column=0)

        lb_tasks = tk.Listbox(self)
        lb_tasks.grid(row=2, column=1, rowspan=7)

        btntodolist = ttk.Button(self, text="Home Page",
                                 command=lambda: controller.show_frame(HomePage))
        btntodolist.grid(row=9, column=0)

        btntimetable = ttk.Button(self, text="Timetable",
                                  command=lambda: controller.show_frame(Timetable))
        btntimetable.grid(row=10, column=0)

        btnhomework = ttk.Button(self, text="Homework",
                                 command=lambda: controller.show_frame(Homework))
        btnhomework.grid(row=11, column=0)

        btntocalendar = ttk.Button(self, text="Calendar",
                                   command=lambda: controller.show_frame(Calendarf))
        btntocalendar.grid(row=12, column=0)

        update_list_box()


class Timetable(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        exist = os.path.isfile("timetable.data")
        if exist:
            pass
        else:
            list1 = [["sun1", "sun2", "sun3", "sun4", "sun5", "sun6", "sun7"],
                     ["mon1", "mon2", "mon3", "mon4", "mon5", "mon6", "mon7"],
                     ["tues1", "tues2", "tues3", "tues4", "tues5", "tues6", "tues7"],
                     ["wed1", "wed2", "wed3", "wed4", "wed5", "wed6", "wed7"],
                     ["thurs1", "thurs2", "thurs3", "thurs4", "thurs5", "thurs6", "thurs7"]]

            with open('timetable.data', 'wb') as filehandle:
                pickle.dump(list1, filehandle)

        with open('timetable.data', 'rb') as filehandle:
            contents = (pickle.load(filehandle))
            sun = contents[0]
            mon = contents[1]
            tues = contents[2]
            wed = contents[3]
            thurs = contents[4]
            totalrows = len(contents)
            totalcolumns = len(contents[0])

        def get_all_entry(parent_widget):
            children_widgets = parent_widget.winfo_children()
            read_sub = []
            content = [[], [], [], [], []]
            for child_widget in children_widgets:
                if child_widget.winfo_class() == 'Entry':
                    read_sub.append(child_widget.get())

            sun1 = [read_sub[0], read_sub[1], read_sub[2], read_sub[3], read_sub[4], read_sub[5], read_sub[6]]
            sun = sun1
            content[0] = sun

            mon1 = [read_sub[7], read_sub[8], read_sub[9], read_sub[10], read_sub[11], read_sub[12], read_sub[13]]
            mon = mon1
            content[1] = mon

            tues1 = [read_sub[14], read_sub[15], read_sub[16], read_sub[17], read_sub[18], read_sub[19], read_sub[20]]
            tues = tues1
            content[2] = tues

            wed1 = [read_sub[21], read_sub[22], read_sub[23], read_sub[24], read_sub[25], read_sub[26], read_sub[27]]
            wed = wed1
            content[3] = wed

            thurs1 = [read_sub[28], read_sub[29], read_sub[30], read_sub[31], read_sub[32], read_sub[33], read_sub[34]]
            thurs = thurs1
            content[4] = thurs

            with open('timetable.data', 'wb') as f:
                pickle.dump(content, f)

        for i in range(totalrows):
            for j in range(totalcolumns):
                gridlock = tk.Entry(self)
                gridlock.grid(row=i + 1, column=j)
                gridlock.insert(END, contents[i][j])
        savebtn = ttk.Button(self, text="Save",
                             command=lambda w=self: get_all_entry(w))
        savebtn.grid(row=totalrows + 1, column=2)

        lbl = ttk.Label(self, text="School Timetable")
        lbl.grid(row=0, column=2)

        btntohome = ttk.Button(self, text="Home Page", command=lambda: controller.show_frame(HomePage))
        btntohome.grid(row=8, column=2)

        btntodolist = ttk.Button(self, text="To Do List", command=lambda: controller.show_frame(ToDo))
        btntodolist.grid(row=9, column=2)

        btnhomework = ttk.Button(self, text="Homework", command=lambda: controller.show_frame(Homework))
        btnhomework.grid(row=10, column=2)

        btntocalendar = ttk.Button(self, text="Calendar",
                                   command=lambda: controller.show_frame(Calendarf))
        btntocalendar.grid(row=11, column=2)


class Calendarf(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        lbl = ttk.Label(self, text="Calendar")
        lbl.pack()

        dates = []
        events = []
        cur_d_e = []

        # check if file exists
        exist = os.path.isfile('dates_events.data')
        if exist:
            pass
        else:
            with open('dates_events.data', 'wb') as f:
                pass

        # if file is not empty, load data from file into list ^
        if os.path.getsize('dates_events.data') > 0:
            with open('dates_events.data', 'rb') as file:
                cur_d_e = pickle.load(file)

        # function to add events
        def add_events():
            top = tk.Toplevel()

            # create calendar in top window
            cal = Calendar(top, selectmode='day', year=2020, month=8)
            cal.pack(padx=10, pady=10)

            def sel_date():
                # get date from selector
                current_date = cal.get_date()
                dates.append(current_date)
                # get event from text input
                ev = txt_input.get()
                events.append(ev)

                # create new list of functions to add to lb and file and global list
                cur_d_e_f = []

                # concatenate inputs to create new list of combined events, add to function list
                cur_d = str(current_date)
                cur_e = str(ev)
                curde = (cur_d + ": " + cur_e)
                cur_d_e_f.append(curde)

                # match global list of events/dates with local function list
                for j in cur_d_e_f:
                    cur_d_e.append(j)

                update_lb()

            # button to add events
            sel_date = ttk.Button(top, text='Add Event', command=sel_date)
            sel_date.pack()

            # text input to enter event
            txt_input = tk.Entry(top, width=15)
            txt_input.pack()

        # to update list box. runs whenever program is opened to make it same as global list
        def update_lb():
            lb_events.delete(0, "end")
            for y in cur_d_e:
                lb_events.insert("end", y)

        def del_event():
            event = lb_events.get("active")
            confirm = tk.messagebox.askyesno("Please confirm", "Are you sure you want to delete this event?")
            if confirm:
                if event in cur_d_e:
                    cur_d_e.remove(event)
                    update_lb()
                else:
                    tk.messagebox.showinfo("Information",
                                           "Please select an event form the list below before doing that!")

        def save():
            with open('dates_events.data', 'wb') as filehandle:
                pickle.dump(cur_d_e, filehandle)

        ttk.Button(self, text='Add Event', command=add_events).pack(padx=10, pady=10)
        ttk.Button(self, text='Delete Event', command=del_event).pack(padx=10, pady=10)
        ttk.Button(self, text='Save', command=save).pack()

        lbl = ttk.Label(self, text="Events")
        lbl.pack()

        lb_events = tk.Listbox(self)
        lb_events.pack()
        update_lb()

        btntohome = ttk.Button(self, text="Home Page",
                               command=lambda: controller.show_frame(HomePage))
        btntohome.pack()

        btntodolist = ttk.Button(self, text="To Do List",
                                 command=lambda: controller.show_frame(ToDo))
        btntodolist.pack()

        btntotimetable = ttk.Button(self, text="Timetable",
                            command=lambda: controller.show_frame(Timetable))
        btntotimetable.pack()

        btntohomework = ttk.Button(self, text="Homework",
                                   command=lambda: controller.show_frame(Homework))
        btntohomework.pack()


class Homework(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # check if there is a file called tasks.data
        exist = os.path.isfile("homework.data")
        if exist:
            pass
        else:
            with open('homework.data', 'wb'):
                pickle.load("[sample task]")

        # make the contents of the tasks file as a list if the file is not empty
        if os.path.getsize("homework.data") > 0:
            with open('homework.data', 'rb') as f:
                unpickler = pickle.Unpickler(f)
                hw = unpickler.load()
        # if the file is empty, create an empty list called tasks
        else:
            hw = []

        # define commands for buttons
        def update_list_box():
            # clear list box before adding in any new tasks, otherwise already existing tasks are added to the box again
            clear_listbox()
            # for each task in the list, add it to the list box of all tasks
            for task in hw:
                lb_tasks.insert("end", task)

        def clear_listbox():
            lb_tasks.delete(0, "end")

        def add_task():
            # get text from text box widget
            hwTask = txt_input.get()
            # make sure that the task is not eempty
            if hwTask != "":
                # add to list of tasks
                hw.append(hwTask)
                update_list_box()
                update_file()
            # update the list box in the bottom every time the add task button is clickes:
            else:
                tk.messagebox.showinfo("Information",
                                            "Please enter a task in the text box to the top right before you add task!")
            txt_input.delete(0, "end")

        def del_all():
            confirm = tk.messagebox.askyesno("Please Confirm", "Do you really want to delete all?")
            if confirm:
                global hw
                hw = []
                update_list_box()
                update_file()

        def del_task():
            # get the text of the current selection
            task = lb_tasks.get("active")
            # confirm it is in the list
            confirm = tk.messagebox.askyesno("Please Confirm", "Do you really want to delete this task?")
            if confirm:
                if task in hw:
                    hw.remove(task)
                    update_list_box()
                    update_file()
                else:
                    tk.messagebox.showinfo("Information", "Please select a task from the list before you do that!")

        def sort_asc():
            hw.sort()
            update_list_box()

        def sort_desc():
            hw.sort()
            hw.reverse()
            update_list_box()

        def choose_random():
            hTask = random.choice(hw)
            lbl_Display["text"] = hTask

        def number_of_tasks():
            num_tasks = str(len(hw))
            msg = ("Number of tasks: " + num_tasks)
            lbl_Display["text"] = msg

        def update_file():
            with open('homework.data', 'wb') as f:
                pickle.dump(hw, f)

        # make buttons
        lbl_Title = ttk.Label(self, text="Homework")
        lbl_Title.grid(row=0, column=0)

        lbl_Display = ttk.Label(self, text="")
        lbl_Display.grid(row=0, column=1)

        txt_input = ttk.Entry(self, width=15)
        txt_input.grid(row=1, column=1)

        btn_add_task = ttk.Button(self, text="Add Homework", command=add_task)
        btn_add_task.grid(row=1, column=0)

        btn_del_all = ttk.Button(self, text="Delete All", command=del_all)
        btn_del_all.grid(row=2, column=0)

        btn_del_task = ttk.Button(self, text="Delete Homework", command=del_task)
        btn_del_task.grid(row=3, column=0)

        btn_sort_asc = ttk.Button(self, text="Sort Ascending", command=sort_asc)
        btn_sort_asc.grid(row=4, column=0)

        btn_sort_desc = ttk.Button(self, text="Sort Descending", command=sort_desc)
        btn_sort_desc.grid(row=5, column=0)

        btn_choose_random = ttk.Button(self, text="Choose Random", command=choose_random)
        btn_choose_random.grid(row=6, column=0)

        btn_number_of_tasks = ttk.Button(self, text="Number of Homework tasks", command=number_of_tasks)
        btn_number_of_tasks.grid(row=7, column=0)

        # Show all tasks
        lb_tasks = tk.Listbox(self)
        lb_tasks.grid(row=2, column=1, rowspan=7)

        # run the update listbox at least once to make sure that tasks are present when the app is opened
        update_list_box()

        # lbl = ttk.Label(self, text="Homework")
        # lbl.pack()

        btntohome = ttk.Button(self, text="Home Page",
                               command=lambda: controller.show_frame(HomePage))
        btntohome.grid(row=10, column = 1)

        btntodolist = ttk.Button(self, text="To Do List",
                                 command=lambda: controller.show_frame(ToDo))
        btntodolist.grid(row=11, column = 1)

        btntotimetable = ttk.Button(self, text="Timetable",
                            command=lambda: controller.show_frame(Timetable))
        btntotimetable.grid(row=12, column = 1)

        btntocalendar = ttk.Button(self, text="Calendar",
                                   command=lambda: controller.show_frame(Calendarf))
        btntocalendar.grid(row=13, column = 1)


app = IBApp()
app.mainloop()