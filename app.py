# import the essentials
import sqlite3
import datetime
from tkinter import *
import tkinter.messagebox
from tkinter import ttk
from tkcalendar import Calendar, DateEntry
from datetime import date, timedelta, datetime
import tkinter.font as font
import webbrowser
import numpy
import time
import matplotlib.pyplot as plt
import matplotlib.dates
from PIL import Image, ImageTk
# from ttkthemes import themed_tk as tk
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import font as tkfont
from tkinter.scrolledtext import ScrolledText

# connection to database
conn = sqlite3.connect('productivity.sqlite')
cur = conn.cursor()


def CompletedActivity(user_id):
    def callback(url):
        webbrowser.open_new(url)

    def addActivityPointsForTheDay(user_id, date_, activity_points):

        cur.execute('SELECT user_id FROM USER WHERE user_id = ?', (user_id,))
        result = cur.fetchall()

        if len(result) == 0:
            print("No such user exists")

        else:
            cur.execute('SELECT date_ FROM POINTS WHERE date_ = ? AND user_id = ?', (date_, user_id))
            result = cur.fetchall()

            if len(result) == 0:
                cur.execute('INSERT INTO POINTS VALUES (?,?,?,?)', (user_id, date_, 0, activity_points))
            else:
                cur.execute(
                    'UPDATE POINTS SET activity_points = (activity_points + ?) WHERE date_ = ? AND user_id = ?',
                    (activity_points, date_, user_id))

        conn.commit()

    def addFollowUpPointsForTheDay(user_id, date_, follow_up_points):
        cur.execute('SELECT user_id FROM USER WHERE user_id = ?', (user_id,))
        result = cur.fetchall()

        if len(result) == 0:
            print("No such user exists")


        else:
            cur.execute('SELECT date_ FROM POINTS WHERE date_ = ? AND user_id = ?', (date_, user_id))
            result = cur.fetchall()

            if len(result) == 0:
                cur.execute('INSERT INTO POINTS VALUES (?,?,?,?)', (user_id, date_, follow_up_points, 0))
            else:
                cur.execute(
                    'UPDATE POINTS SET follow_up_points = (follow_up_points + ?) WHERE date_ = ? AND user_id = ?',
                    (follow_up_points, date_, user_id))

        conn.commit()

    def activity_category(passed_parameter):
        # bug in image of enter activity  V
        # inserting into book read register error in split
        # increase label size for both label and entry, external link V

        def addActivityPointsForTheDay(user_id, date_, activity_points):

            cur.execute('SELECT user_id FROM USER WHERE user_id = ?', (user_id,))
            result = cur.fetchall()

            if len(result) == 0:
                print("No such user exists")

            else:
                cur.execute('SELECT date_ FROM POINTS WHERE date_ = ? AND user_id = ?', (date_, user_id))
                result = cur.fetchall()

                if len(result) == 0:
                    cur.execute('INSERT INTO POINTS VALUES (?,?,?,?)', (user_id, date_, 0, activity_points))
                else:
                    cur.execute(
                        'UPDATE POINTS SET activity_points = (activity_points + ?) WHERE date_ = ? AND user_id = ?',
                        (activity_points, date_, user_id))

            conn.commit()

        def addFollowUpPointsForTheDay(user_id, date_, follow_up_points):

            cur.execute('SELECT user_id FROM USER WHERE user_id = ?', (user_id,))
            result = cur.fetchall()

            if len(result) == 0:
                print("No such user exists")

            else:
                cur.execute('SELECT date_ FROM POINTS WHERE date_ = ? AND user_id = ?', (date_, user_id))
                result = cur.fetchall()

                if len(result) == 0:
                    cur.execute('INSERT INTO POINTS VALUES (?,?,?,?)', (user_id, date_, follow_up_points, 0))
                else:
                    cur.execute(
                        'UPDATE POINTS SET follow_up_points = (follow_up_points + ?) WHERE date_ = ? AND user_id = ?',
                        (follow_up_points, date_, user_id))

            conn.commit()

        def clicked_ok_from_category():

            def enteractivity(userAndActiv):
                try:
                    root3 = Toplevel()
                    root3.title("Insert Activity Completed")
                    root3.geometry("1290x660")

                    global add_bg
                    original = Image.open(r'Background images\add_activity.png')
                    resized = original.resize((1290, 660), Image.ANTIALIAS)
                    add_bg = ImageTk.PhotoImage(resized)  # Keep a reference, prevent GC
                    Label(root3, image=add_bg).pack()

                    # photo3 = PhotoImage(file=r'Background images/add_activity.png')
                    # w = Label(root3, image=photo3)
                    # w.pack()

                    def doActivity(abc):
                        print(abc)
                        temp_store = abc.split(',')
                        print(temp_store)
                        # user_id,activity_id,date_,time_,repetition,external_link=""
                        user_id = int(temp_store[0])
                        activity_id = int(temp_store[1])
                        date_ = temp_store[2]
                        time_ = temp_store[3]
                        repetition = temp_store[4]
                        if activity_id <= 27:
                            external_link = temp_store[5]
                            for iter_ in range(6,len(temp_store)):
                                external_link = external_link + ',' +temp_store[iter_]
                        else:
                            external_link = ''
                        cur.execute('SELECT user_id FROM USER WHERE user_id = ?', (user_id,))
                        result = cur.fetchall()

                        if len(result) == 0:
                            print("No such user exists")

                        else:
                            cur.execute('SELECT COUNT(activity_register) FROM ACTIVITIES_DONE')
                            result = cur.fetchall()
                            activity_register = int(result[0][0]) + 1

                            date_time_completed = date_ + ' ' + time_
                            repetition = int(repetition)

                            cur.execute('SELECT points FROM LIST_OF_ACTIVITIES WHERE activity_id = ?',
                                        (activity_id,))
                            result = cur.fetchall()
                            pts_for_one_rep = int(result[0][0])
                            activity_points = pts_for_one_rep * repetition

                            cur.execute(
                                'INSERT INTO ACTIVITIES_DONE(activity_register,user_id,activity_id,date_time_completed,repetition) VALUES (?,?,?,?,?)',
                                (activity_register, user_id, activity_id, date_time_completed, repetition))
                            addActivityPointsForTheDay(user_id, date_, activity_points)

                            if external_link != '':  # add follow upp

                                if activity_id < 25:
                                    status_id = activity_id % 4
                                    if status_id == 0:
                                        status_id = 4

                                    if activity_id < 13:
                                        cur.execute(
                                            'INSERT INTO CODECHEF(activity_register,problem_tag,status_id) VALUES (?,?,?)',
                                            (activity_register, external_link, status_id))
                                    else:
                                        cur.execute(
                                            'INSERT INTO CP_WEBSITES(activity_register,problem_link,status_id) VALUES (?,?,?)',
                                            (activity_register, external_link, status_id))

                                if activity_id == 25:
                                    # 12|1-2,3,4,7-8
                                    hasError = False
                                    temparr = external_link.split('|')
                                    book_id = int(temparr[0])
                                    arr = temparr[1].split("&")
                                    cur.execute('SELECT book_id FROM BOOK WHERE book_id = ?', (book_id,))
                                    result = cur.fetchall()
                                    if len(result) == 0:
                                        hasError = True

                                    list = []
                                    for i in range(len(arr)):
                                        arr2 = arr[i].split("-")
                                        list.append(arr2)
                                        # [ [1,10], [13,15], [18] ]
                                    for i in range(len(list)):
                                        if len(list[i]) == 1:
                                            try:
                                                pg = int(list[i][0])
                                                if not hasError:
                                                    cur.execute(
                                                        'INSERT INTO BOOK_READ_REGISTER(activity_register,book_id,page_no) VALUES (?,?,?)',
                                                        (activity_register, book_id, pg))
                                            except:
                                                hasError = True

                                        elif len(list[i]) == 2:
                                            try:
                                                pgstart = int(list[i][0])
                                                pgend = int(list[i][1])
                                                if pgstart <= pgend:
                                                    for j in range(pgstart, pgend + 1):
                                                        if not hasError:
                                                            cur.execute(
                                                                'INSERT INTO BOOK_READ_REGISTER(activity_register,book_id,page_no) VALUES (?,?,?)',
                                                                (activity_register, book_id, j))
                                            except:
                                                hasError = True
                                        else:
                                            hasError = True
                                    if not hasError:
                                        date_str = date_
                                        date_object = datetime.strptime(date_str, '%Y-%m-%d').date()
                                        date_object = date_object + timedelta(days=1)
                                        date_str = date_object.strftime("%Y-%m-%d")
                                        cur.execute(
                                            'INSERT INTO FOLLOW_UP(activity_register,date_to_be_done,next_follow_up_number_id) VALUES (?,?,?)',
                                            (activity_register, date_str, 2))

                                if activity_id == 26:
                                    cur.execute('INSERT INTO ARTICLES(activity_register,article_link) VALUES (?,?)',
                                                (activity_register, external_link))
                                    date_str = date_
                                    date_object = datetime.strptime(date_str, '%Y-%m-%d').date()
                                    date_object = date_object + timedelta(days=1)
                                    date_str = date_object.strftime("%Y-%m-%d")
                                    cur.execute(
                                        'INSERT INTO FOLLOW_UP(activity_register,date_to_be_done,next_follow_up_number_id) VALUES (?,?,?)',
                                        (activity_register, date_str, 2))

                                if activity_id == 27:
                                    temparr = external_link.split('-')
                                    word = temparr[0]
                                    meaning = temparr[1]
                                    cur.execute(
                                        'INSERT INTO VOCABULARY(activity_register,word,meaning) VALUES (?,?,?)',
                                        (activity_register, word, meaning))
                                    date_str = date_
                                    date_object = datetime.strptime(date_str, '%Y-%m-%d').date()
                                    date_object = date_object + timedelta(days=1)
                                    date_str = date_object.strftime("%Y-%m-%d")
                                    cur.execute(
                                        'INSERT INTO FOLLOW_UP(activity_register,date_to_be_done,next_follow_up_number_id) VALUES (?,?,?)',
                                        (activity_register, date_str, 2))
                        conn.commit()
                        tkinter.messagebox.showinfo("Successful operation",
                                                    "Congrats, Activity entered sucessfully")
                except:
                    tkinter.messagebox.showinfo("Error occured", "Oops, sorry some error occured")

                def get_current_state():
                    answer = str(user_id) + ','
                    answer = answer + str(activity_id) + ','
                    temp_date = (cal.selection_get()).strftime("%Y-%m-%d")
                    answer = answer + temp_date + ','
                    hr = hours.get()
                    try:
                        if hr == '':
                            now = datetime.now()
                            t = now.strftime("%H:%M:%S")
                            hr = str(t[0:2])
                            min = str(t[3:5])
                        else:
                            hr = int(hr)
                            if hr < 0 or hr > 24:
                                now = datetime.now()
                                t = now.strftime("%H:%M:%S")
                                hr = str(t[0:2])
                                min = str(t[3:5])
                            elif hr < 10:
                                hr = '0' + str(hr)
                            else:
                                hr = str(hr)
                    except:
                        now = datetime.now()
                        t = now.strftime("%H:%M:%S")
                        hr = str(t[0:2])
                        min = str(t[3:5])

                    min = minutes.get()
                    try:
                        if min == '':
                            now = datetime.now()
                            t = now.strftime("%H:%M:%S")
                            hr = str(t[0:2])
                            min = str(t[3:5])
                        else:
                            min = int(min)
                            if min < 0 or min > 60:
                                now = datetime.now()
                                t = now.strftime("%H:%M:%S")
                                hr = str(t[0:2])
                                min = str(t[3:5])
                            elif min < 10:
                                min = '0' + str(min)
                            else:
                                min = str(min)
                    except:
                        now = datetime.now()
                        t = now.strftime("%H:%M:%S")
                        hr = str(t[0:2])
                        min = str(t[3:5])

                    answer = answer + hr + ':' + min + ':00,'
                    answer = answer + repetition.get() + ','
                    if activity_id <= 27:
                        answer = answer + external_link.get()
                    return answer

                helv50 = font.Font(family='Helvetica', size=50, weight=font.BOLD)

                temp_arr = userAndActiv.split(',')
                user_id = int(temp_arr[0])
                activity_id = int(temp_arr[1])

                cur.execute("SELECT activity_name FROM LIST_OF_ACTIVITIES WHERE activity_id=?", (activity_id,))
                result = cur.fetchall()
                act_name = result[0][0]
                Label(root3, text=act_name, font=helv50, bg='#d92d21', fg='gold').place(x=20, y=50)

                cal = Calendar(root3, font="Arial 14", selectmode='day', cursor="hand1")
                cal.place(x=100, y=200)
                Button(root3, text="OK", width=20, relief=RAISED, bg='slateblue4', fg='white',
                       command=lambda: doActivity(get_current_state())).place(x=600, y=415)

                Label(root3, text='Hours', width=10, font=('Helvetica', 17), bg='slateblue4', fg='gold').place(
                    x=500, y=220)
                Label(root3, text='Minutes', width=10, font=('Helvetica', 17), bg='slateblue4', fg='gold').place(
                    x=700,
                    y=220)
                Label(root3, text='Repetition', width=10, font=('Helvetica', 17), height=1, bg='purple',
                      fg='gold').place(
                    x=530, y=352)

                large_font = ('Verdana', 40)
                medium_font = ('Verdana', 20)
                repetition = Entry(root3, font=medium_font, width=6)
                repetition.place(x=675, y=350)
                repetition.insert(END, '1')

                now = datetime.now()
                t = now.strftime("%H:%M:%S")
                hr = str(t[0:2])
                min = str(t[3:5])

                EAHE = StringVar()
                EAME = StringVar()
                hours = Entry(root3, width=4, font=large_font, textvariable=EAHE)
                hours.place(x=500, y=260)
                EAHE.set(hr)
                minutes = Entry(root3, width=4, font=large_font, textvariable=EAME)
                minutes.place(x=700, y=260)
                EAME.set(min)

                if activity_id <= 27:
                    if activity_id <= 24:
                        var_label_entry = 'Problem Link'
                    if activity_id <= 12:
                        var_label_entry = 'Problem Tag'
                    if activity_id == 25:
                        var_label_entry = 'Book Id | pgno1-pgno2&pgno3'
                    if activity_id == 26:
                        var_label_entry = 'Link to Article'
                    if activity_id == 27:
                        var_label_entry = 'Word - Meaning'
                    Label(root3, text=var_label_entry, width=25, font=('Helvetica', 17), height=1, bg='purple',
                          fg='gold').place(x=100, y=520)
                    external_link = Entry(root3, font=medium_font, width=40)
                    external_link.place(x=450, y=520)

                s = ttk.Style(root3)
                s.theme_use('clam')

                root3.mainloop()

            print(passed_parameter)
            root = Toplevel()
            root.title("Completed Activity")
            root.geometry("1290x660")

            main_frame = Frame(root)
            main_frame.pack(fill=BOTH, expand=1)
            my_canvas = Canvas(main_frame)
            my_canvas.pack(side=LEFT, fill=BOTH, expand=1)

            my_scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
            my_scrollbar.pack(side=RIGHT, fill=Y)

            def _on_mousewheel(event):
                my_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

            my_canvas.bind_all("<MouseWheel>", _on_mousewheel)

            my_canvas.configure(yscrollcommand=my_scrollbar.set)
            my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))

            second_frame = Frame(my_canvas)
            my_canvas.create_window((0, 0), window=second_frame, anchor="nw")

            result = []
            resultTemp = []
            if v1.get() == 1:
                cur.execute("SELECT * FROM LIST_OF_ACTIVITIES WHERE category_id=1")
                resultTemp = cur.fetchall()
                result += resultTemp

            if v2.get() == 1:
                cur.execute("SELECT * FROM LIST_OF_ACTIVITIES WHERE category_id=2")
                resultTemp = cur.fetchall()
                result += resultTemp

            if v3.get() == 1:
                cur.execute("SELECT * FROM LIST_OF_ACTIVITIES WHERE category_id=3")
                resultTemp = cur.fetchall()
                result += resultTemp

            if v4.get() == 1:
                cur.execute("SELECT * FROM LIST_OF_ACTIVITIES WHERE category_id=4")
                resultTemp = cur.fetchall()

                result += resultTemp

            for i in range(len(result)):
                if i % 2 == 0:
                    col_value = 0
                else:
                    col_value = 3
                l1 = Label(second_frame, width=7, height=2, bg='black')
                l1.grid(row=i // 2 + 3, column=col_value)

                l2 = Label(second_frame, width=7, height=2, bg='black')
                l2.grid(row=i // 2 + 3, column=col_value + 3)

                temp_act_id = result[i][0]

                userAndActiv = str(user_id) + ',' + str(temp_act_id)
                e1 = Button(second_frame, text=result[i][2], width=27, height=2,
                            font=('Gotham Medium Interface', 20),
                            relief='sunken', activebackground="#00fa68", bg="#007836", fg="white",
                            command=lambda userAndActiv=userAndActiv: enteractivity(userAndActiv))
                e1.grid(row=i // 2 + 3, column=col_value + 1, sticky='e')

                e2 = Label(second_frame, text=result[i][3], width=5, height=2,
                           font=('Gotham Medium Interface', 20, 'bold'),
                           fg='white', bg='black')
                e2.grid(row=i // 2 + 3, column=col_value + 2, sticky='e')

            second_frame.configure(bg='black')
            my_canvas.configure(bg='black')
            root.configure(bg='black')

            root.mainloop()

        root = Toplevel()
        root.title("Activity Category")
        root.iconphoto(False, PhotoImage(file=r'Window icons\category.gif'))
        root.geometry("1290x660")
        photo = PhotoImage(file=r'Background images\activity_category.png')
        # photo3 = PhotoImage(file="login1.png")
        w = Label(root, image=photo)
        w.pack()

        ######################
        user_id = int(passed_parameter)

        helv36 = font.Font(family='Helvetica', size=36, weight=font.BOLD)
        helv50 = font.Font(family='Helvetica', size=50, weight=font.BOLD)
        titleLabel = Label(root, text="CHOOSE YOUR ACTIVITY CATEGORY", font=helv50, bg='slateblue4',
                           fg='gold').place(x=20,
                                            y=50)

        v1 = IntVar()
        v2 = IntVar()
        v3 = IntVar()
        v4 = IntVar()

        e1 = Label(root, text='COMPETITIVE PROGRAMMING', width=35, height=2,
                   font=('Gotham Medium Interface', 23, 'bold'),
                   fg='black', bg='#baae00')
        e1.place(x=250, y=150)
        e2 = Checkbutton(root, width=3, height=2, font=('Gotham Medium Interface', 20), bg='black', variable=v1,
                         onvalue=1,
                         offvalue=0)
        e2.place(x=920, y=150)
        e1 = Label(root, text='FITNESS', width=35, height=2, font=('Gotham Medium Interface', 23, 'bold'),
                   fg='black',
                   bg='#baae00')
        e1.place(x=250, y=250)
        e2 = Checkbutton(root, width=3, height=2, font=('Gotham Medium Interface', 20), bg='black', variable=v2,
                         onvalue=1,
                         offvalue=0)
        e2.place(x=920, y=250)

        e1 = Label(root, text='KNOWLEDGE', width=35, height=2, font=('Gotham Medium Interface', 23, 'bold'),
                   fg='black',
                   bg='#baae00')
        e1.place(x=250, y=350)
        e2 = Checkbutton(root, width=3, height=2, font=('Gotham Medium Interface', 20), bg='black', variable=v3,
                         onvalue=1,
                         offvalue=0)
        e2.place(x=920, y=350)
        e1 = Label(root, text='MIND', width=35, height=2, font=('Gotham Medium Interface', 23, 'bold'), fg='black',
                   bg='#baae00')
        e1.place(x=250, y=450)
        e2 = Checkbutton(root, width=3, height=2, font=('Gotham Medium Interface', 20), bg='black', variable=v4,
                         onvalue=1,
                         offvalue=0)
        e2.place(x=920, y=450)

        okay = Button(root, text='OK', width=10, height=1, font=('Gotham Medium Interface', 23, 'bold'), fg='black',
                      bg='green', command=clicked_ok_from_category).place(x=480, y=550)
        root.mainloop()

    def leaderboard():
        leaderboard_window = Toplevel()
        leaderboard_window.title('Leaderboard')
        leaderboard_window.iconphoto(False, PhotoImage(file=r'Window icons\leaderboard.GIF'))

        cur.execute(
            'SELECT *,sum(follow_up_points+activity_points) as tot FROM points GROUP BY user_id,date_ ORDER BY tot DESC;')
        rank_result = cur.fetchall()

        # Parent widget for the buttons
        leaderboard_frame = Frame(leaderboard_window)
        leaderboard_frame.pack()

        # leaderboard table headers
        def table():
            Label(leaderboard_frame, width=7).grid(row=10, column=0)

            Label(leaderboard_frame, text='USER NAME', bg='dark blue', fg='white', width=15, height=3,
                  font=('Helvetica', 15, 'bold')).grid(row=10, column=1)
            Label(leaderboard_frame, text='DATE', bg='dark blue', fg='white', width=15, height=3,
                  font=('Helvetica', 15, 'bold')).grid(row=10, column=2)
            Label(leaderboard_frame, text='FOLLOW UP POINTS', bg='dark blue', fg='white', width=25, height=3,
                  font=('Helvetica', 15, 'bold')).grid(row=10, column=3)
            Label(leaderboard_frame, text='ACTIVITY POINTS', bg='dark blue', fg='white', width=20, height=3,
                  font=('Helvetica', 15, 'bold')).grid(row=10, column=4)
            Label(leaderboard_frame, text='TOTAL POINTS', bg='dark blue', fg='white', width=15, height=3,
                  font=('Helvetica', 15, 'bold')).grid(row=10, column=5)
            Label(leaderboard_frame, width=5,
                  font=('Helvetica', 15, 'bold')).grid(row=10, column=6)

        def results():
            j = 0
            ranks = []

            for i in rank_result:
                ranks += rank_result[j]
                j += 1
            how_many = len(ranks) // 5
            if ranks:
                table()
            y_value = 11
            cur.execute('SELECT user_name from USER,points WHERE user.user_id=points.user_id')
            name_list = cur.fetchall()

            names = []
            j = 0
            for i in name_list:
                names += name_list[j]
                j += 1

            print(ranks)
            j = 0
            no_of_iterations = min(len(ranks), 50)

            # yesterday=(datetime.now()-timedelta(days=1)).strftime("%Y-%m-%d")
            # has_yesterday = False
            # today=datetime.now().strftime("%Y-%m-%d")
            # has_today=False

            for i in range(0, no_of_iterations, 5):
                fg_var = 'black'
                bg_var = 'white'
                if i == 0:
                    fg_var = 'black'
                    bg_var = '#FFD700'
                if i == 5:
                    fg_var = 'black'
                    bg_var = 'silver'
                if i == 10:
                    fg_var = 'white'
                    bg_var = '#cd7f32'

                Label(leaderboard_frame, text=names[j], bg=bg_var, fg=fg_var, width=15, height=2,
                      font=('Helvetica', 15, 'bold')).grid(row=y_value, column=1)

                Label(leaderboard_frame, text=ranks[i + 1], bg=bg_var, fg=fg_var, width=15, height=2,
                      font=('Helvetica', 15, 'bold')).grid(row=y_value, column=2)

                Label(leaderboard_frame, text=ranks[i + 2], bg=bg_var, fg=fg_var, width=25, height=2,
                      font=('Helvetica', 15, 'bold')).grid(row=y_value, column=3)

                Label(leaderboard_frame, text=ranks[i + 3], bg=bg_var, fg=fg_var, width=20, height=2,
                      font=('Helvetica', 15, 'bold')).grid(row=y_value, column=4)

                Label(leaderboard_frame, text=ranks[i + 4], bg=bg_var, fg=fg_var, width=15, height=2,
                      font=('Helvetica', 15, 'bold')).grid(
                    row=y_value, column=5)

                y_value += 1
                j += 1

        table()
        results()

        root.columnconfigure(0, weight=1)
        root.rowconfigure(1, weight=1)

        root.mainloop()

    def codechef():
        root = Toplevel()
        root.title("Codechef problems")
        root.geometry("1290x660")
        root.iconphoto(False, PhotoImage(file=r'Window icons\codechef.GIF'))

        main_frame = Frame(root)
        main_frame.pack(fill=BOTH, expand=1)
        my_canvas = Canvas(main_frame)
        my_canvas.pack(side=LEFT, fill=BOTH, expand=1)

        my_scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
        my_scrollbar.pack(side=RIGHT, fill=Y)

        def _on_mousewheel(event):
            my_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        my_canvas.bind_all("<MouseWheel>", _on_mousewheel)

        my_canvas.configure(yscrollcommand=my_scrollbar.set)
        my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))

        second_frame = Frame(my_canvas)
        my_canvas.create_window((0, 0), window=second_frame, anchor="nw")

        cur.execute(
            'SELECT c.problem_tag, s.status,min(c.status_id) FROM CODECHEF c,STATUS s WHERE c.status_id = s.status_id AND activity_register IN (SELECT activity_register FROM ACTIVITIES_DONE WHERE user_id = (?)) GROUP BY c.problem_tag order by c.status_id;',
            (user_id,))
        result = cur.fetchall()
        print(result)
        problem_list = []
        for i in result:
            problem_list.append(i[0])
        print(problem_list)

        cur.execute(
            '''SELECT count(*),s.status FROM CODECHEF c,STATUS s WHERE s.status_id=c.status_id AND activity_register IN (SELECT activity_register
            FROM ACTIVITIES_DONE WHERE user_id = ?) GROUP BY c.status_id;''',
            (user_id,))

        result2 = cur.fetchall()
        print(result2)
        status = []
        counts = []
        for i in result2:
            counts.append(i[0])
            status.append(i[1])
        print(counts)

        def graph1():

            fig = plt.figure()
            ax = plt.subplot()

            col_val = []
            for val in status:
                if val == 'AC':
                    col_val.append('green')
                elif val == 'PA':
                    col_val.append('#51e800')
                elif val == 'TLE':
                    col_val.append('#e38c00')
                else:
                    col_val.append('#ff0000')

            bars = plt.bar(status, counts, width=0.4, color=col_val)

            annot = ax.annotate("", xy=(0, 0), xytext=(-20, 20), textcoords="offset points",
                                bbox=dict(boxstyle="round", fc="black", ec="b", lw=2),
                                arrowprops=dict(arrowstyle="->"))
            annot.set_visible(False)

            def update_annot(bar):
                x = bar.get_x() + bar.get_width() / 2.
                y = bar.get_y() + bar.get_height()
                annot.xy = (x, y)
                text = "{:.2g}".format(y)
                annot.set_text(text)
                annot.get_bbox_patch().set_alpha(0.4)

            def hover(event):
                vis = annot.get_visible()
                if event.inaxes == ax:
                    for bar in bars:
                        cont, ind = bar.contains(event)
                        if cont:
                            update_annot(bar)
                            annot.set_visible(True)
                            fig.canvas.draw_idle()
                            return
                if vis:
                    annot.set_visible(False)
                    fig.canvas.draw_idle()

            fig.canvas.mpl_connect("motion_notify_event", hover)

            plt.show()

        if problem_list:
            Button(second_frame,text='Show graph',command=graph1,width=30,height=2,bg='light blue',fg='black',font=('Helvetica',15,'bold')).grid(row=0,column=0,columnspan=7,pady=10,padx=10)
            for i, problem in enumerate(problem_list):
                if i % 2 == 0:
                    col_value = 0
                else:
                    col_value = 3

                if result[i][2] == 1:
                    status_bg = 'green'
                    status_fg = 'white'
                if result[i][2] == 2:
                    status_bg = '#51e800'
                    status_fg = 'white'
                if result[i][2] == 3:
                    status_bg = '#e38c00'
                    status_fg = 'white'
                if result[i][2] == 4:
                    status_bg = '#ff0000'
                    status_fg = 'white'

                l1 = Label(second_frame, width=7, height=2, bg='#0f52ba')
                l1.grid(row=i // 2 + 4, column=col_value)

                l2 = Label(second_frame, width=7, height=2, bg='#0f52ba')
                l2.grid(row=i // 2 + 4, column=col_value + 3)

                e1 = Label(second_frame, text=result[i][0], width=27, height=2,
                           font=('Gotham Medium Interface', 20, 'bold'),
                           relief='sunken', activebackground="#00fa68", bg=status_bg, fg='white', cursor='hand2')
                e1.grid(row=i // 2 + 4, column=col_value + 1, sticky='e')

                f = font.Font(e1, e1.cget("font"))
                f.configure(underline=True)
                e1.configure(font=f)
                # e1.grid(row=i, column=col_value)
                url = 'https://www.codechef.com/problems/' + problem_list[i]
                e1.bind('<Button-1>', lambda e, url=url: callback(url))

                e2 = Label(second_frame, text=result[i][1], width=5, height=2,
                           font=('Gotham Medium Interface', 20, 'bold'),
                           fg='white', bg='#0f52ba')
                e2.grid(row=i // 2 + 4, column=col_value + 2, sticky='e')

            # Label(second_frame, text='You have not done any codechef problems :(', width=5, height=2,
            # font=('Gotham Medium Interface', 25, 'bold'), fg='white', bg='#0f52ba').grid(row=0,column=0,rowspan=2,columnspan=10)
        else:
            Label(second_frame,text='You have not done any codechef problems',font=('Helvetica',30), bg='#0f52ba').grid(row=0,column=0,sticky='n',padx=120,pady=300)



        second_frame.configure(bg='#0f52ba')
        my_canvas.configure(bg='#0f52ba')
        main_frame.configure(bg='#0f52ba')
        root.configure(bg='#0f52ba')

        root.mainloop()

    def cp():
        root = Toplevel()
        root.title("Status of CP Problems")
        root.geometry("1290x660")
        root.iconphoto(False, PhotoImage(file=r'Window icons\cp.GIF'))
        root.geometry("1290x660")

        main_frame = Frame(root)
        main_frame.pack(fill=BOTH, expand=1)
        my_canvas = Canvas(main_frame)
        my_canvas.pack(side=LEFT, fill=BOTH, expand=1)

        my_scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
        my_scrollbar.pack(side=RIGHT, fill=Y)

        def _on_mousewheel(event):
            my_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        my_canvas.bind_all("<MouseWheel>", _on_mousewheel)

        my_canvas.configure(yscrollcommand=my_scrollbar.set)
        my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))

        second_frame = Frame(my_canvas)
        my_canvas.create_window((0, 0), window=second_frame, anchor="nw")

        ##########################
        # user_id = 1
        cur.execute(
            'SELECT c.problem_link, s.status,min(c.status_id) FROM CP_WEBSITES c,STATUS s WHERE c.status_id = s.status_id AND activity_register IN (SELECT activity_register FROM ACTIVITIES_DONE WHERE user_id = (?)) GROUP BY c.problem_link order by c.status_id;',
            (user_id,))
        result = cur.fetchall()
        cp_url = []
        for i in result:
            cp_url.append(i[0])

        if cp_url:

            for i, url in enumerate(cp_url):
                col_value = 0

                if result[i][2] == 1:
                    status_bg = 'green'
                    status_fg = 'white'
                if result[i][2] == 2:
                    status_bg = '#51e800'
                    status_fg = 'white'
                if result[i][2] == 3:
                    status_bg = '#e38c00'
                    status_fg = 'white'
                if result[i][2] == 4:
                    status_bg = '#ff0000'
                    status_fg = 'white'

                l2 = Label(second_frame, width=7, height=2, bg='#4d00a6')
                l2.grid(row=i, column=col_value + 3)

                e1 = Label(second_frame, text=result[i][0], width=67, height=2,
                           font=('Gotham Medium Interface', 20, 'bold'),
                           relief='sunken', activebackground="#00fa68", bg=status_bg, fg="white", cursor="hand2")
                e1.grid(row=i, column=col_value + 1, sticky='e')

                e2 = Label(second_frame, text=result[i][1], width=5, height=2,
                           font=('Gotham Medium Interface', 20, 'bold'),
                           fg='white', bg='#4d00a6')
                e2.grid(row=i, column=col_value + 2, sticky='e')

                e1.bind('<Button-1>', lambda e, url=url: callback(url))

                f = font.Font(e1, e1.cget("font"))
                f.configure(underline=True)
                e1.configure(font=f)

        else:
            Label(second_frame,text='You have not done any CP problems',font=('Helvetica',30)).grid(row=0,column=0,sticky='n',padx=120,pady=300)




        second_frame.configure(bg='#4d00a6')

        root.mainloop()

    def articles():
        root = Toplevel()
        root.title("Articles read")
        root.geometry("1290x660")
        root.iconphoto(False, PhotoImage(file=r'Window icons\article.GIF'))

        main_frame = Frame(root)
        main_frame.pack(fill=BOTH, expand=1)
        my_canvas = Canvas(main_frame)
        my_canvas.pack(side=LEFT, fill=BOTH, expand=1)

        my_scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
        my_scrollbar.pack(side=RIGHT, fill=Y)

        def _on_mousewheel(event):
            my_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        my_canvas.bind_all("<MouseWheel>", _on_mousewheel)

        my_canvas.configure(yscrollcommand=my_scrollbar.set)
        my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))

        second_frame = Frame(my_canvas)
        my_canvas.create_window((0, 0), window=second_frame, anchor="nw")

        ##########################
        # user_id = 1
        cur.execute(
            'SELECT article_link from ARTICLES WHERE activity_register IN (SELECT activity_register FROM ACTIVITIES_DONE WHERE user_id = (?));',
            (user_id,))
        result = cur.fetchall()
        print(result)

        def on_enter(e):
            # e1['underline']=True
            f = font.Font(e1, e1.cget("font"))
            f.configure(underline=True)
            e1.configure(font=f)

        def on_leave(e):
            # e1['underline']=False
            f = font.Font(e1, e1.cget("font"))
            f.configure(underline=False)
            e1.configure(font=f)

        url_list = []
        for i in result:
            url_list.append(i[0])

        Label(second_frame, text='Links to Articles', width=75, height=2,
              font=('Gotham Medium Interface', 20, 'bold'),
              relief='sunken', activebackground="#00fa68", bg='#40514e', fg="#0041e6").grid(row=0, column=0)
        col_value = 0
        for i, url in enumerate(url_list):
            e1 = Label(second_frame, text=url, width=75, height=2, font=('Gotham Medium Interface', 20, 'bold'),
                       relief='sunken', activebackground="#00fa68", bg='#40514e', fg="#49beb7", cursor="hand2")
            f = font.Font(e1, e1.cget("font"))
            f.configure(underline=True)
            e1.configure(font=f)
            e1.grid(row=i + 1, column=col_value)
            e1.bind('<Button-1>', lambda e, url=url: callback(url))
            e1.bind('<Enter>', lambda e: on_enter(e))
            e1.bind('<Leave>', lambda e: on_leave(e))

            # f = font.Font(e1, e1.cget("font"))
            # f.configure(underline=True)
            # e1.configure(font=f)

            # e1.bind('<Enter>',on_enter)
            # e1.bind('<Leave>',on_leave)

        second_frame.configure(bg='black')

        root.mainloop()

    def words():
        root = Toplevel()
        root.title("Your words")
        # w, h = root.winfo_screenwidth(), root.winfo_screenheight()
        # root.geometry("%dx%d+0+0" % (w, h))
        root.state('zoomed')

        main_frame = Frame(root)
        main_frame.pack(fill=BOTH, expand=1)
        my_canvas = Canvas(main_frame)
        my_canvas.pack(side=LEFT, fill=BOTH, expand=1)

        my_scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
        my_scrollbar.pack(side=RIGHT, fill=Y)

        def _on_mousewheel(event):
            my_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        my_canvas.bind_all("<MouseWheel>", _on_mousewheel)

        my_canvas.configure(yscrollcommand=my_scrollbar.set)
        my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))

        second_frame = Frame(my_canvas, borderwidth=1, highlightbackground='white', relief=GROOVE)
        my_canvas.create_window((0, 0), window=second_frame, anchor="nw")

        frame1 = LabelFrame(second_frame, labelanchor='n', text='Words Learnt', font=('Tahoma', 30), padx=5, pady=10,
                            relief='raised')
        frame1.pack(padx=10, pady=15)
        frame1.configure(bg='#cccccc')
        root.configure(bg='#cccccc')
        second_frame.configure(bg='#969696')
        main_frame.configure(bg='#969696')
        my_canvas.configure(bg='#969696')

        ##########################
        # user_id = 1
        cur.execute(
            'SELECT word,meaning FROM VOCABULARY WHERE activity_register IN (SELECT activity_register FROM ACTIVITIES_DONE WHERE user_id = (?));',
            (user_id,))
        result = cur.fetchall()
        print(result)

        j = 0
        word_list = []
        for i in result:
            word_list.append(i[0])
            j += 1
        print(word_list)
        Label(frame1, width=18, text='Word', bg='#dcdcdc', fg='black', height=2, font=('Tahoma', 20, 'bold')).grid(
            row=0, column=0)
        Label(frame1, width=45, text='Definition', bg='#dcdcdc', fg='black', height=2,
              font=('Tahoma', 20, 'bold')).grid(row=0, column=1)

        for i, word in enumerate(word_list):
            col_value = 0

            # l2 = Label(frame1, width=7, height=2, bg='#cccccc')
            # l2.grid(row=i+1, column=col_value + 3)

            e1 = Label(frame1, text=result[i][0], width=22, height=2,
                       font=('Tahoma', 20, 'bold'),
                       bg='#f3b0a2', fg='#f95800', relief=RAISED, cursor='hand2')
            e1.grid(row=i + 1, column=col_value, sticky='e')

            e2 = Label(frame1, text=result[i][1], width=55, height=2,
                       font=('Tahoma', 20),
                       fg='#24c30f', bg='#bc5b01', relief='groove')
            e2.grid(row=i + 1, column=col_value + 1, sticky='e')

            f = font.Font(e1, e1.cget("font"))
            f.configure(underline=True)
            e1.configure(font=f)
            word = 'https://www.lexico.com/definition/{}'.format(result[i][0])
            e1.bind('<Button-1>', lambda e, word=word: callback(word))
            # e2['wraplength']=50
            # e2['justify']=LEFT

        root.mainloop()

    def codechef_status():
        root = Toplevel()
        root.title('Codechef Problems Status')
        root.iconphoto(False, PhotoImage(file=r'Window icons\codechef.GIF'))

        def p_status():
            cur.execute('SELECT status_id FROM CODECHEF WHERE problem_tag= ? AND activity_register IN (SELECT activity_register FROM ACTIVITIES_DONE WHERE user_id = ?)ORDER BY status_id ',
                        (problem_tag.get(),user_id))
            res = cur.fetchall()
            print(res)
            text1 = ''

            if not res:
                tkinter.messagebox.showinfo('INPUT ERROR', 'Please enter a valid problem tag or you would have not completed that question')
            elif res[0][0] == 1:
                tkinter.messagebox.showinfo("PROBLEM STATUS",
                                            "You have a successful submission for the problem {}".format(
                                                problem_tag.get()))
            elif res[0][0] == 2:
                tkinter.messagebox.showinfo("PROBLEM STATUS",
                                            'You have partially answered for the problem {}'.format(
                                                problem_tag.get()),
                                            icon='question')
            elif res[0][0] == 3:
                # root.iconbitmap(r'C:\Users\HP\Desktop\ac1.GIF')
                tkinter.messagebox.showinfo("PROBLEM STATUS",
                                            'Time limted exceeded solution to the problem {}'.format(
                                                problem_tag.get()),
                                            icon='warning')
            elif res[0][0] == 4:
                # root.iconbitmap(r'C:\Users\HP\Desktop\ac1.GIF')
                tkinter.messagebox.showinfo("PROBLEM STATUS",
                                            'Wrong answer for the problem {}'.format(problem_tag.get()),
                                            icon='error')

        # BACKGROUND IMAGE
        global codechef_status_bg
        original = Image.open(r'Background images\codechef_status.png')
        resized = original.resize((1290, 660), Image.ANTIALIAS)
        codechef_status_bg = ImageTk.PhotoImage(resized)  # Keep a reference, prevent GC
        Label(root, image=codechef_status_bg).pack()

        # image6 = PhotoImage(file=r'Background images\codechef_status.png')
        # image6_ = Label(root, image=image6).pack()

        medium_font = ('Verdana', 20)
        Label(root, text='Enter the problem tag: ', height=1, bg='#142436', fg='white',
              font=('Gotham Medium Interface', 25, 'bold')).place(x=200, y=300)
        problem_tag = Entry(root, width=30, font=medium_font)
        problem_tag.place(x=570, y=300)

        Button(root, text='Check Problem Status', width=20, height=2, command=p_status, activebackground='white',
               fg='black', bg='white'
               , font=('Arial', 10, 'bold')).place(x=580, y=400)

        root.mainloop()

    def cp_status():
        root = Toplevel()
        root.title('CP Problem Status')
        root.iconphoto(False, PhotoImage(file=r'Window icons\cp.GIF'))
        root.geometry("1290x660")

        def p_status():
            cur.execute('SELECT status_id FROM CP_WEBSITES WHERE problem_link= ? AND activity_register IN (SELECT activity_register FROM ACTIVITIES_DONE WHERE user_id = ?) ORDER BY status_id',
                        (problem_link.get(),user_id))
            res = cur.fetchall()
            print(res)
            text1 = ''

            if not res:
                tkinter.messagebox.showinfo('INPUT ERROR', 'Please enter a valid problem tag or you would have not completed that question')
            elif res[0][0] == 1:
                tkinter.messagebox.showinfo("PROBLEM STATUS",
                                            "You have a successful submission for the problem {}".format(
                                                problem_link.get()))
            elif res[0][0] == 2:
                tkinter.messagebox.showinfo("PROBLEM STATUS",
                                            'You have partially answered for the problem {}'.format(
                                                problem_link.get()),
                                            icon='question')
            elif res[0][0] == 3:
                # root.iconbitmap(r'C:\Users\HP\Desktop\ac1.GIF')
                tkinter.messagebox.showinfo("PROBLEM STATUS",
                                            'Time limted exceeded solution to the problem {}'.format(
                                                problem_link.get()),
                                            icon='warning')
            elif res[0][0] == 4:
                # root.iconbitmap(r'C:\Users\HP\Desktop\ac1.GIF')
                tkinter.messagebox.showinfo("PROBLEM STATUS",
                                            'Wrong answer for the problem {}'.format(problem_link.get()),
                                            icon='error')

        # BACKGROUND IMAGE
        global cp_status_bg
        original = Image.open(r'Background images\cp_status_bg.png')
        resized = original.resize((1290, 660), Image.ANTIALIAS)
        cp_status_bg = ImageTk.PhotoImage(resized)  # Keep a reference, prevent GC
        Label(root, image=cp_status_bg).pack()

        # image6 = PhotoImage(file=r'Background images\cp_status_bg.png')
        # image6_ = Label(root, image=image6).pack()

        medium_font = ('Verdana', 20)
        Label(root, text='Enter the problem link: ', height=1, bg='#142436', fg='white',
              font=('Gotham Medium Interface', 25, 'bold')).place(x=200, y=300)
        problem_link = Entry(root, width=30, font=medium_font)
        problem_link.place(x=570, y=300)

        Button(root, text='Check Problem Status', width=20, height=2, command=p_status, activebackground='white',
               fg='black', bg='white', font=('Arial', 10, 'bold')).place(x=580, y=400)

        root.mainloop()

    def article_status():
        root = Toplevel()
        root.title('Articles Status')
        root.iconphoto(False, PhotoImage(file=r'Window icons\article.GIF'))

        def p_status():
            cur.execute(
                'SELECT article_link FROM ARTICLES WHERE article_link=? AND activity_register in (SELECT activity_register FROM ACTIVITIES_DONE WHERE user_id=?)',
                (problem_link.get(), user_id))
            res = cur.fetchall()
            print(res)
            text1 = ''

            if not res:
                tkinter.messagebox.showinfo('Incomplete', 'You have not read the article')
            else:
                tkinter.messagebox.showinfo('Completed', 'You have read the article')

        # BACKGROUND IMAGE
        global article_bg
        original = Image.open(r'Background images\article_status.png')
        resized = original.resize((1290, 660), Image.ANTIALIAS)
        article_bg = ImageTk.PhotoImage(resized)  # Keep a reference, prevent GC
        Label(root, image=article_bg).pack()
        # image6 = PhotoImage(file=r'Background images\article_status.png')
        # image6_ = Label(root, image=image6).pack()

        medium_font = ('Verdana', 20)
        Label(root, text='Enter article link: ', height=1, bg='#142436', fg='white',
              font=('Gotham Medium Interface', 25, 'bold')).place(x=200, y=300)
        problem_link = Entry(root, width=30, font=medium_font)
        problem_link.place(x=570, y=300)

        Button(root, text='Check Article Status', width=20, height=2, command=p_status, activebackground='white',
               fg='black', bg='white', font=('Arial', 10, 'bold')).place(x=580, y=400)

        root.mainloop()

    def points_for_user_by_day():
        root = Toplevel()
        root.title("Points for the day")
        root.state("zoomed")

        main_frame = Frame(root)
        main_frame.pack(fill=BOTH, expand=1)
        my_canvas = Canvas(main_frame)
        my_canvas.pack(side=LEFT, fill=BOTH, expand=1)

        my_scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
        my_scrollbar.pack(side=RIGHT, fill=Y)
        my_canvas.configure(yscrollcommand=my_scrollbar.set)
        my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))

        second_frame = Frame(my_canvas)
        my_canvas.create_window((0, 0), window=second_frame, anchor="nw")

        cur.execute(
            'SELECT *,sum(follow_up_points+activity_points) as total FROM points WHERE user_id=? GROUP BY user_id,date_ ORDER BY date_ DESC;',
            (user_id,))
        rank_result = cur.fetchall()
        dates=[]
        points=[]
        def graph():
            date_objects = [datetime.strptime(date, '%Y-%m-%d').date() for date in dates]
            plt.plot(date_objects, points, color='blue', marker='o', markerfacecolor='blue', markersize=9)

            plt.xlabel('Date - axis')
            plt.ylabel('Points - axis')
            plt.title('Points vs Date Comparison')
            plt.show()

        def table():
            Label(second_frame, width=11).grid(row=10, column=4)

            Label(second_frame, text='DATE', bg='dark blue', fg='white', width=15, height=3,
                  font=('Helvetica', 15, 'bold')).grid(row=10, column=7)
            Label(second_frame, text='FOLLOW UP POINTS', bg='dark blue', fg='white', width=25, height=3,
                  font=('Helvetica', 15, 'bold')).grid(row=10, column=8)
            Label(second_frame, text='ACTIVITY POINTS', bg='dark blue', fg='white', width=20, height=3,
                  font=('Helvetica', 15, 'bold')).grid(row=10, column=9)
            Label(second_frame, text='TOTAL POINTS', bg='dark blue', fg='white', width=15, height=3,
                  font=('Helvetica', 15, 'bold')).grid(row=10, column=10)

        def results():
            #Button(second_frame,text='graph',command=graph).grid(row=11,column=1)

            j = 0
            ranks = []

            for i in rank_result:
                ranks += rank_result[j]
                j += 1
            how_many = len(ranks) // 5
            if ranks:
                table()
            y_value = 11

            print(ranks)
            j = 0

            # yesterday=(datetime.now()-timedelta(days=1)).strftime("%Y-%m-%d")
            # has_yesterday = False
            # today=datetime.now().strftime("%Y-%m-%d")
            # has_today=False

            for i in range(0, len(ranks), 5):
                fg_var = 'black'
                bg_var = 'white'

                Label(second_frame, text=ranks[i + 1], bg=bg_var, fg=fg_var, width=15, height=2,
                      font=('Helvetica', 15, 'bold')).grid(
                    row=y_value, column=7)
                dates.append(ranks[i+1])
                Label(second_frame, text=ranks[i + 2], bg=bg_var, fg=fg_var, width=25, height=2,
                      font=('Helvetica', 15, 'bold')).grid(row=y_value, column=8)
                Label(second_frame, text=ranks[i + 3], bg=bg_var, fg=fg_var, width=20, height=2,
                      font=('Helvetica', 15, 'bold')).grid(row=y_value, column=9)
                Label(second_frame, text=ranks[i + 4], bg=bg_var, fg=fg_var, width=15, height=2,
                      font=('Helvetica', 15, 'bold')).grid(
                    row=y_value, column=10)
                points.append(ranks[i+4])
                y_value += 1
                j += 1

        table()
        results()

        root.columnconfigure(0, weight=1)
        root.rowconfigure(1, weight=1)

    def points_for_user_by_day_graph():

        cur.execute(
            'SELECT *,sum(follow_up_points+activity_points) as total FROM points WHERE user_id=? GROUP BY user_id,date_ ORDER BY date_ DESC;',
            (user_id,))
        rank_result = cur.fetchall()
        dates=[]
        points=[]

        for i in rank_result:
            dates.append(i[1])
            points.append(i[4])

        date_objects = [datetime.strptime(date, '%Y-%m-%d').date() for date in dates]
        plt.plot(date_objects, points, color='blue', marker='o', markerfacecolor='blue', markersize=9)

        plt.xlabel('Date - axis')
        plt.ylabel('Points - axis')
        plt.title('Points vs Date Comparison')
        plt.show()

         # def table():
         #    Label(second_frame, width=11).grid(row=10, column=4)
         #
         #    Label(second_frame, text='DATE', bg='dark blue', fg='white', width=15, height=3,
         #          font=('Helvetica', 15, 'bold')).grid(row=10, column=7)
         #    Label(second_frame, text='FOLLOW UP POINTS', bg='dark blue', fg='white', width=25, height=3,
         #          font=('Helvetica', 15, 'bold')).grid(row=10, column=8)
         #    Label(second_frame, text='ACTIVITY POINTS', bg='dark blue', fg='white', width=20, height=3,
         #          font=('Helvetica', 15, 'bold')).grid(row=10, column=9)
         #    Label(second_frame, text='TOTAL POINTS', bg='dark blue', fg='white', width=15, height=3,
         #          font=('Helvetica', 15, 'bold')).grid(row=10, column=10)

        # def results():
        #     Button(second_frame,text='graph',command=graph).grid(row=11,column=1)
        #
        #     j = 0
        #     ranks = []
        #
        #     for i in rank_result:
        #         ranks += rank_result[j]
        #         j += 1
        #     how_many = len(ranks) // 5
        #     if ranks:
        #         table()
        #     y_value = 12
        #
        #     print(ranks)
        #     j = 0
        #
        #     # yesterday=(datetime.now()-timedelta(days=1)).strftime("%Y-%m-%d")
        #     # has_yesterday = False
        #     # today=datetime.now().strftime("%Y-%m-%d")
        #     # has_today=False
        #
        #     for i in range(0, len(ranks), 5):
        #         fg_var = 'black'
        #         bg_var = 'white'
        #
        #         Label(second_frame, text=ranks[i + 1], bg=bg_var, fg=fg_var, width=15, height=2,
        #               font=('Helvetica', 15, 'bold')).grid(
        #             row=y_value, column=7)
        #         dates.append(ranks[i+1])
        #         Label(second_frame, text=ranks[i + 2], bg=bg_var, fg=fg_var, width=25, height=2,
        #               font=('Helvetica', 15, 'bold')).grid(row=y_value, column=8)
        #         Label(second_frame, text=ranks[i + 3], bg=bg_var, fg=fg_var, width=20, height=2,
        #               font=('Helvetica', 15, 'bold')).grid(row=y_value, column=9)
        #         Label(second_frame, text=ranks[i + 4], bg=bg_var, fg=fg_var, width=15, height=2,
        #               font=('Helvetica', 15, 'bold')).grid(
        #             row=y_value, column=10)
        #         points.append(ranks[i+4])
        #         y_value += 1
        #         j += 1

        # table()
        # results()

    def article_follow_up():
        root = Toplevel()
        root.title("Article follow up")
        root.geometry("1290x660")
        root.iconphoto(False, PhotoImage(file=r'Window icons\follow_up.GIF'))

        main_frame = Frame(root)
        main_frame.pack(fill=BOTH, expand=1)
        my_canvas = Canvas(main_frame)
        my_canvas.pack(side=LEFT, fill=BOTH, expand=1)

        my_scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
        my_scrollbar.pack(side=RIGHT, fill=Y)

        def _on_mousewheel(event):
            my_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        my_canvas.bind_all("<MouseWheel>", _on_mousewheel)

        my_canvas.configure(yscrollcommand=my_scrollbar.set)
        my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))

        second_frame = Frame(my_canvas)
        my_canvas.create_window((0, 0), window=second_frame, anchor="nw")

        today = datetime.now().strftime("%Y-%m-%d")
        cur.execute(
            'SELECT a.article_link,a.activity_register,f.next_follow_up_number_id FROM FOLLOW_UP f, ARTICLES a WHERE f.date_to_be_done '
            '<= ? AND f.date_time_completed IS NULL AND a.activity_register=f.activity_register  '
            'AND f.activity_register IN (SELECT activity_register FROM ACTIVITIES_DONE WHERE user_id = ? AND activity_id = 26) ORDER BY f.date_to_be_done',
            (today, user_id))
        result = cur.fetchall()

        def fudone(p):

            arr = p.split(',')
            user_id = int(arr[0])
            activity_register = int(arr[1])
            follow_up_number = int(arr[2])
            date_ = arr[3]

            cur.execute(
                'SELECT activity_register FROM FOLLOW_UP WHERE activity_register = ? AND next_follow_up_number_id '
                '= ? AND date_time_completed IS NULL', (activity_register, follow_up_number))
            result__ = cur.fetchall()
            if len(result__) == 0:
                tkinter.messagebox.showinfo('Error', 'You have already completed this article follow up')
            else:
                cur.execute(
                    'UPDATE FOLLOW_UP SET date_time_completed =? WHERE activity_register = ? AND date_time_completed IS NULL AND next_follow_up_number_id=?;',
                    (date_, activity_register, follow_up_number))
                cur.execute('SELECT days_to_be_added FROM FOLLOW_UP_NUMBER WHERE follow_up_number_id = ?',
                            (follow_up_number,))
                result___ = cur.fetchall()

                date_str = date_
                date_object = datetime.strptime(date_str, '%Y-%m-%d').date()
                date_object = date_object + timedelta(days=int(result___[0][0]))
                date_str = date_object.strftime("%Y-%m-%d")

                if follow_up_number <= 6:
                    follow_up_number += 1
                else:
                    follow_up_number = 7
                cur.execute(
                    'INSERT INTO FOLLOW_UP(activity_register,date_to_be_done,next_follow_up_number_id) VALUES (?,?,?)',
                    (activity_register, date_str, follow_up_number))

                cur.execute('SELECT points FROM LIST_OF_ACTIVITIES WHERE activity_id = 26')
                pts = cur.fetchall()
                cur.execute('SELECT repetition FROM ACTIVITIES_DONE WHERE activity_register = ?;',
                            (activity_register,))
                rep = cur.fetchall()

                follow_up_points = int(0.5 * float(pts[0][0]) * float(rep[0][0]))

                addFollowUpPointsForTheDay(user_id, date_, follow_up_points)
                conn.commit()
                tkinter.messagebox.showinfo('Done', 'Congratulations for completing your follow up')

        def fudismiss(p):

            arr = p.split(',')
            print(arr)
            user_id = int(arr[0])
            activity_register = int(arr[1])
            follow_up_number = int(arr[2])
            date_ = arr[3]

            cur.execute(
                'SELECT activity_register FROM FOLLOW_UP WHERE activity_register = ? AND next_follow_up_number_id '
                '= ? AND date_time_completed IS NULL', (activity_register, follow_up_number))
            result__ = cur.fetchall()
            if len(result__) == 0:
                tkinter.messagebox.showinfo('Error', 'You have already completed this article follow up')
            else:
                cur.execute(
                    '''UPDATE FOLLOW_UP SET date_time_completed =? WHERE activity_register = ? AND date_time_completed IS
                        NULL AND next_follow_up_number_id=?;''', ('0000-00-00', activity_register, follow_up_number))
                conn.commit()
                tkinter.messagebox.showinfo('No follow ups', 'Follow up for this activity stopped')

        article_links = []
        for links in result:
            article_links.append(links[0])
        print(article_links)

        Label(second_frame, text='Article Link', width=60, height=2,
              font=('Gotham Medium Interface', 20, 'bold'),
              relief='sunken', activebackground="#00fa68", bg='#e16588', fg="#3d1053").grid(row=0,column=0,columnspan=2)

        for i, url in enumerate(article_links):
            e1 = Label(second_frame, text=result[i][0], width=60, height=3,
                       font=('Gotham Medium Interface', 20, 'bold'),
                       relief='sunken', activebackground="#00fa68", bg='#28324b', fg="#fbdc44", cursor="hand2")
            e1.grid(row=i+1, column=1, sticky='e')

            f = font.Font(e1, e1.cget("font"))
            f.configure(underline=True)
            e1.configure(font=f)
            e1.bind('<Button-1>', lambda e, url=url: callback(url))

            encode = str(user_id) + ',' + str(result[i][1]) + ',' + str(result[i][2]) + ',' + str(today)
            e2 = Button(second_frame, text='Done', width=5, height=2, font=('Gotham Medium Interface', 20, 'bold'),
                        fg='white', bg='#008f40', activebackground='#00f56e',
                        command=lambda encode=encode: fudone(encode))
            e2.grid(row=i+1, column=2, sticky='e')
            e3 = Button(second_frame, text='Dismiss', width=8, height=2,
                        font=('Gotham Medium Interface', 20, 'bold'),
                        fg='white', bg='red', command=lambda encode=encode: fudismiss(encode))
            e3.grid(row=i+1, column=3, sticky='e')

    def word_follow_up():
        today = datetime.now().strftime("%Y-%m-%d")
        cur.execute(
            'SELECT a.word,a.activity_register,f.next_follow_up_number_id,a.meaning FROM FOLLOW_UP f, VOCABULARY a WHERE f.date_to_be_done '
            '<= ? AND f.date_time_completed IS NULL AND a.activity_register=f.activity_register  '
            'AND f.activity_register IN (SELECT activity_register FROM ACTIVITIES_DONE WHERE user_id = ? AND activity_id = 27) ORDER BY f.date_to_be_done',
            (today, user_id))
        result = cur.fetchall()
        print(result)
        print(len(result))

        def fudone(p):

            arr = p.split(',')
            user_id = int(arr[0])
            activity_register = int(arr[1])
            follow_up_number = int(arr[2])
            date_ = arr[3]

            cur.execute(
                'SELECT activity_register FROM FOLLOW_UP WHERE activity_register = ? AND next_follow_up_number_id '
                '= ? AND date_time_completed IS NULL', (activity_register, follow_up_number))
            result10 = cur.fetchall()
            print(result10)
            if len(result10) == 0:
                tkinter.messagebox.showinfo('Error', 'You have already completed this word follow up')
            else:
                cur.execute(
                    'UPDATE FOLLOW_UP SET date_time_completed =? WHERE activity_register = ? AND date_time_completed IS NULL AND next_follow_up_number_id=?;',
                    (date_, activity_register, follow_up_number))
                cur.execute('SELECT days_to_be_added FROM FOLLOW_UP_NUMBER WHERE follow_up_number_id = ?',
                            (follow_up_number,))
                result11 = cur.fetchall()

                date_str = date_
                date_object = datetime.strptime(date_str, '%Y-%m-%d').date()
                date_object = date_object + timedelta(days=int(result11[0][0]))
                date_str = date_object.strftime("%Y-%m-%d")

                if follow_up_number <= 6:
                    follow_up_number += 1
                else:
                    follow_up_number = 7
                cur.execute(
                    'INSERT INTO FOLLOW_UP(activity_register,date_to_be_done,next_follow_up_number_id) VALUES (?,?,?)',
                    (activity_register, date_str, follow_up_number))

                cur.execute('SELECT points FROM LIST_OF_ACTIVITIES WHERE activity_id = 27')
                pts = cur.fetchall()
                cur.execute('SELECT repetition FROM ACTIVITIES_DONE WHERE activity_register = ?;',
                            (activity_register,))
                rep = cur.fetchall()

                follow_up_points = int(0.5 * float(pts[0][0]) * float(rep[0][0]))

                addFollowUpPointsForTheDay(user_id, date_, follow_up_points)
                conn.commit()
                tkinter.messagebox.showinfo('Done', 'Congratulations for completing your follow up')

        def fudismiss(p):

            arr = p.split(',')
            user_id = int(arr[0])
            activity_register = int(arr[1])
            follow_up_number = int(arr[2])
            date_ = arr[3]

            cur.execute(
                'SELECT activity_register FROM FOLLOW_UP WHERE activity_register = ? AND next_follow_up_number_id '
                '= ? AND date_time_completed IS NULL', (activity_register, follow_up_number))
            result10 = cur.fetchall()
            if len(result10) == 0:
                tkinter.messagebox.showinfo('Error', 'You have already completed this word follow up')
            else:
                cur.execute(
                    '''UPDATE FOLLOW_UP SET date_time_completed =? WHERE activity_register = ? AND date_time_completed IS
                        NULL AND next_follow_up_number_id=?;''', ('0000-00-00', activity_register, follow_up_number))
                conn.commit()
                tkinter.messagebox.showinfo('No follow ups', 'Follow up for this activity stopped')

        if not result:
            tkinter.messagebox.showinfo('All done',
                                        'You have no dues on word follow ups and no words scheduled today')
        else:
            root = Toplevel()
            root.title("Word follow up")
            root.iconphoto(False, PhotoImage(file=r'Window icons\follow_up.GIF'))
            root.geometry("1290x660")

            main_frame = Frame(root)
            main_frame.pack(fill=BOTH, expand=1)
            my_canvas = Canvas(main_frame)
            my_canvas.pack(side=LEFT, fill=BOTH, expand=1)

            my_scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
            my_scrollbar.pack(side=RIGHT, fill=Y)

            def _on_mousewheel(event):
                my_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

            my_canvas.bind_all("<MouseWheel>", _on_mousewheel)

            my_canvas.configure(yscrollcommand=my_scrollbar.set)
            my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))

            second_frame = Frame(my_canvas)
            my_canvas.create_window((0, 0), window=second_frame, anchor="nw")

            Label(second_frame, text='Word', width=20, height=2,
                  font=('Gotham Medium Interface', 20, 'bold'),
                  relief='sunken', activebackground="#00fa68", bg='#a9eee6', fg="#625772").grid(row=0,column=0)

            Label(second_frame, text='Meaning', width=40, height=2,
                  font=('Gotham Medium Interface', 20, 'bold'),
                  relief='sunken', activebackground="#00fa68", bg='#a9eee6', fg="#625772").grid(row=0,column=1)

            for i in range(len(result)):
                e1 = Label(second_frame, text=result[i][0], width=20, height=3,
                           font=('Gotham Medium Interface', 20, 'bold'),
                           relief='sunken', activebackground="#00fa68", bg='#3d1053', fg="#e16589", cursor="hand2")
                e1.grid(row=i+1, column=0, sticky='e')
                print(i)
                e5 = Label(second_frame, text=result[i][3], width=40, height=3,
                           font=('Gotham Medium Interface', 20, 'bold'),
                           relief='sunken', activebackground="#00fa68", bg='#c8d3d5', fg="#604083")
                e5.grid(row=i+1, column=1, sticky='e')
                f = font.Font(e1, e1.cget("font"))
                f.configure(underline=True)
                e1.configure(font=f)
                word = 'https://www.lexico.com/definition/{}'.format(result[i][0])
                e1.bind('<Button-1>', lambda e, word=word: callback(word))

                encode = str(user_id) + ',' + str(result[i][1]) + ',' + str(result[i][2]) + ',' + str(today)
                e2 = Button(second_frame, text='Done', width=5, height=2,
                            font=('Gotham Medium Interface', 20, 'bold'),
                            fg='white', bg='#008f40', activebackground='#00f56e',
                            command=lambda encode=encode: fudone(encode))
                e2.grid(row=i+1, column=2, sticky='e')
                e3 = Button(second_frame, text='Dismiss', width=8, height=2,
                            font=('Gotham Medium Interface', 20, 'bold'),
                            fg='white', bg='red', command=lambda encode=encode: fudismiss(encode))
                e3.grid(row=i+1, column=3, sticky='e')

            root.mainloop()

    def book_follow_up():
        root = Toplevel()
        root.geometry("1290x660")
        root.title("Book follow up")

        root.iconphoto(False, PhotoImage(file=r'Window icons\follow_up.GIF'))

        main_frame = Frame(root)
        main_frame.pack(fill=BOTH, expand=1)
        my_canvas = Canvas(main_frame)
        my_canvas.pack(side=LEFT, fill=BOTH, expand=1)

        my_scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
        my_scrollbar.pack(side=RIGHT, fill=Y)

        def _on_mousewheel(event):
            my_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        my_canvas.bind_all("<MouseWheel>", _on_mousewheel)

        my_canvas.configure(yscrollcommand=my_scrollbar.set)
        my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))

        second_frame = Frame(my_canvas)
        my_canvas.create_window((0, 0), window=second_frame, anchor="nw")

        today = datetime.now().strftime("%Y-%m-%d")
        cur.execute(
            'SELECT a.book_id,a.activity_register,f.next_follow_up_number_id,count(a.page_no) FROM FOLLOW_UP f, BOOK_READ_REGISTER a WHERE f.date_to_be_done '
            '<= ? AND f.date_time_completed IS NULL AND a.activity_register=f.activity_register  '
            'AND f.activity_register IN (SELECT activity_register FROM ACTIVITIES_DONE WHERE user_id = ? AND activity_id = 25) GROUP BY a.activity_register ORDER BY f.date_to_be_done',
            (today, user_id))
        result = cur.fetchall()

        def fudone(p):

            arr = p.split(',')
            user_id = int(arr[0])
            activity_register = int(arr[1])
            follow_up_number = int(arr[2])
            date_ = arr[3]

            cur.execute(
                'SELECT activity_register FROM FOLLOW_UP WHERE activity_register = ? AND next_follow_up_number_id '
                '= ? AND date_time_completed IS NULL', (activity_register, follow_up_number))
            result__ = cur.fetchall()
            print(result)
            if len(result__) == 0:
                tkinter.messagebox.showinfo('Error', 'You have already completed these pages as follow ups')
            else:
                cur.execute(
                    'UPDATE FOLLOW_UP SET date_time_completed =? WHERE activity_register = ? AND date_time_completed IS NULL AND next_follow_up_number_id=?;',
                    (date_, activity_register, follow_up_number))
                cur.execute('SELECT days_to_be_added FROM FOLLOW_UP_NUMBER WHERE follow_up_number_id = ?',
                            (follow_up_number,))
                result___ = cur.fetchall()

                date_str = date_
                date_object = datetime.strptime(date_str, '%Y-%m-%d').date()
                date_object = date_object + timedelta(days=int(result___[0][0]))
                date_str = date_object.strftime("%Y-%m-%d")

                if follow_up_number <= 6:
                    follow_up_number += 1
                else:
                    follow_up_number = 7
                cur.execute(
                    'INSERT INTO FOLLOW_UP(activity_register,date_to_be_done,next_follow_up_number_id) VALUES (?,?,?)',
                    (activity_register, date_str, follow_up_number))

                cur.execute('SELECT points FROM LIST_OF_ACTIVITIES WHERE activity_id = 25')
                pts = cur.fetchall()
                cur.execute('SELECT repetition FROM ACTIVITIES_DONE WHERE activity_register = ?;',
                            (activity_register,))
                rep = cur.fetchall()

                follow_up_points = int(0.5 * float(pts[0][0]) * float(rep[0][0]))

                addFollowUpPointsForTheDay(user_id, date_, follow_up_points)
                conn.commit()
                tkinter.messagebox.showinfo('Done', 'Congratulations for completing your follow up')

        def fudismiss(p):

            arr = p.split(',')
            user_id = int(arr[0])
            activity_register = int(arr[1])
            follow_up_number = int(arr[2])
            date_ = arr[3]

            cur.execute(
                'SELECT activity_register FROM FOLLOW_UP WHERE activity_register = ? AND next_follow_up_number_id '
                '= ? AND date_time_completed IS NULL', (activity_register, follow_up_number))
            result__ = cur.fetchall()
            if len(result__) == 0:
                tkinter.messagebox.showinfo('Error', 'You have already completed these pages as follow ups')
            else:
                cur.execute(
                    '''UPDATE FOLLOW_UP SET date_time_completed =? WHERE activity_register = ? AND date_time_completed IS
                        NULL AND next_follow_up_number_id=?;''', ('0000-00-00', activity_register, follow_up_number))
                conn.commit()
                tkinter.messagebox.showinfo('No follow ups', 'Follow up for this activity stopped')

        Label(second_frame, text='Book number', width=20, height=2,
              font=('Gotham Medium Interface', 20, 'bold'),
              relief='sunken', activebackground="#00fa68", bg='#f23005', fg="#ffbe73").grid(row=0,column=0)

        Label(second_frame, text='Pages to follow', width=40, height=2,
              font=('Gotham Medium Interface', 20, 'bold'),
              relief='sunken', activebackground="#00fa68", bg='#f23005', fg="#ffbe73").grid(row=0,column=1)

        for i in range(len(result)):
            e1 = Label(second_frame, text=result[i][0], width=20, height=3,
                       font=('Gotham Medium Interface', 20, 'bold'),
                       relief='sunken', activebackground="#00fa68", bg='#fe9901', fg="#f4eec7")
            e1.grid(row=i+1, column=0, sticky='e')
            cur.execute('SELECT page_no FROM BOOK_READ_REGISTER WHERE activity_register = ?', (result[i][1],))
            pages = cur.fetchall()

            page_str = ''
            for j in pages:
                page_str = page_str + str(j[0]) + ','
            page_str = page_str[0:len(page_str) - 1]

            e1 = Label(second_frame, text=page_str, width=40, height=3,
                       font=('Gotham Medium Interface', 20, 'bold'),
                       relief='sunken', activebackground="#00fa68", bg='#687c37', fg="#ccda46")
            e1.grid(row=i+1, column=1, sticky='e')

            encode = str(user_id) + ',' + str(result[i][1]) + ',' + str(result[i][2]) + ',' + str(today)
            e2 = Button(second_frame, text='Done', width=5, height=2, font=('Gotham Medium Interface', 20, 'bold'),
                        fg='white', bg='#008f40', activebackground='#00f56e',
                        command=lambda encode=encode: fudone(encode))
            e2.grid(row=i+1, column=2, sticky='e')
            e3 = Button(second_frame, text='Dismiss', width=8, height=2,
                        font=('Gotham Medium Interface', 20, 'bold'),
                        fg='white', bg='red', command=lambda encode=encode: fudismiss(encode))
            e3.grid(row=i+1, column=3, sticky='e')

    def interval_one_hr():
        date_ = '2021-01-17'
        # user_id = 1
        total_pts = 0
        for start_hr in range(0, 24):
            end_hr = start_hr + 1
            start_time = str(date_) + ' ' + str(start_hr) + ':00:00'
            end_time = str(date_) + ' ' + str(end_hr) + ':00:00'
            if start_hr < 10:
                start_time = str(date_) + ' 0' + str(start_hr) + ':00:00'
            if end_hr < 10:
                end_time = str(date_) + ' 0' + str(end_hr) + ':00:00'
            cur.execute(
                'SELECT a.date_time_completed,l.activity_name,l.points,a.repetition FROM ACTIVITIES_DONE a, '
                'LIST_OF_ACTIVITIES l WHERE a.date_time_completed>= ? AND a.date_time_completed< ? AND '
                'a.activity_id = l.activity_id AND a.user_id= ? ORDER BY a.date_time_completed',
                (start_time, end_time, user_id))
            sub_total = 0
            result1 = cur.fetchall()
            print(result1)
            print(start_time)
            for j in result1:
                temp = int(j[2]) * int(j[3])
                print(j[0][11:], j[1], j[2], j[3], temp)
                sub_total += temp
                total_pts += temp
            print(end_time, sub_total)
        print(total_pts)

    def one_hour():
        root = Toplevel()

        # BACKGROUND IMAGE
        global one_hour_bg
        original = Image.open(r'Background images\one_hour.png')
        resized = ((1290, 660), Image.ANTIALIAS)
        one_hour_bg = ImageTk.PhotoImage(resized)  # Keep a reference, prevent GC
        Label(root, image=one_hour_bg).pack()

        # image6 = PhotoImage(file=r'Background images\one_hour.png')
        # image6_ = Label(root, image=image6).pack()

        cal = Calendar(root, font="Arial 14", selectmode='day', cursor="hand1")
        cal.place(x=50, y=30)

        def disp_one_hr():
            root = Tk()
            root.title("One hour")
            root.state("zoomed")

            main_frame = Frame(root)
            main_frame.pack(fill=BOTH, expand=1)
            my_canvas = Canvas(main_frame)
            my_canvas.pack(side=LEFT, fill=BOTH, expand=1)

            my_scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
            my_scrollbar.pack(side=RIGHT, fill=Y)
            my_canvas.configure(yscrollcommand=my_scrollbar.set)
            my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))

            def _on_mousewheel(event):
                my_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

            my_canvas.bind_all("<MouseWheel>", _on_mousewheel)

            second_frame = Frame(my_canvas)
            my_canvas.create_window((0, 0), window=second_frame, anchor="nw")

            my_canvas.configure(bg='#aaaaaa')
            second_frame.configure(bg='#b9b9b9')
            root.configure(bg='#aaaaaa')
            main_frame.configure(bg='#aaaaaa')

            date_ = (cal.selection_get()).strftime("%Y-%m-%d")
            total_pts = 0
            Label(second_frame, text=date_, font=('Tahoma', 20, 'bold'), fg='black', bg='#787878',
                  width=75).grid(row=0, column=0, columnspan=3)
            for start_hr in range(0, 24):
                end_hr = start_hr + 1
                start_time = str(date_) + ' ' + str(start_hr) + ':00:00'
                end_time = str(date_) + ' ' + str(end_hr) + ':00:00'
                if start_hr < 10:
                    start_time = str(date_) + ' 0' + str(start_hr) + ':00:00'
                if end_hr < 10:
                    end_time = str(date_) + ' 0' + str(end_hr) + ':00:00'
                cur.execute(
                    'SELECT a.date_time_completed,l.activity_name,l.points,a.repetition FROM ACTIVITIES_DONE a, '
                    'LIST_OF_ACTIVITIES l WHERE a.date_time_completed>= ? AND a.date_time_completed< ? AND '
                    'a.activity_id = l.activity_id AND a.user_id= ? ORDER BY a.date_time_completed',
                    (start_time, end_time, user_id))
                sub_total = 0
                result1 = cur.fetchall()
                # print(result1)
                # print(start_time)
                for j in result1:
                    temp = int(j[2]) * int(j[3])
                    # print(j[0][11:], j[1], j[2], j[3], temp)
                    sub_total += temp
                    total_pts += temp
                # print(end_time, sub_total)
                Label(second_frame, text=start_time[11:], bg='#dcdcdc', width=32, font=('Tahoma', 15, 'bold')).grid(
                    row=start_hr + 1,
                    column=0)
                Label(second_frame, text=str(sub_total), bg='#dcdcdc', width=33, font=('Tahoma', 15, 'bold')).grid(
                    row=start_hr + 1,
                    column=1)
                Label(second_frame, text=end_time[11:], bg='#dcdcdc', width=33, font=('Tahoma', 15, 'bold')).grid(
                    row=start_hr + 1,
                    column=2)

            Label(second_frame, text='Total', bg='#b9b9b9', width=33, height=2, font=('Tahoma', 15, 'bold')).grid(
                row=start_hr + 2,
                column=1)
            Label(second_frame, text=str(total_pts), width=33, height=2, font=('Tahoma', 15, 'bold'),
                  bg='#b9b9b9').grid(
                row=start_hr + 2,
                column=2)
            root.mainloop()

            # print(total_pts)

        Button(root, text='OK', width=20, command=disp_one_hr).place(x=160, y=285)
        root.mainloop()

    def one_hour_with_act():
        root = Toplevel()

        # BACKGROUND IMAGE
        global one_bg
        original = Image.open(r'Background images\one_hour_activity.png')
        resized = original.resize((1290, 660), Image.ANTIALIAS)
        one_bg = ImageTk.PhotoImage(resized)  # Keep a reference, prevent GC
        Label(root, image=one_bg).pack()

        cal = Calendar(root, font="Arial 14", selectmode='day', cursor="hand1")
        cal.place(x=50, y=30)

        def disp_one_hr():
            root = Tk()
            root.title("One hour")
            root.state('zoomed')

            main_frame = Frame(root)
            main_frame.pack(fill=BOTH, expand=1)
            my_canvas = Canvas(main_frame)
            my_canvas.pack(side=LEFT, fill=BOTH, expand=1)

            my_scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
            my_scrollbar.pack(side=RIGHT, fill=Y)
            my_canvas.configure(yscrollcommand=my_scrollbar.set)
            my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))

            def _on_mousewheel(event):
                my_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

            my_canvas.bind_all("<MouseWheel>", _on_mousewheel)

            second_frame = Frame(my_canvas)
            my_canvas.create_window((0, 0), window=second_frame, anchor="nw")
            my_canvas.configure(bg='#aaaaaa')
            second_frame.configure(bg='#aaaaaa')
            root.configure(bg='#aaaaaa')
            main_frame.configure(bg='#aaaaaa')

            def show_graph():
                #date_objects = [datetime.strptime(date, '%Y-%m-%d').date() for date in dates]
                plt.plot(hour_list, points_list, color='blue', marker='o', markerfacecolor='blue', markersize=9)

                plt.xlabel('Hour - axis')
                plt.ylabel('Points - axis')
                plt.title('Points vs Hour Comparison')
                plt.show()

            date_ = (cal.selection_get()).strftime("%Y-%m-%d")
            total_pts = 0
            x = 2
            points_list = []
            hour_list=[]

            for start_hr in range(0, 24):
                end_hr = start_hr + 1
                start_time = str(date_) + ' ' + str(start_hr) + ':00:00'
                end_time = str(date_) + ' ' + str(end_hr) + ':00:00'
                if start_hr < 10:
                    start_time = str(date_) + ' 0' + str(start_hr) + ':00:00'
                if end_hr < 10:
                    end_time = str(date_) + ' 0' + str(end_hr) + ':00:00'
                cur.execute(
                    'SELECT a.date_time_completed,l.activity_name,l.points,a.repetition FROM ACTIVITIES_DONE a, '
                    'LIST_OF_ACTIVITIES l WHERE a.date_time_completed>= ? AND a.date_time_completed< ? AND '
                    'a.activity_id = l.activity_id AND a.user_id= ? ORDER BY a.date_time_completed',
                    (start_time, end_time, user_id))
                sub_total = 0
                result1 = cur.fetchall()
                flag = 0
                #Button(second_frame,text='graph',command=show_graph).grid(row=0,column=0)
                Label(second_frame, text=date_, font=('Tahoma', 20, 'bold'), fg='black', bg='#787878',
                      width=75).grid(row=1, column=0, columnspan=2)

                Label(second_frame, text=start_time[11:], width=115, font=('Tahoma', 15),
                      fg='black', bg='#bfbfbf').grid(row=x, column=0, columnspan=2)
                x += 1
                for j in result1:
                    def on_click(e):
                        e.widget['bg'] = '#fafafa'
                        e.widget.peer['bg'] = "#fafafa"  # set the peer as well

                    def on_leave(e):
                        e.widget['bg'] = '#dcdcdc'
                        e.widget.peer['bg'] = "#dcdcdc"  # set the peer as well

                    temp = int(j[2]) * int(j[3])
                    # print(j[0][11:], j[1], j[2], j[3], temp)
                    sub_total += temp
                    total_pts += temp
                    e1 = Label(second_frame, text=j[0][11:], font=('Tahoma', 12), bg='#dcdcdc', width=71)
                    e1.grid(row=x, column=0)

                    e2 = Label(second_frame, text=str(j[1]), font=('Tahoma', 12), bg='#dcdcdc', width=71)
                    e2.grid(row=x, column=1)
                    e1.bind('<Enter>', on_click)
                    e1.bind('<Leave>', on_leave)
                    e2.bind('<Enter>', on_click)
                    e2.bind('<Leave>', on_leave)

                    e1.peer = e2
                    e2.peer = e1
                    x += 1

                points_list.append(sub_total)
                hour_list.append(start_hr+0.5)

                Label(second_frame, text=end_time[11:], width=115, font=('Tahoma', 15), fg='black',
                      bg='#bfbfbf').grid(row=x, column=0, columnspan=2)
                x += 1
                Label(second_frame, text=str(sub_total), width=58, font=('Tahoma', 15), fg='black',
                      bg='#969696').grid(row=x, column=1)
                Label(second_frame, text='Total points for the hour', width=58, font=('Tahoma', 15), fg='black',
                      bg='#969696').grid(row=x, column=0)
                x += 1
                Label(second_frame, text=str(total_pts), height=2, width=49, font=('Tahoma', 15, 'bold'),
                      fg='black',
                      bg='#b9b9b9').grid(row=x, column=1)
                Label(second_frame, text='Total points for the day', width=49, height=2,
                      font=('Tahoma', 15, 'bold'),
                      fg='black',
                      bg='#b9b9b9').grid(row=x,
                                         column=0)


            # Label(second_frame, text=str(total_pts), width=20, font=('Tahoma', 15, 'bold')).grid(row=x, column=1)
            # Label(second_frame, text='Total points for the day', width=20, font=('Tahoma', 15, 'bold')).grid(
            # row=x,
            # column=0)
            root.mainloop()

            # print(total_pts)

        Button(root, text='OK', width=20, command=disp_one_hr).place(x=160, y=285)
        root.mainloop()

    def one_hour_with_act_graph():



        # Label(second_frame, text=str(total_pts), width=20, font=('Tahoma', 15, 'bold')).grid(row=x, column=1)
        # Label(second_frame, text='Total points for the day', width=20, font=('Tahoma', 15, 'bold')).grid(
        # row=x,
        # column=0)

        # print(total_pts)

        root = Toplevel()

        # BACKGROUND IMAGE
        global one_bg
        original = Image.open(r'Background images\one_hour_activity.png')
        resized = original.resize((1290, 660), Image.ANTIALIAS)
        one_bg = ImageTk.PhotoImage(resized)  # Keep a reference, prevent GC
        Label(root, image=one_bg).pack()

        cal = Calendar(root, font="Arial 14", selectmode='day', cursor="hand1")
        cal.place(x=50, y=30)

        def disp_one_hr():

            def show_graph():
                # date_objects = [datetime.strptime(date, '%Y-%m-%d').date() for date in dates]
                plt.plot(hour_list, points_list, color='blue', marker='o', markerfacecolor='blue', markersize=9)

                plt.xlabel('Hour - axis')
                plt.ylabel('Points - axis')
                plt.title('Points vs Hour Comparison')
                plt.show()


            date_ = (cal.selection_get()).strftime("%Y-%m-%d")
            total_pts = 0
            x = 2
            points_list = []
            hour_list = []

            for start_hr in range(0, 24):
                end_hr = start_hr + 1
                start_time = str(date_) + ' ' + str(start_hr) + ':00:00'
                end_time = str(date_) + ' ' + str(end_hr) + ':00:00'
                if start_hr < 10:
                    start_time = str(date_) + ' 0' + str(start_hr) + ':00:00'
                if end_hr < 10:
                    end_time = str(date_) + ' 0' + str(end_hr) + ':00:00'
                cur.execute(
                    'SELECT a.date_time_completed,l.activity_name,l.points,a.repetition FROM ACTIVITIES_DONE a, '
                    'LIST_OF_ACTIVITIES l WHERE a.date_time_completed>= ? AND a.date_time_completed< ? AND '
                    'a.activity_id = l.activity_id AND a.user_id= ? ORDER BY a.date_time_completed',
                    (start_time, end_time, user_id))
                sub_total = 0
                result1 = cur.fetchall()
                flag = 0
                #Button(second_frame, text='graph', command=show_graph).grid(row=0, column=0)
                #Label(second_frame, text=date_, font=('Tahoma', 20, 'bold'), fg='black', bg='#787878',
                #      width=75).grid(row=1, column=0, columnspan=2)

                #Label(second_frame, text=start_time[11:], width=115, font=('Tahoma', 15),
                 #     fg='black', bg='#bfbfbf').grid(row=x, column=0, columnspan=2)
                x += 1
                for j in result1:
                    def on_click(e):
                        e.widget['bg'] = '#fafafa'
                        e.widget.peer['bg'] = "#fafafa"  # set the peer as well

                    def on_leave(e):
                        e.widget['bg'] = '#dcdcdc'
                        e.widget.peer['bg'] = "#dcdcdc"  # set the peer as well

                    temp = int(j[2]) * int(j[3])
                    # print(j[0][11:], j[1], j[2], j[3], temp)
                    sub_total += temp
                    total_pts += temp
                    #e1 = Label(second_frame, text=j[0][11:], font=('Tahoma', 12), bg='#dcdcdc', width=71)
                    #e1.grid(row=x, column=0)

                    #e2 = Label(second_frame, text=str(j[1]), font=('Tahoma', 12), bg='#dcdcdc', width=71)
                    #e2.grid(row=x, column=1)
                    #e1.bind('<Enter>', on_click)
                    #e1.bind('<Leave>', on_leave)
                    #e2.bind('<Enter>', on_click)
                    #e2.bind('<Leave>', on_leave)

                    #e1.peer = e2
                    #e2.peer = e1
                    x += 1

                points_list.append(sub_total)
                hour_list.append(start_hr + 0.5)

                #Label(second_frame, text=end_time[11:], width=115, font=('Tahoma', 15), fg='black',
                 #     bg='#bfbfbf').grid(row=x, column=0, columnspan=2)
                x += 1
                #Label(second_frame, text=str(sub_total), width=58, font=('Tahoma', 15), fg='black',
                #      bg='#969696').grid(row=x, column=1)
                #Label(second_frame, text='Total points for the hour', width=58, font=('Tahoma', 15), fg='black',
                 #     bg='#969696').grid(row=x, column=0)
                x += 1
                #Label(second_frame, text=str(total_pts), height=2, width=49, font=('Tahoma', 15, 'bold'),
                  #    fg='black',
                  #    bg='#b9b9b9').grid(row=x, column=1)
               # Label(second_frame, text='Total points for the day', width=49, height=2,
                #      font=('Tahoma', 15, 'bold'),
                 #     fg='black',
                  #    bg='#b9b9b9').grid(row=x,
                   #                      column=0)

            # Label(second_frame, text=str(total_pts), width=20, font=('Tahoma', 15, 'bold')).grid(row=x, column=1)
            # Label(second_frame, text='Total points for the day', width=20, font=('Tahoma', 15, 'bold')).grid(
            # row=x,
            # column=0)
            show_graph()

            # print(total_pts)

        Button(root, text='OK', width=20, command=disp_one_hr).place(x=160, y=285)
        root.mainloop()



    def new_book():
        add_book_window = Toplevel()
        add_book_window.geometry("1290x660")
        add_book_window.iconphoto(False, PhotoImage(file=r'Window icons\book.GIF'))
        # BACKGROUND IMAGE
        global a
        original = Image.open(r'Background images\add_book.png')
        resized = original.resize((1290, 660), Image.ANTIALIAS)
        a = ImageTk.PhotoImage(resized)  # Keep a reference, prevent GC
        Label(add_book_window, image=a).pack()

        # add_book_bg = PhotoImage(file=r'Background images\add_book.png')
        # Label(add_book_window, image=add_book_bg).pack()

        def insert_new_book():
            # To insert the new book with correct ID -- book_row
            cur.execute('SELECT COUNT(*) FROM BOOK')
            book_rows = cur.fetchall()
            book_rows = book_rows[0][0] + 1

            # List of books already present
            cur.execute('SELECT book_name FROM BOOK')
            temp_book_list = cur.fetchall()
            book_list = []

            for book in temp_book_list:
                book_list.append(book[0])

            temp_book_list.clear()
            print(book_list)
            for i in book_list:
                temp_book_list.append(str(i).lower())

            if str(book_name.get()).lower() not in temp_book_list:
                cur.execute('INSERT INTO BOOK VALUES (?,?)', (book_rows, book_name.get()))
                conn.commit()
                tkinter.messagebox.showinfo('Success', '{} is added'.format(book_name.get()))
            else:
                tkinter.messagebox.showinfo('Error', 'Book already there')

        medium_font = ('Verdana', 20)
        Label(add_book_window, text='Enter book title: ', height=1, bg='#142436', fg='white',
              font=('Gotham Medium Interface', 25, 'bold')).place(x=200, y=300)
        book_name = Entry(add_book_window, width=30, font=medium_font)
        book_name.place(x=570, y=300)

        Button(add_book_window, text='Add Book', width=20, height=2, command=insert_new_book,
               activebackground='white',
               fg='black', bg='white'
               , font=('Arial', 10, 'bold')).place(x=580, y=400)

        add_book_window.mainloop()

    def library():
        root = Toplevel()
        root.geometry("1290x660")
        root.title('Library')
        root.iconphoto(False, PhotoImage(file=r'Window icons\book.GIF'))

        main_frame = Frame(root)
        main_frame.pack(fill=BOTH, expand=1)
        my_canvas = Canvas(main_frame)
        my_canvas.pack(side=LEFT, fill=BOTH, expand=1)

        my_scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
        my_scrollbar.pack(side=RIGHT, fill=Y)

        def _on_mousewheel(event):
            my_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        my_canvas.bind_all("<MouseWheel>", _on_mousewheel)

        my_canvas.configure(yscrollcommand=my_scrollbar.set)
        my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))

        second_frame = Frame(my_canvas)
        my_canvas.create_window((0, 0), window=second_frame, anchor="nw")

        cur.execute('SELECT * FROM BOOK')
        book_list = cur.fetchall()
        print(book_list)

        Label(second_frame, text='Book ID', width=10, height=2, font=('Gotham Medium Interface', 20, 'bold'),
              relief='sunken', activebackground="#00fa68", bg='#5d5b6a', fg="white").grid(row=0, column=0)
        Label(second_frame, text='Book Title', width=65, height=2, font=('Gotham Medium Interface', 20, 'bold'),
              relief='sunken', activebackground="#00fa68", bg='#5d5b6a', fg="white").grid(row=0, column=1)

        for i in range(len(book_list)):
            e1 = Label(second_frame, text=book_list[i][0], width=10, height=2,
                       font=('Gotham Medium Interface', 20, 'bold'),
                       relief='sunken', activebackground="#00fa68", bg='#cfb495', fg="white")
            e1.grid(row=i + 1, column=0, sticky='e')

            e2 = Label(second_frame, text=book_list[i][1], width=65, height=2,
                       font=('Gotham Medium Interface', 20, 'bold'),
                       fg='white', bg='#cfb495')
            e2.grid(row=i + 1, column=1, sticky='e')

        root.mainloop()

    def your_interval():
        your_interval_window = Toplevel()

        def view():
            if cal1.get_date() > cal2.get_date():
                tkinter.messagebox.showerror('Error', 'Please select a valid date range')
            else:
                root = Tk()
                root.title("Activities done - date range")
                # root.geometry("600x600")
                # root.resizable(width=0,height=0)

                main_frame = Frame(root)
                main_frame.pack(fill=BOTH, expand=1)
                my_canvas = Canvas(main_frame)
                my_canvas.pack(side=LEFT, fill=BOTH, expand=1)

                my_scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
                my_scrollbar.pack(side=RIGHT, fill=Y)
                my_canvas.configure(yscrollcommand=my_scrollbar.set)
                my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))

                def _on_mousewheel(event):
                    my_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

                my_canvas.bind_all("<MouseWheel>", _on_mousewheel)

                my_canvas.configure(yscrollcommand=my_scrollbar.set)
                my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))

                second_frame = Frame(my_canvas)
                my_canvas.create_window((0, 0), window=second_frame, anchor="nw")
                my_canvas.configure(bg='#aaaaaa')
                second_frame.configure(bg='#aaaaaa')
                root.configure(bg='#aaaaaa')
                main_frame.configure(bg='#aaaaaa')

                # date_ = (cal1.selection_get()).strftime("%Y-%m-%d")
                date1 = (cal1.selection_get()).strftime("%Y-%m-%d")
                date2 = (cal2.selection_get()).strftime("%Y-%m-%d")
                # print(date1,date2)
                # print(int(date1[:4]), int(date1[5:7]), int(date1[8:]))

                sdate = date(int(date1[:4]), int(date1[5:7]), int(date1[8:]))
                edate = date(int(date2[:4]), int(date2[5:7]), int(date2[8:]))
                # print(sdate, edate)

                delta = edate - sdate
                x = 1
                for i in range(delta.days + 1):
                    date_ = sdate + timedelta(days=i)
                    date_ = (date_.strftime("%Y-%m-%d"))
                    # print(date_)
                    total_pts = 0

                    x += 1

                    for start_hr in range(0, 24):
                        end_hr = start_hr + 1
                        start_time = str(date_) + ' ' + str(start_hr) + ':00:00'
                        end_time = str(date_) + ' ' + str(end_hr) + ':00:00'
                        if start_hr < 10:
                            start_time = str(date_) + ' 0' + str(start_hr) + ':00:00'
                        if end_hr < 10:
                            end_time = str(date_) + ' 0' + str(end_hr) + ':00:00'
                        cur.execute(
                            'SELECT a.date_time_completed,l.activity_name,l.points,a.repetition FROM ACTIVITIES_DONE a, '
                            'LIST_OF_ACTIVITIES l WHERE a.date_time_completed>= ? AND a.date_time_completed< ? AND '
                            'a.activity_id = l.activity_id AND a.user_id= ? ORDER BY a.date_time_completed',
                            (start_time, end_time, user_id))
                        sub_total = 0
                        result1 = cur.fetchall()
                        print(result1)

                        # print(result1)
                        # print(start_time)
                        def on_click(e):
                            e.widget['bg'] = '#fafafa'
                            e.widget.peer['bg'] = "#fafafa"  # set the peer as well

                        def on_leave(e):
                            e.widget['bg'] = '#dcdcdc'
                            e.widget.peer['bg'] = "#dcdcdc"  # set the peer as well

                        flag = 0
                        Label(second_frame, text=date_, font=('Tahoma', 20, 'bold'), fg='black', bg='#787878',
                              width=75).grid(row=x, column=0, columnspan=2)
                        Label(second_frame, text=start_time[11:], width=115, font=('Tahoma', 15),
                              fg='black', bg='#aaaaaa').grid(row=x, column=0, columnspan=2)
                        x += 1
                        for j in result1:
                            temp = int(j[2]) * int(j[3])
                            # print(j[0][11:], j[1], j[2], j[3], temp)
                            sub_total += temp
                            total_pts += temp
                            e1 = Label(second_frame, text=j[0][11:], font=('Tahoma', 12), bg='#dcdcdc', width=71)
                            e1.grid(row=x, column=0)

                            e2 = Label(second_frame, text=str(j[1]), font=('Tahoma', 12), bg='#dcdcdc', width=71)
                            e2.grid(row=x, column=1)
                            e1.bind('<Enter>', on_click)
                            e1.bind('<Leave>', on_leave)
                            e2.bind('<Enter>', on_click)
                            e2.bind('<Leave>', on_leave)

                            e1.peer = e2
                            e2.peer = e1
                            x += 1

                        # print(end_time, sub_total)
                        Label(second_frame, text=end_time[11:], width=115, font=('Tahoma', 15), fg='black',
                              bg='#aaaaaa').grid(row=x, column=0, columnspan=2)
                        x += 1

                        Label(second_frame, text=str(sub_total), width=58, font=('Tahoma', 15), fg='black',
                              bg='#969696').grid(row=x, column=1)
                        Label(second_frame, text='Total points for the hour', width=58, font=('Tahoma', 15),
                              fg='black',
                              bg='#969696').grid(row=x, column=0)
                        x += 1
                        Label(second_frame, text=str(total_pts), height=2, width=49, font=('Tahoma', 15, 'bold'),
                              fg='black',
                              bg='#b9b9b9').grid(row=x, column=1)
                        Label(second_frame, text='Total points for the day', width=49, height=2,
                              font=('Tahoma', 15, 'bold'),
                              fg='black',
                              bg='#b9b9b9').grid(row=x,
                                                 column=0)

                    x += 1

                root.mainloop()


        # BACKGROUND IMAGE
        global one__bg
        original = Image.open(r'Background images\your_interval.png')
        resized = original.resize((1290, 660), Image.ANTIALIAS)
        one__bg = ImageTk.PhotoImage(resized)  # Keep a reference, prevent GC
        Label(your_interval_window, image=one__bg).pack()

        # your_interval_bg = PhotoImage(file=r'Background images\your_interval.png')
        # Label(your_interval_window, image=your_interval_bg).pack()

        Label(your_interval_window, text='Start Date', fg='white', font=('Gotham Medium Interface', 15, 'bold'),
              bg='#85c9d6').place(x=240,
                                  y=50)
        Label(your_interval_window, text='End Date', fg='white', font=('Gotham Medium Interface', 15, 'bold'),
              bg='#9fd7d8').place(x=930,
                                  y=50)

        cal1 = Calendar(your_interval_window, font="Arial 14", selectmode='day', cursor="hand1")
        cal1.place(x=110, y=100)

        cal2 = Calendar(your_interval_window, font="Arial 14", selectmode='day', cursor="hand1")
        cal2.place(x=790, y=100)

        # Label(your_interval_window, text='Start Time', bg='#205357', fg='white',
        # font=('Gotham Medium Interface', 15, 'bold')).place(x=240,
        # y=400)
        # Label(your_interval_window, text='End Time', bg='#164b6c', fg='white',
        # font=('Gotham Medium Interface', 15, 'bold')).place(x=930,
        # y=400)

        Button(your_interval_window, text='View Activities', font=('Medium Gotham Interface', 15),
               command=view).place(
            x=560, y=550)

        your_interval_window.mainloop()

    def weight():
        #####################
        # user_id = 1
        weight_window = Toplevel()
        weight_window.geometry("1290x660")
        weight_window.title('Add Weight')
        weight_window.iconphoto(False, PhotoImage(file=r'Window icons\weight.GIF'))

        def insert_weight():
            date_ = (cal.selection_get()).strftime("%Y-%m-%d")
            try:
                cur.execute('INSERT INTO WEIGHT VALUES (?,?,?)', (date_, user_id, float(weight_entered.get())))
                if not weight_entered.get():
                    tkinter.messagebox.showinfo('Error', 'Please enter your weight')
                else:
                    conn.commit()
                    tkinter.messagebox.showinfo('Success', 'New weight has been recorded')
            except:
                tkinter.messagebox.showinfo('Error', 'Please enter a valid weight(in kgs)')

        # BACKGROUND IMAGE
        global weight_bg
        original = Image.open(r'Background images\weight.png')
        resized = original.resize((1290, 660), Image.ANTIALIAS)
        weight_bg = ImageTk.PhotoImage(resized)  # Keep a reference, prevent GC
        Label(weight_window, image=weight_bg).pack()

        # weight_bg = PhotoImage(file=r'Background images\weight.png')
        # Label(weight_window, image=weight_bg).pack()
        Label(weight_window, text='Weight as on', font=('Gotham Medium Interface', 20)).place(x=540, y=50)
        cal = Calendar(weight_window, font="Arial 14", selectmode='day', cursor="hand1")
        cal.place(x=450, y=130)

        Label(weight_window, text='Enter weight(in kgs)', font=('Gotham Medium Interface', 20)).place(x=360, y=410)
        medium_font = ('Verdana', 20)
        weight_entered = Entry(weight_window, font=medium_font, width=18)
        weight_entered.place(x=630, y=410)

        Button(weight_window, text='Enter weight', font=('Gotham Medium Interface', 15),
               command=insert_weight).place(x=580,
                                            y=500)

        weight_window.mainloop()

    def show_weight():
        show_weight_window = Toplevel()
        show_weight_window.geometry("1290x660")
        show_weight_window.title('Weight Record')
        show_weight_window.iconphoto(False, PhotoImage(file=r'Window icons\weight.GIF'))

        main_frame = Frame(show_weight_window)
        main_frame.pack(fill=BOTH, expand=1)
        my_canvas = Canvas(main_frame)
        my_canvas.pack(side=LEFT, fill=BOTH, expand=1)

        my_scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
        my_scrollbar.pack(side=RIGHT, fill=Y)
        def _on_mousewheel(event):
            my_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        my_canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        my_canvas.configure(yscrollcommand=my_scrollbar.set)
        my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))

        second_frame = Frame(my_canvas)
        my_canvas.create_window((0, 0), window=second_frame, anchor="nw")

        # weight_bg = PhotoImage(file=r'Background images\show_weight.png')
        # Label(second_frame, image=weight_bg).pack()

        def show_more():
            cur.execute('SELECT date_entered,weight FROM WEIGHT WHERE user_id=? ORDER BY date_entered DESC', (user_id,))
            result = cur.fetchall()
            dates = []
            weights = []
            for date in result:
                dates.append(date[0])
                weights.append(date[1])
            print(dates + weights)

            def show_graph():

                date_objects = [datetime.strptime(date, '%Y-%m-%d').date() for date in dates]
                plt.plot(date_objects, weights, color='blue', marker='o', markerfacecolor='blue', markersize=9)

                plt.xlabel('Date - axis')
                plt.ylabel('Weight - axis')
                plt.title('Weight vs Date Comparison')
                plt.show()

            for i in range(len(result)):
                Label(second_frame, text=result[i][0]).grid(row=i + 2, column=0)
                Label(second_frame, text=result[i][1]).grid(row=i + 2, column=1)

            Button(second_frame, text='Show graph', command=show_graph).grid(row=len(result) + 3, column=1)

        def show_less():
            cur.execute('SELECT date_entered,weight FROM WEIGHT WHERE user_id=? ORDER BY date_entered DESC LIMIT 1',
                        (user_id,))
            result = cur.fetchall()
            print(result)
            last_date = result[0][0]
            last_weight = result[0][1]
            print(last_date, last_weight)

            Label(second_frame, text='Last updated weight' + ' (' + last_date + ')' + ' - ' + str(last_weight),
                  font=('Gotham Medium Interface', 15)).grid(row=0, column=0)
            button = Button(second_frame, text='Show more', command=show_more).grid(row=1, column=1)

        show_less()

        show_weight_window.mainloop()

    def wake():
        #####################
        # user_id = 1
        weight_window = Toplevel()
        weight_window.title('Enter wake up time')
        weight_window.iconphoto(False, PhotoImage(file=r'Window icons\weight.GIF'))

        def handle_click(event):
            weight_entered.delete(0, END)

        def validate():
            if weight_entered.get() == '':
                tkinter.messagebox.showinfo('Error', 'Please enter the wake up time')
            else:
                try:
                    w_time = weight_entered.get()
                    arr = w_time.split(':')
                    hour = int(arr[0])
                    min = int(arr[1])
                    if 0 <= hour < 24 and 0 <= min < 60:
                        date_ = (cal.selection_get()).strftime("%Y-%m-%d")
                        if hour < 4:
                            pts = 250
                        elif hour < 8:
                            offset = ((hour - 4) * 60 + min)
                            offset = (240 - offset) / 10
                            pts = int(3.14477880 * (1.2 ** offset))
                        elif hour < 12:
                            offset = ((hour - 8) * 60 + min)
                            offset = offset / 10
                            pts = int(-3.14477880 * (1.2 ** offset))
                        else:
                            pts = -250
                        f_time = ''
                        if hour < 10:
                            f_time = '0'
                        f_time = f_time + str(hour) + ":"
                        if min < 10:
                            f_time = f_time + '0'
                        f_time = f_time + str(min)

                        cur.execute("SELECT wake_up_time FROM wake_up_time where user_id = ? and date_ = ?;",
                                    (user_id, date_))
                        result = cur.fetchall()
                        if not result:
                            cur.execute(
                                'INSERT INTO wake_up_time(user_id,date_,wake_up_time,pts_fetched) VALUES (?,?,?,?);',
                                (user_id, date_, f_time, pts))
                            addActivityPointsForTheDay(user_id, date_, pts)
                            conn.commit()
                            tkinter.messagebox.showinfo('Success',
                                                        'Wake up time recorded. You have got {} points'.format(pts))
                            weight_entered.delete(0, END)
                            weight_entered.insert(END, 'HH:MM')

                        else:
                            tkinter.messagebox.showinfo('Error', 'You woke up at {}'.format(result[0][0]))
                    else:
                        # TODO   Kill k1
                        raise EXCEPTION

                except:
                    tkinter.messagebox.showerror('Error', 'Please enter a valid time')

        # BACKGROUND IMAGE
        global weight_bg
        original = Image.open(r'Background images\weight.png')
        resized = original.resize((1290, 660), Image.ANTIALIAS)
        weight_bg = ImageTk.PhotoImage(resized)  # Keep a reference, prevent GC
        Label(weight_window, image=weight_bg).pack()

        # weight_bg = PhotoImage(file=r'Background images\weight.png')
        # Label(weight_window, image=weight_bg).pack()
        Label(weight_window, text='Wake up time', font=('Gotham Medium Interface', 20)).place(x=560, y=50)
        cal = Calendar(weight_window, font="Arial 14", selectmode='day', cursor="hand1")
        cal.place(x=450, y=130)

        Label(weight_window, text='Time', font=('Gotham Medium Interface', 20)).place(x=500, y=410)
        medium_font = ('Verdana', 20)
        weight_entered = Entry(weight_window, font=medium_font, width=10)
        weight_entered.place(x=590, y=410)
        weight_entered.insert(END, 'HH:MM')
        # weight_entered.INSERT('end','HH:MM')
        weight_entered.bind('<1>', handle_click)
        # weight_entered.bind('<1>',)

        Button(weight_window, text='Add record', font=('Gotham Medium Interface', 15),
               command=validate).place(x=580,
                                       y=500)

        weight_window.mainloop()

    def show_wake():
        show_weight_window = Toplevel()
        show_weight_window.geometry("1290x660")
        show_weight_window.title('Weight Record')
        show_weight_window.iconphoto(False, PhotoImage(file=r'Window icons\weight.GIF'))

        main_frame = Frame(show_weight_window)
        main_frame.pack(fill=BOTH, expand=1)
        my_canvas = Canvas(main_frame)
        my_canvas.pack(side=LEFT, fill=BOTH, expand=1)

        my_scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
        my_scrollbar.pack(side=RIGHT, fill=Y)
        def _on_mousewheel(event):
            my_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        my_canvas.bind_all("<MouseWheel>", _on_mousewheel)
        my_canvas.configure(yscrollcommand=my_scrollbar.set)
        my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))

        second_frame = Frame(my_canvas)
        my_canvas.create_window((0, 0), window=second_frame, anchor="nw")

        # weight_bg = PhotoImage(file=r'Background images\show_weight.png')
        # Label(second_frame, image=weight_bg).pack()

        def show_more():
            cur.execute('SELECT date_,wake_up_time FROM wake_up_time WHERE user_id=? ORDER BY date_ DESC', (user_id,))
            result = cur.fetchall()
            dates = []
            weights = []
            for date in result:
                dates.append(date[0])
                bugresolve = date[1].split(":")
                bugresolve = bugresolve[0]+'.'+bugresolve[1]
                bugresolve = float(bugresolve)
                weights.append(bugresolve)
                #weights.append(date[1])
            print(dates + weights)

            def show_graph():

                date_objects = [datetime.strptime(date, '%Y-%m-%d').date() for date in dates]
                #weight_ob = [datetime.strptime(time, "%H:%M").time() for time in weights]
                #weight_ob = [datetime.strptime(time, '%H:%M').strftime('%H:%M') for time in weights]
                plt.plot(date_objects, weights, color='blue', marker='o', markerfacecolor='blue', markersize=9)

                plt.xlabel('Wake up time - axis')
                plt.ylabel('Weight - axis')
                plt.title('Wake up time vs Date Comparison')
                plt.show()

            for i in range(len(result)):
                Label(second_frame, text=result[i][0]).grid(row=i + 2, column=0)
                Label(second_frame, text=result[i][1]).grid(row=i + 2, column=1)

            Button(second_frame, text='Show graph', command=show_graph).grid(row=len(result) + 3, column=1)

        def show_less():
            cur.execute('SELECT date_,wake_up_time FROM wake_up_time WHERE user_id=? ORDER BY date_ DESC LIMIT 1',
                        (user_id,))
            result = cur.fetchall()
            print(result)
            last_date = result[0][0]
            last_weight = result[0][1]
            print(last_date, last_weight)

            # Label(second_frame, text='Last updated weight' + ' (' + last_date + ')' + ' - ' + str(last_weight),
            # font=('Gotham Medium Interface', 15)).grid(row=0, column=0)
            button = Button(second_frame, text='Show more', command=show_more).grid(row=1, column=1)

        show_less()

        show_weight_window.mainloop()

    def custom_activity():
        show_weight_window = Toplevel()
        show_weight_window.geometry("1290x660")
        show_weight_window.title('custom activity')
        show_weight_window.iconphoto(False, PhotoImage(file=r'Window icons\weight.GIF'))

        global create
        original = Image.open(
        r'Background images\custom_activity.png')
        resized = original.resize((1290, 660), Image.ANTIALIAS)
        create = ImageTk.PhotoImage(resized) # Keep a reference, prevent GC
        tk.Label(show_weight_window, image=create).pack()

        main_frame = Frame(show_weight_window)
        main_frame.pack(fill=BOTH, expand=1)
        my_canvas = Canvas(main_frame)
        my_canvas.pack(side=LEFT, fill=BOTH, expand=1)

        my_scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
        my_scrollbar.pack(side=RIGHT, fill=Y)
        my_canvas.configure(yscrollcommand=my_scrollbar.set)
        my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))

        second_frame = Frame(my_canvas)
        my_canvas.create_window((0, 0), window=second_frame, anchor="nw")
        big_font=('Verdana',30)

        Label(show_weight_window,bg='#c8f3fc',text='Create your own custom activity',font=big_font).place(x=300,y=100)

        medium_font = ('Verdana', 20)
        small_font = ('Verdana', 15)
        custom_activity_name = tk.Entry(show_weight_window, width=20, relief="sunken",font=medium_font )
        custom_activity_name.insert(END,'Activity name')
        custom_activity_name.place(x=470,y=200)

        custom_activity_points = tk.Entry(show_weight_window, width=20, relief="sunken",font=medium_font )
        custom_activity_points.insert(END,'Activity points')
        custom_activity_points.place(x=470,y=270)

        def handle_click(event):
            custom_activity_name.delete(0, END)

        def handle(event):
            custom_activity_points.delete(0, END)

        custom_activity_name.bind('<1>',handle_click)
        custom_activity_points.bind('<1>',handle)

        def insert_custom_activity():
            try:
                cat_name = (clicked.get())
                activity_name = (custom_activity_name.get())
                act_pts = int(custom_activity_points.get())
            except:
                tkinter.messagebox.showinfo('Error', 'Please enter points as a decimal number')
                return
            cur.execute('SELECT category_id FROM CATEGORY_OF_ACTIVITY WHERE category_name = ?',(cat_name,))
            result = cur.fetchall()
            if(len(result)==0):
                tkinter.messagebox.showinfo('Error', 'Some unexpected error while processing category')
                return
            if(len(activity_name)==0):
                tkinter.messagebox.showinfo('Error', 'Enter an activity name')
                return
            category_id = int(result[0][0])

            cur.execute('SELECT activity_id FROM LIST_OF_ACTIVITIES WHERE activity_name = ?',(activity_name,))
            result = cur.fetchall()
            if(len(result)!=0):
                tkinter.messagebox.showinfo('Error', 'That activity already exists')
                return
            cur.execute('SELECT count(activity_id) FROM LIST_OF_ACTIVITIES')
            result = cur.fetchall()
            activity_id = int(result[0][0]) + 1
            cur.execute('INSERT INTO LIST_OF_ACTIVITIES VALUES (?,?,?,?)',(activity_id,category_id,activity_name,act_pts))
            conn.commit()
            tkinter.messagebox.showinfo('Success', 'Activity added')

        category_names=["COMPETITIVE PROGRAMMING", 'FITNESS', 'KNOWLEDGE' ,'MIND']
        clicked = StringVar()

        # initial menu text
        clicked.set( "COMPETITIVE PROGRAMMING" )

        # Create Dropdown menu
        drop = OptionMenu( show_weight_window , clicked , *category_names )
        drop.place(x=550,y=340)

        confirm_button=Button(show_weight_window,text='create activity', command = insert_custom_activity, activeforeground='#000000',fg='#FFFFFF',bg='#d30404',font=small_font)
        confirm_button.place(x=580,y=400)
        show_weight_window.mainloop()

    root = Toplevel()
    ############################
    # user_id = 1

    # BACKGROUND IMAGE
    # image5 = PhotoImage(file=r'Background images\after_login.png')
    # image5_ = Label(root, image=image5).pack()

    global comp
    original = Image.open(
        r'MicrosoftTeams-image.png')
    resized = original.resize((1290, 660), Image.ANTIALIAS)
    comp = ImageTk.PhotoImage(resized)  # Keep a reference, prevent GC
    tk.Label(root, image=comp).pack()

    # add_activity
    button_1 = Button(root, text='Add Activity', font=('Helvetica', 15, 'bold'), width=15,
                      command=lambda: (activity_category(user_id))).place(x=550, y=50)

    # ranking
    button_2 = Button(root, text='Leaderboard', command=leaderboard, width=15, font=('Helvetica', 15, 'bold')).place(
        x=550, y=100)

    # view codechef tags
    button_3 = Button(root, text='Codechef Problems', font=('Helvetica', 13, 'bold'), width=20, command=codechef).place(
        x=150, y=180)

    # view cp
    button_4 = Button(root, text='CP Websites', command=cp, font=('Helvetica', 13, 'bold'), width=20).place(x=150,
                                                                                                            y=240)

    # view websites
    button_5 = Button(root, text='Online Articles', command=articles, font=('Helvetica', 13, 'bold'), width=20).place(x=150,
                                                                                                               y=300)

    # view word
    button_5 = Button(root, text='Words learnt', command=words, font=('Helvetica', 13, 'bold'), width=20).place(x=150,
                                                                                                                y=360)

    # codechef status
    button_6 = Button(root, text='Codechef Problem Status', command=codechef_status, font=('Helvetica', 13, 'bold'),
                      width=20).place(x=400, y=180)

    # cp status
    button_6 = Button(root, text='CP Problem Status', width=20, command=cp_status,
                      font=('Helvetica', 13, 'bold')).place(x=400, y=240)

    # article status
    button_7 = Button(root, text='Article Status', command=article_status, font=('Helvetica', 13, 'bold'),
                      width=20).place(x=400, y=300)

    # points for day
    button_7 = Button(root, text='Points vs Day', command=points_for_user_by_day, font=('Helvetica', 13, 'bold'),
                      width=40).place(x=200, y=450)

    button_7 = Button(root, text='Points vs Day(Graph)', command=points_for_user_by_day_graph, font=('Helvetica', 13, 'bold'),
                      width=40).place(x=650, y=450)

    # article follow up
    button_7 = Button(root, text='Article Follow Up', command=article_follow_up, font=('Helvetica', 13, 'bold'),
                      width=20).place(x=650, y=180)

    # word follow up
    button_7 = Button(root, text='Word Follow Up', command=word_follow_up, font=('Helvetica', 13, 'bold'),
                      width=20).place(x=650, y=240)

    # book follow up
    button_7 = Button(root, text='Book Follow Up', command=book_follow_up, font=('Helvetica', 13, 'bold'),
                      width=20).place(x=650, y=300)

    # testing
    #button_7 = Button(root, text='Performance in each Hour', command=one_hour, font=('Helvetica', 13, 'bold'), width=40).place(x=200,
    #                                                                                                         y=510)

    # Performance in each Hour with Activity
    button_7 = Button(root, text='Performance in each Hour with Activity', command=one_hour_with_act, font=('Helvetica', 13, 'bold'),
                      width=40).place(x=200, y=510)

    # custom_activity
    button_7 = Button(root,text="Add Your Custom Activity",command=custom_activity ,font=('Helvetica', 13, 'bold'),
    width=40).place(x=200, y=570)

    #########################
    # testing
    # button_7 = Button(root, text='interval one hour', command=interval_one_hr).place(x=800, y=500)

    # Add Book
    button_7 = Button(root, text='Add Book', command=new_book, font=('Helvetica', 13, 'bold'), width=20).place(x=400,
                                                                                                               y=360)

    # Available Books
    button_7 = Button(root, text='Available Books', command=library, font=('Helvetica', 13, 'bold'), width=20).place(x=650, y=360)

    # Performance analysis (Choose your period)
    button_7 = Button(root, text='Performance analysis (Choose your period)', command=your_interval, font=('Helvetica', 13, 'bold'),
                      width=40).place(x=650, y=570)

    # One hour graph
    button_7 = Button(root, text='One hour graph', command=one_hour_with_act_graph,
                      font=('Helvetica', 13, 'bold'),
                      width=40).place(x=650, y=510)

    # Add Weight
    button_7 = Button(root, text='Add Weight', command=weight, font=('Helvetica', 13, 'bold'), width=20).place(x=900,
                                                                                                                y=180)

    # Weight Analysis
    button_7 = Button(root, text='Weight Analysis', command=show_weight, font=('Helvetica', 13, 'bold'), width=20).place(
        x=900, y=240)

    # View Wake up time
    button_7 = Button(root, text='View Wake up time', command=show_wake, font=('Helvetica', 13, 'bold'),
                      width=20).place(x=900, y=360)

    # Enter Wake up time
    button_7 = Button(root, text='Enter Wake up time', command=wake, font=('Helvetica', 13, 'bold'), width=20).place(x=900, y=300)
    root.mainloop()


class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Gotham Medium Interface', size=18, weight="bold")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (Mainmenu, Login, Feedback, AccountCreation):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("Mainmenu")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


class Mainmenu(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # bg = tk.PhotoImage(file='1.png')
        # my_label = tk.Label(self, image=bg)
        # my_label.place(x=0, y=0, relwidth=1, relheight=1)

        global home_image
        original = Image.open(
            r'Background images\main_menu.png')
        resized = original.resize((1290, 660), Image.ANTIALIAS)
        home_image = ImageTk.PhotoImage(resized)  # Keep a reference, prevent GC
        tk.Label(self, image=home_image).pack()

        tk.Label(self, bg='#3b3939', width=100, height=25).place(x=270, y=145)
        tk.Label(self, text='Productivity Manager', width=20, height=1, font=('Malgun Gothic', 40, 'bold'), fg='white',
                 bg='#3b3939').place(x=310, y=180)

        def on_enter(e):
            e.widget['bg'] = '#3b3939'
            e.widget['fg'] = 'white'
            e.widget['relief'] = 'flat'

        def on_leave(e):
            e.widget['bg'] = 'white'
            e.widget['fg'] = 'black'
            e.widget['relief'] = 'raised'

        button1 = tk.Button(self, text="Login", font=controller.title_font,
                            command=lambda: controller.show_frame("Login"), width=20, height=1)
        button2 = tk.Button(self, text="Create new account", font=controller.title_font,
                            command=lambda: controller.show_frame("AccountCreation"), width=20, height=1)
        #button4 = tk.Button(self, text="Points Criteria", font=controller.title_font, width=20, height=1)
        #button5 = tk.Button(self, text="Feedback/suggestions", font=controller.title_font, width=20, height=1,
        #                    command=lambda: controller.show_frame("Feedback"))
        button6 = tk.Button(self, text="Quit",font=controller.title_font, width=20, height=1, command=parent.quit)

        button1.place(x=460, y=275)
        button2.place(x=460, y=325)
        #button4.place(x=460, y=375)
        #button5.place(x=460, y=425)

        button1.bind('<Enter>', on_enter)
        button1.bind('<Leave>', on_leave)
        button2.bind('<Enter>', on_enter)
        button2.bind('<Leave>', on_leave)
        #button4.bind('<Enter>', on_enter)
        #button4.bind('<Leave>', on_leave)
        #button5.bind('<Enter>', on_enter)
        #button5.bind('<Leave>', on_leave)

        button6.place(x=460,y=375)


# class options(tk.Frame)

class Login(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        global back2, photoimage1
        back2 = tk.PhotoImage(
            file=r'back.png')
        photoimage1 = back2.subsample(14, 14)
        # r'C:\Users\HP\AppData\Roaming\JetBrains\PyCharmCE2020.2\THE_BIG_POJECT\Background images\
        global after_home
        original = Image.open(
            r'Background images\login_11.png')
        resized = original.resize((1290, 660), Image.ANTIALIAS)
        after_home = ImageTk.PhotoImage(resized)  # Keep a reference, prevent GC
        tk.Label(self, image=after_home).pack()

        bgg = tk.Label(self, bg='#1f3d57', width=70, height=30).place(x=390, y=100)
        tk.Label(self, text='Login to Productivity Manager', width=30, height=1, font=('Malgun Gothic', 20, 'bold'),
                 fg='white',
                 bg='#1f3d57').place(x=400, y=220)
        medium_font = ('Verdana', 20)

        # icon_=tk.PhotoImage(file=r'C:\Users\HP\Desktop\time.gif')
        # tk.Label(self,image=icon_,bg='#1f3d57').place(x=500,y=180)

        # username = tk.Label(self, text="Username: ", font=("Gotham Medium typeface", 11))
        # password_label = tk.Label(self, text="Password: ", font=("Gotham Medium typeface", 11))
        # username.place(x=500, y=150)
        # password_label.place(x=500, y=200)

        # Entry labels
        name = tk.Entry(self, width=20, relief="sunken", font=medium_font)
        password = tk.Entry(self, width=20, relief="sunken", font=medium_font)

        def verify():
            #try:
                cur.execute('SELECT * FROM USER WHERE user_name = ?', (name.get(),))
                result = cur.fetchall()
                print(result)
                if not result:
                    raise EXCEPTION
                else:
                    user_id = result[0][0]
                    hashed_pass = result[0][2]
                    if hashed_pass != password.get():
                        tkinter.messagebox.showinfo('Credential Error',
                                                    'Incorrect Password. Please enter the correct password')
                    else:
                        for widget in app.winfo_children():
                            widget.destroy()
                        app.configure(bg='green')
                        # time1 = ''
                        clock = Label(app, fg='white', font=('times', 20, 'bold'), bg='green')
                        clock.place(x=600, y=320)
                        time_start = time.strftime('%H:%M:%S')
                        Label(app, text='Time of login', fg='white', font=('times', 20, 'bold'), bg='green').place(
                            x=570,
                            y=180)
                        Label(app, text='Time spent on current session', fg='white', font=('times', 20, 'bold'),
                              bg='green').place(x=460, y=280)
                        Label(app, text=time_start, fg='white', font=('times', 20, 'bold'), bg='green').place(x=600,
                                                                                                              y=215)

                        time_start1 = datetime.now()

                        def tick():
                            global time1
                            time1 = ''
                            # get the current local time from the PC
                            time2 = time.strftime('%H:%M:%S')

                            # if time string has changed, update it
                            if time2 != time1:
                                time1 = time2
                                # print(datetime.now())
                                disp = str(datetime.now() - time_start1)
                                # print(disp)
                                disp = disp[0:7]
                                # print(disp)
                                clock.config(text=disp)
                            # calls itself every 200 milliseconds
                            # to update the time display as needed
                            # could use >200 ms, but display gets jerky
                            clock.after(200, tick)

                        tick()
                        # image_py=PhotoImage(file=r'C:\Users\HP\AppData\Roaming\JetBrains\PyCharmCE2020.2\THE_BIG_POJECT\Background images\start.png')
                        # original = Image.open(r'Background images\MicrosoftTeams-image.png')
                        # resized = original.resize((1290, 660), Image.ANTIALIAS)
                        # start = ImageTk.PhotoImage(resized)  # Keep a reference, prevent GC
                        # Label(app, image=image_py).pack()
                        # app.destroy()
                        # app.quit()
                        # SampleApp().destroy()
                        # Button(app, text='Hello').place(x=100, y=100)
                        CompletedActivity(user_id)

            #except:
                #tkinter.messagebox.showerror('Error',
                                             #'There exists no account with that name. Please create an account')

        def on_enter(e):
            e.widget['bg'] = '#1a2b57'
            e.widget['fg'] = 'white'
            # e.widget['relief'] = 'flat'

        def on_leave(e):
            e.widget['bg'] = 'white'
            e.widget['fg'] = 'black'
            # e.widget['relief'] = 'raised'

        def handle_click(event):
            name.delete(0, END)

        def handle(event):
            password.delete(0, END)

        # Button widgets
        submit = tk.Button(self, text="Login", height=1, width=19,
                           relief="raised", font=controller.title_font,
                           command=verify, )
        new_account = tk.Button(self, text="Create new account", height=1, width=19, relief="raised",
                                font=controller.title_font,
                                command=lambda: controller.show_frame('AccountCreation'))
        # forgot_pass = tk.Button(self, text="Forgot password?", height=1, width=15, relief="raised",
        # font=("Gotham Medium typeface", 10))
        button1 = tk.Button(self, text='Back', image=photoimage1, compound='left', height=20, bg='#1a2b57', fg='white',
                            command=lambda: controller.show_frame('Mainmenu'), relief='flat')
        button1.place(x=0, y=0)

        def on(e):
            e.widget['bg'] = 'white'
            e.widget['fg'] = 'black'
            e.widget['relief'] = 'raised'

        def off(e):
            e.widget['bg'] = '#1a2b57'
            e.widget['fg'] = 'white'
            e.widget['relief'] = 'flat'

        button1.bind('<Enter>', on)
        button1.bind('<Leave>', off)

        name.place(x=470, y=290)
        name.insert(END, 'Username')
        password.place(x=470, y=360)
        password.insert(END, 'Password')
        submit.place(x=500, y=420)
        new_account.place(x=500, y=480)

        submit.bind('<Enter>', on_enter)
        submit.bind('<Leave>', on_leave)

        new_account.bind('<Enter>', on_enter)
        new_account.bind('<Leave>', on_leave)

        name.bind("<1>", handle_click)
        password.bind("<1>", handle)
        # forgot_pass.place(x=600, y=300)


class AccountCreation(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        global back1, photoimage
        back1 = tk.PhotoImage(
            file=r'Window icons\back.png')
        # tk.Frame.__init__(self, parent)

        global create
        original = Image.open(
            r'Background images\create_new_account.png')
        resized = original.resize((1290, 660), Image.ANTIALIAS)
        create = ImageTk.PhotoImage(resized)  # Keep a reference, prevent GC
        tk.Label(self, image=create).pack()

        label = tk.Label(self, text="Get started with your account", fg='white', bg='#112938',
                         font=("Malgun Gothic", 22, 'bold'))
        label.place(x=430, y=30)

        medium_font = ('Verdana', 15)

        def validate():
            cnt = True
            cur.execute('SELECT user_name FROM USER')
            res = cur.fetchall()
            print(res)
            present_user = []
            cur.execute('SELECT COUNT(user_id) FROM USER')
            row_num = cur.fetchall()
            row_num = row_num[0][0] + 1
            for i in res:
                present_user.append(i[0])
            print(present_user)
            if f_name.get() == '':
                tkinter.messagebox.showerror('Input Error', 'Please enter your name')
                cnt = False
            b_date = (cal1.selection_get()).strftime("%Y-%m-%d")

            print(b_date)
            print(datetime.now().date())
            if cal1.selection_get() > datetime.now().date():
                # print(datetime.now())
                tkinter.messagebox.showerror('Input Error', 'Please choose a valid date')
                cnt = False
            if var.get() == 1:
                gender1 = 'MALE'
            else:
                gender1 = 'FEMALE'
            if user_name.get() == '':
                tkinter.messagebox.showerror('Error', 'Please enter a user name')
                cnt = False
            if user_name.get() in present_user:
                tkinter.messagebox.showerror('Error', 'This username is already taken')
                cnt = False
            if password.get() == '':
                tkinter.messagebox.showerror('Error', 'Please enter a password')
                cnt = False
            if (password.get() != c_password.get()):
                tkinter.messagebox.showerror('Error', 'The passwords do not match')
                cnt = False

            if cnt:
                cur.execute('INSERT INTO USER VALUES (?,?,?,?,?,?,?)',
                            (row_num, user_name.get(), password.get(), b_date, gender1, f_name.get(), l_name.get()))
                conn.commit()
                f_name.delete(0, END)
                l_name.delete(0, END)
                password.delete(0, END)
                c_password.delete(0, END)
                user_name.delete(0, END)
                tkinter.messagebox.showinfo('Success', 'Account created successfully')

        tk.Label(self, text="First name : ", bg='#112938', fg='white', font=("Malgun Gothic", 15, 'bold')).place(x=300,
                                                                                                                 y=120,

                                                                                                                 anchor='e')
        tk.Label(self, text="Last name : ", bg='#112938', fg='white', font=("Malgun Gothic", 15, 'bold')).place(x=300,
                                                                                                                y=160,
                                                                                                                anchor='e')
        tk.Label(self, text="Date of birth : ", bg='#112938', fg='white', font=("Malgun Gothic", 15, 'bold')).place(
            x=690, y=120,
            anchor='e')
        tk.Label(self, text="Gender : ", bg='#112938', fg='white', font=("Malgun Gothic", 15, 'bold')).place(x=690,
                                                                                                             y=380,
                                                                                                             anchor='e')

        tk.Label(self, text="User name : ", bg='#112938', fg='white', font=("Malgun Gothic", 15, 'bold')).place(x=300,
                                                                                                                y=300,
                                                                                                                anchor='e')
        tk.Label(self, text="Enter new password : ", bg='#112938', fg='white',
                 font=("Malgun Gothic", 15, 'bold')).place(x=300, y=340,
                                                           anchor='e')
        tk.Label(self, text="Confirm password : ", bg='#112938', fg='white', font=("Malgun Gothic", 15, 'bold')).place(
            x=300, y=380,
            anchor='e')

        def on_enter(e):
            e.widget['bg'] = 'white'
            e.widget['fg'] = '#112938'
            e.widget['relief'] = 'raised'

        def on_leave(e):
            e.widget['bg'] = '#112938'
            e.widget['fg'] = 'white'
            e.widget['relief'] = 'flat'

        def on_button(e):
            e.widget['bg'] = '#112938'
            e.widget['fg'] = 'white'

        def off_button(e):
            e.widget['bg'] = 'white'
            e.widget['fg'] = 'black'

        f_name = tk.Entry(self, width=15, font=medium_font)
        f_name.place(x=300, y=120, anchor='w')
        l_name = tk.Entry(self, width=15, font=medium_font)
        l_name.place(x=300, y=160, anchor='w')
        cal1 = Calendar(self, font="Arial 14", selectmode='day', cursor="hand1")
        cal1.place(x=700, y=110)
        gender = tk.Entry(self, width=30)

        var = IntVar()
        var.set(1)
        Radiobutton(self, text="MALE", variable=var, value=1, bg='#112938', fg='white',
                    font=("Malgun Gothic", 12, 'bold'), selectcolor='black').place(x=700, y=370)
        Radiobutton(self, text="FEMALE", variable=var, value=2, bg='#112938', fg='white',
                    font=("Malgun Gothic", 12, 'bold'), selectcolor='black').place(x=780, y=370)

        # gender.place(x=570, y=300, anchor='w')
        user_name = tk.Entry(self, width=15, font=medium_font)
        user_name.place(x=300, y=300, anchor='w')
        password = tk.Entry(self, width=15, show='*', font=medium_font)
        password.place(x=300, y=340, anchor='w')
        c_password = tk.Entry(self, width=15, show='*', font=medium_font)
        c_password.place(x=300, y=380, anchor='w')

        button = tk.Button(self, text="Create account", height=1, width=13, font=medium_font, command=validate,
                           activebackground='#e0ebcf')
        button.place(x=520, y=450)
        button.bind('<Enter>', on_button)
        button.bind('<Leave>', off_button)

        photoimage = back1.subsample(14, 14)
        button1 = tk.Button(self, text='Back', image=photoimage, compound='left', height=20, bg='#112938', fg='white',
                            command=lambda: controller.show_frame('Mainmenu'), relief='flat')
        button1.place(x=0, y=0)
        button1.bind('<Enter>', on_enter)
        button1.bind('<Leave>', on_leave)


class Feedback(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Your feedback is valuable", font=("Gotham Medium Interface", 20)).place(x=475,
                                                                                                             y=30)

        global back6, photoimage6
        back6 = tk.PhotoImage(file='back.png')
        photoimage6 = back6.subsample(14, 14)

        label1 = tk.Label(self, text="Rate your experience on a scale of 100",
                          font=("Gotham Medium Interface", 12)).place(x=340, y=110)

        scale1 = tk.Scale(self, from_=0, to=100, orient=tk.HORIZONTAL, width=15, length=300)

        scale1.place(x=650, y=90)

        label2 = tk.Label(self, text="Suggestions/Complaints/Feedback", font=("Gotham Medium Interface", 12)).place(
            x=340, y=160)
        ScrolledText(self, height=15).place(x=340, y=200)

        button1 = tk.Button(self, text="Submit response", width=15, height=1).place(x=610, y=480)

        button2 = tk.Button(self, text='Back', image=photoimage6, compound='left', height=20, bg='#FFFFFF',
                            command=lambda: controller.show_frame('Mainmenu')).place(x=0, y=0)


if __name__ == "__main__":
    app = SampleApp()
    app.title("Productivity Manager")

    p1 = tk.PhotoImage(file='pro.png')
    app.iconphoto(False, p1)
    app.mainloop()
