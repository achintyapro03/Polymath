from tkinter import INSERT, messagebox, Label, Button, Frame, StringVar, Entry, Toplevel, Text, Tk, IntVar, Checkbutton, \
    Menubutton, Menu, Scrollbar, RAISED, Radiobutton, END, ttk
import tkinter.ttk as ttk
from PIL import ImageTk, Image
from tkinter import filedialog
from tkcalendar import *
from tksheet import Sheet

from pymongo import *
import pyrebase
# from firebase import firebase

from re import match
from datetime import datetime
from threading import Thread
import time
import os
import shutil
from random import randint, shuffle, choice

from smtplib import SMTP
import webbrowser
from email.message import EmailMessage
import email, smtplib, ssl

# s = MongoClient("mongodb+srv://user1:alpine123@cluster0.myfdu.mongodb.net", tlsCAFile=certifi.where())

client1 = MongoClient(
    "mongodb+srv://user1:alpine123@cluster0.7fwee.gcp.mongodb.net/<dbname>?retryWrites=true&w=majority")
client2 = MongoClient(
    "mongodb+srv://user1:alpine123@cluster0.jm6j5.gcp.mongodb.net/<dbname>?retryWrites=true&w=majority")
client3 = MongoClient(
    "mongodb+srv://user1:alpine123@cluster0.0br3v.gcp.mongodb.net/<dbname>?retryWrites=true&w=majority")
# client1 = MongoClient(
#     "mongodb+srv://user1:alpine123@cluster0.7fwee.gcp.mongodb.net/<dbname>?")
# client2 = MongoClient(
#      "mongodb+srv://user1:alpine123@cluster0.jm6j5.gcp.mongodb.net/<dbname>?")
# client3 = MongoClient(
#      "mongodb+srv://user1:alpine123@cluster0.0br3v.gcp.mongodb.net/<dbname>?")
db1 = client1.get_database('Main1')
db2 = client2.get_database('Main')
db3 = client3.get_database('Main3')
rec1, rec2, rec3 = db1.account, db2.classes, db3.test
accounts = list(map(lambda item: list(item.values()), rec1.find()))
classes = list(map(lambda item: list(item.values()), rec2.find()))
tests = list(map(lambda item: list(item.values()), rec3.find()))

config = {
    "apiKey": "AIzaSyDZ93sh0Xmg6Vo8hSQZkdIjdUDKeQ-5Dno",
    "authDomain": "polymath-93c91.firebaseapp.com",
    "databaseURL": "https://polymath-93c91.firebaseio.com",
    "projectId": "polymath-93c91",
    "storageBucket": "polymath-93c91.appspot.com",
    "messagingSenderId": "623497520965",
    "appId": "1:623497520965:web:0be7ecc5475b1b8774802c",
    "measurementId": "G-E27H1SK6BS"
}

firebase1 = pyrebase.initialize_app(config)
storage = firebase1.storage()

# firebase2 = firebase.FirebaseApplication('https://poly-chat-293dc-default-rtdb.firebaseio.com', None)


current = 1
ans_status = []
imgs = []

time_up = False
men = []
temp_timer = 10

men = ["" for i in range(4)]
eye = ""


def initialise():
    global root3, root2, frame1, frame2, frame3, flag1, backphoto, num, end_time, date, start_time, date_now, current, img, path, questions, media_paths, media
    root3 = Toplevel(root2)
    root3.title("Polymath")
    root3.geometry("960x640")
    root3.iconbitmap("assets/icon.ico")
    root3.resizable(0, 0)
    frame1 = Frame(root3, width=960, height=640)
    frame2 = Frame(root3, width=960, height=640, bg="white")
    frame3 = Frame(root3, width=360, height=340, bg="thistle1", highlightbackground="black", highlightthickness=1)

    flag1 = False
    backphoto = ImageTk.PhotoImage(Image.open("assets/back2.png"))
    num = 0
    end_time = ""
    date = ""
    start_time = ""
    date_now = datetime.today().strftime('%Y-%m-%d').split("-")
    current = 1
    img = ""
    path = ""
    questions = []
    media_paths = []
    media = []


class Login:

    def __init__(self):
        self.email = ""
        self.name = ""
        self.line = None
        self.keep_logged_in = 0

    def drive_ret(self):
        global accounts
        accounts = list(map(lambda item: list(item.values()), rec1.find()))

    def sign_in_check(self):
        global accounts
        self.drive_ret()

        flag = False

        if accounts != None and accounts != []:
            try:
                with open("assets/logged_in.txt", "r") as emailfile:
                    eml = emailfile.read()

                for i in range(0, len(accounts), 1):

                    if accounts[i][1] == eml:
                        flag = True
                        self.email = accounts[i][1]
                        self.line = i

                        self.name = accounts[i][2]
            except:
                pass
        if flag == True:
            lob.page1_lob(1)
        if accounts == None or accounts == False or flag == False:
            self.page1(1)

    def Forgot_Password(self):

        global root
        forgot = Toplevel(root)
        forgot.geometry("400x400")
        forgot.resizable(0, 0)
        forgot.iconbitmap("assets/icon.ico")
        back = ImageTk.PhotoImage(Image.open("assets/forgot2.jpg"))

        def part1():
            global forgot1
            forgot1 = Frame(forgot, width=400, height=400)
            forgot1.place(x=0, y=0)

            Label(forgot1, image=back).place(x=0, y=0)
            Label(forgot1, bg="white", text="Enter your e-mail id", font=("Comic Sans MS",)).place(x=10, y=40)
            Label(forgot1, bg="white", text="An otp will be sent to You", font=("Comic Sans MS",)).place(x=10, y=80)
            ent = Entry(forgot1, width=25)
            ent.place(x=60, y=120)
            Button(forgot1, text="Submit", bg="yellow", command=lambda: part2(ent.get())).place(x=300, y=300)

        def part2(mail):
            global forgot1, forgot2
            result = match('[0-9a-z]+@[a-z]+\.[a-z]+', mail)
            if result != None:
                # try:
                dic = rec1.find_one({"email": mail})
                if dic != None:
                    otp = str(randint(1000, 9999))
                    message = EmailMessage()
                    message.set_content(f"Account Recovery\nYour otp is {otp}")
                    message['Subject'] = "Account Recovery | Polymath"
                    message['From'] = "webmanx03@gmail.com"
                    message['To'] = mail
                    context = ssl.create_default_context()
                    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                        server.login("webmanx03@gmail.com", "alpine123$")
                        server.sendmail("webmanx03@gmail.com", mail, message.as_string())

                else:
                    messagebox.showinfo("Error",
                                        "No account exists corresponding to the email entered.\nPlease create a new one")
                    forgot.destroy()

                try:
                    forgot1.destroy()
                    forgot2 = Frame(forgot, width=400, height=400)
                    forgot2.place(x=0, y=0)
                    Label(forgot2, image=back).place(x=0, y=0)
                    Label(forgot2, text="Enter the otp sent", bg="white").place(x=10, y=100)
                    ent = Entry(forgot2)
                    ent.place(x=120, y=100)
                    Button(forgot2, text="Submit", command=lambda: part3(otp, ent.get(), mail)).place(x=300, y=300)
                except:
                    pass
            else:
                messagebox.showerror("Error", "Enter a valid email address")

        def part3(otp, ent, mail):
            global view_pass2
            view_pass2 = u"\u25CF"

            def toggle_pass_show2():
                global view_pass2
                if view_pass2 == "":
                    view_pass2 = u"\u25CF"
                else:
                    view_pass2 = ""
                entry["show"] = view_pass2

            global accounts

            def change(password):
                global accounts
                rec1.update_one({"email": mail}, {'$set': {'password': password}})
                forgot.destroy()
                accounts = list(map(lambda item: list(item.values()), rec1.find()))
                messagebox.showinfo("Notification", "Password updated Successfully!!")

            global forgot2
            forgot2.destroy()
            if str(otp) == str(ent):
                forgot3 = Frame(forgot, width=400, height=400)
                forgot3.place(x=0, y=0)

                Label(forgot3, image=back).place(x=0, y=0)
                Label(forgot3, bg="white", text="Enter new password", font=("Comic Sans MS",)).place(x=10, y=40)
                entry = Entry(forgot3, show=view_pass2)
                entry.place(x=120, y=100)
                global eye
                # eye = ImageTk.PhotoImage(Image.open("assets/eye.png"))
                Button(forgot3, image=eye, command=lambda: toggle_pass_show2()).place(x=260, y=100)
                Button(forgot3, text="Submit", command=lambda: change(entry.get())).place(x=300, y=300)
            else:
                messagebox.showerror("Error", "You entered a wrong otp")

        part1()
        forgot.mainloop()

    def signin_up(self, case, page):
        global frame_log2, frame_log, backphoto, root, root2, view_pass1
        view_pass1 = u"\u25CF"

        def toggle_pass_show1():
            global view_pass1
            if view_pass1 == "":
                view_pass1 = u"\u25CF"
            else:
                view_pass1 = ""
            p2["show"] = view_pass1

        try:
            frame_log.destroy()

        except:
            # root2.destroy()
            root = Toplevel()
            root.geometry("960x640")

            root.title("Polymath")
            root.iconbitmap("assets/icon.ico")
            root.resizable(0, 0)
            back = Image.open("assets/log.jpg").resize((960, 640))
            backphoto = ImageTk.PhotoImage(back)

        frame_log2 = Frame(root, width=960, height=640)
        frame_log2.place(x=0, y=0)

        Label(frame_log2, image=backphoto).place(x=0, y=0)
        if page == 1:
            var = StringVar()
            var.set("Email")
            root.title("Polymath --> Login")

        elif page == 2:
            var = StringVar()
            var.set(log.email)
            root.title("Polymath --> Edit Password")

        if case == 1 and page == 1:
            Button(frame_log2, text="Forgot Password?", bg="white", font=("Comic Sans MS", 12, "bold"),
                   fg="deep sky blue",
                   command=lambda: self.Forgot_Password()).place(
                x=30, y=260)
            Button(frame_log2, text="Back", command=lambda: self.page1(2)).place(x=400, y=400)

        Label(frame_log2, textvariable=var, bg="white", font=("Comic Sans MS", 14, "bold")).place(x=50, y=80)
        Label(frame_log2, text="Password", bg="white", font=("Comic Sans MS", 14, "bold")).place(x=50, y=120)

        global n2, a2, p2

        if page == 1:
            global e2, checkbox, selected_option

            selected_option = IntVar()
            checkbox = Checkbutton(frame_log2, onvalue=1, offvalue=0, bg="sandy brown", text="Keep me signed in ",
                                   variable=selected_option)
            checkbox.place(x=30, y=310)
            e2 = Entry(frame_log2, width=30)
            e2.place(x=145, y=87)

            Button(frame_log2, text="\nSubmit\n", padx=5, bg="sandy brown",
                   command=lambda: self.collectdata(case)).place(
                x=210, y=265)
        elif page == 2:
            pass
            Button(frame_log2, text="\nSubmit\n", bg="sandy brown",
                   command=lambda: lob.edit_profile(n2.get(), a2.get(), p2.get())).place(x=180, y=260)

        n2 = Entry(frame_log2)
        a2 = Entry(frame_log2)

        if case == 2:
            Label(frame_log2, text="Name", bg="white", font=("Comic Sans MS", 14, "bold")).place(x=50, y=170)

            Label(frame_log2, text="Age", bg="white", font=("Comic Sans MS", 14, "bold")).place(x=50, y=220)

            n2.place(x=145, y=170)
            a2.place(x=145, y=220)

        p2 = Entry(frame_log2, show=view_pass1, width=30)
        p2.place(x=145, y=128)
        global eye
        eye = ImageTk.PhotoImage(Image.open("assets/eye.png"))

        Button(frame_log2, image=eye, command=lambda: toggle_pass_show1()).place(x=345, y=125)
        root.mainloop()

    def collectdata(self, num):
        global li, n, root
        n = num
        l = [e2, p2, n2, a2]
        li = [l[i].get() for i in range(0, 2 * num)]
        li.append(selected_option.get())

        self.email = e2.get()
        self.name = n2.get()
        self.keep_logged_in = selected_option.get()
        self.validate_email()

        root.destroy()

    def validate_email(self):
        global li
        result = match('[0-9a-z]+@[a-z]+\.[a-z]+', li[0])

        if result == None:
            r = Tk()
            r.withdraw()
            messagebox.showerror("Pop-Up", "Email-Id entered is In-valid.")
            r.destroy()
            self.page1(1)
        else:
            li[0] = li[0].strip('\n')
            self.emailprocess(li, n)

    def page1(self, times):
        global root, frame_log, backphoto
        if times == 1:
            root = Tk()
            root.geometry("960x640")

            root.title("Polymath")
            root.iconbitmap("assets/icon.ico")
            root.resizable(0, 0)
            back = Image.open("assets/log.jpg").resize((960, 640))
            backphoto = ImageTk.PhotoImage(back)

        frame_log = Frame(root, width=960, height=640)
        frame_log.place(x=0, y=0)
        Label(frame_log, image=backphoto).place(x=0, y=0)

        i1 = Image.open("assets/login.png")
        i2 = Image.open("assets/signup.png")

        i3 = ImageTk.PhotoImage(Image.open("assets/Polylogo.png"))
        img1 = ImageTk.PhotoImage(i1.resize((int(i1.width / 2), int(i1.height / 2))))
        img2 = ImageTk.PhotoImage(i2.resize((int(i2.width / 2), int(i2.height / 2))))
        Label(frame_log, image=i3).place(x=40, y=60)

        Button(frame_log, image=img1, command=lambda: self.signin_up(1, 1), borderwidth=0).place(x=100, y=280)
        Button(frame_log, image=img2, command=lambda: self.signin_up(2, 1), borderwidth=0).place(x=100, y=380)

        root.mainloop()

    def emailprocess(self, details, cond):
        global accounts, frame2, root
        if (cond == 1):

            flag = False
            for i in range(0, len(accounts), 1):
                if (accounts[i][1] == details[0]):
                    if (accounts[i][2] == details[1]):
                        self.line = i
                        flag = True

            if (flag == True and self.keep_logged_in == 1):
                with open("assets/logged_in.txt", "w") as emailfile:
                    eml = emailfile.write(self.email)

            if (flag == False):
                r = Tk()
                r.withdraw()
                messagebox.showerror("Pop-Up",
                                     "No account created with this EmailID.Please Sign Up to continue or Re-enter the Email-Id and password.")
                r.destroy()
                self.page1(2)
            if (flag == True):
                root.destroy()
                lob.page1_lob(1)

        if (cond == 2):
            flag = False

            if (accounts != False and accounts != None):

                for i in range(0, len(accounts), 1):
                    if (accounts[i][1] == details[0]):
                        flag = True
                        r = Tk()
                        r.withdraw()
                        messagebox.showerror("Pop-Up",
                                             "An account already exists with this Email Id. Please sign in to contiue. Click Forgot Password to retrieve the password.")
                        r.destroy()
                        self.page1(2)

            if (accounts == False or flag == False or accounts == [[]]):
                with open("assets/logged_in.txt", "w") as emailfile:
                    if (self.keep_logged_in == 1):
                        eml = emailfile.write(self.email)
                    else:
                        pass
                fields = ["email", 'age', "name", "address"]
                new_user = {value: details[i] for i, value in enumerate(fields)}
                new_user["classes"] = []
                new_user["history"] = []
                rec1.insert_one(new_user)
                root.destroy()
                lob.page1_lob(1)


class lobby:

    def __init__(self):
        self.code = ""
    def edit_profile(self, name, address, password):
        global root
        rec1.update_one({"email": log.email}, {'$set': {'password': password, "name": name, "address": address}})
        root.destroy()

    def sign_out(self):
        global root2
        with open("assets/logged_in.txt", "w") as file:
            pass
        root2.destroy()

        log.sign_in_check()

    def mid_call_create(self, mail, name, sec, grade, sub):
        global win, frame_class, vsb1
        
        tec.create_class([mail, name.get(), sec.get(), grade.get(), sub.get()])
        win.destroy()
        vsb1.destroy()
        frame_class.destroy()
        self.page1_lob(2)

    def mid_call_join(self, mail, code):
        global win, frame_class, vsb1
        stu.join_class(mail, code)
        win.destroy()
        vsb1.destroy()
        frame_class.destroy()
        self.page1_lob("2times")

    def create_class_win(self):
        global win

        win = Toplevel()
        win.title("Create class")
        win.geometry("300x300")
        win.configure(bg="azure")
        win.iconbitmap("assets/icon.ico")
        Label(win, text="Class Name", bg="azure").place(x=5, y=20)
        Label(win, text="Section", bg="azure").place(x=5, y=50)
        Label(win, text="Grade", bg="azure").place(x=5, y=80)
        Label(win, text="Subject", bg="azure").place(x=5, y=110)
        name = Entry(win)
        sec = Entry(win)
        grade = Entry(win)
        sub = Entry(win)
        name.place(x=80, y=20)
        sec.place(x=80, y=50)
        grade.place(x=80, y=80)
        sub.place(x=80, y=110)
        Button(win, text="Create", command=lambda: self.mid_call_create(log.email, name, sec, grade, sub)).place(x=30,
                                                                                                                 y=150)
        win.mainloop()

    def join_class_win(self):
        global win, men, plus

        win = Toplevel()
        win.title("Create class")
        win.geometry("300x300")
        win.configure(bg="azure")
        win.iconbitmap("assets/icon.ico")
        Label(win, text="Class Code", bg="azure").place(x=5, y=20)
        Label(win, text="Ask your teacher for the class code, then enter it here.", bg="azure").place(x=5, y=40)
        code = Entry(win)

        code.place(x=80, y=60)

        Button(win, text="Join", command=lambda: self.mid_call_join(log.email, code.get())).place(x=30, y=150)
        win.mainloop()

    def page1_lob(self, times):
        global accounts, root2, header1, frame_class, vsb1, men

        def open_website():
            webbrowser.open('https://sites.google.com/view/polymath1/home')

        if (times == 1):
            root2 = Tk()
            root2.title("Polymath")
            root2.iconbitmap("assets/icon.ico")
            root2.geometry("960x700")
            root2.resizable(0, 0)

            men = ["", "", "", ""]
            men[2] = ImageTk.PhotoImage(Image.open("assets/Polylogo.png"))
            men[0] = ImageTk.PhotoImage(Image.open("assets/plus.png"))
            men[1] = ImageTk.PhotoImage(Image.open("assets/menu.png"))
            men[3] = ImageTk.PhotoImage(Image.open("assets/home.png"))

        header1 = Frame(root2, width=1000, height=150, bg="lavender", highlightbackground="black", highlightthickness=1)
        header1.place(x=0, y=0)
        footer = Frame(root2, width=1000, height=180, bg="azure", highlightbackground="black", highlightthickness=1)
        footer.place(x=0, y=555)
        visit = ImageTk.PhotoImage(Image.open("assets/visit_us2.png"))
        Button(header1,image=men[3],borderwidth=0, command=lambda :self.page1_lob(2)).place(x=650,y=50)
        Button(footer, image=visit, borderwidth=0, command=lambda: open_website()).place(x=50, y=3)
        Label(header1, image=men[2]).place(x=30, y=10)
        Label(footer, text="Polymath inc", bg="azure", font=("Comic Sans MS", 15)).place(x=600, y=10)
        mb1 = Menubutton(header1, image=men[0], text="+", relief=RAISED, borderwidth=0)
        mb1.place(x=750, y=50)
        mb1.menu = Menu(mb1, tearoff=0)
        mb1["menu"] = mb1.menu

        mb1.menu.add_command(label="Join Class", command=lambda: self.join_class_win())
        mb1.menu.add_command(label="Create Class", command=lambda: self.create_class_win())

        mb2 = Menubutton(header1, image=men[1], text="+", relief=RAISED, borderwidth=0)
        mb2.place(x=850, y=50)
        mb2.menu = Menu(mb2, tearoff=0)
        mb2["menu"] = mb2.menu

        mb2.menu.add_command(label="Test History", command=lambda: self.history())
        mb2.menu.add_command(label="Edit Profile", command=lambda: log.signin_up(2, 2))
        mb2.menu.add_command(label="SignOut", command=lambda: lob.sign_out())

        frame_class = Frame(root2, width=1000, height=590, bg="white")
        frame_class.place(x=0, y=150)

        text = Text(frame_class, width=120, height=25)
        vsb1 = Scrollbar(frame_class, orient="vertical", command=text.yview)
        text.configure(yscrollcommand=vsb1.set)
        vsb1.pack(side="right", fill="y")

        text.pack(fill="both", expand=True)
        click = lambda code: self.page2_lob(code)
        text.insert("end", "\n   ")
        # Label(text, text="sad").place(x=50,y=300)
        accounts = list(map(lambda item: list(item.values()), rec1.find()))
        acc = []
        # print(accounts)
        for i in accounts:

            if (i[1] == log.email):
                acc = i

        colours = ["azure", "misty rose", "darkolivegreen1", "lavender"]
        try:

            for j in range(len(acc[-2])):

                dic = rec2.find_one({"code": acc[-2][j][0]})
                name = dic["name"]
                sec = dic["section"]
                sub = dic["subject"]
                tex = name + "\n" + sub + "\n" + sec
                col = choice(colours)
                b = Button(frame_class, bg=col, padx=25, pady=25, text=tex,
                           command=lambda idx=j: click(acc[-2][idx][0]))
                text.window_create("end", window=b)
                text.insert("end", "\t\t\t")
                if ((j + 1) % 5 == 0):
                    text.insert("end", "\n\n\n   ")
        except:
            pass

        text.configure(state="disabled")
        root2.mainloop()

    def page2_lob(self, code):
        self.code = code
        global men

        def transition():
            root2.iconify()
            initialise()
            tec.page1_teach([log.email, code])

        def call_exam_page(test_no, code, end):
            root2.iconify()
            time_now = datetime.now().strftime('%H-%M-%S').split("-")
            time_now = [int(i) for i in time_now]
            secs = (end[0] * 3600 + end[1] * 60) - (time_now[0] * 3600 + time_now[1] * 60)
            try:
                shutil.rmtree("temporary")
            except:
                pass
            dic = rec3.find_one({"class": code, "test_no": test_no})
            attempted = [dic["answers"][i][0] for i in range(len(dic["answers"]))]
            if (log.email not in attempted):
                stu.exam_page_2(log.email, secs, code, test_no, case=1)
            else:
                messagebox.showinfo("Notification", "You have already attempted this test!!")

        def back_to_main(a, b, c):
            global frame_test
            frame_test.destroy()
            frame_test2 = Frame(root2, width=1000, height=640)
            dic = rec3.find_one({"class": code})
            # for x in dic["answers"][0]:
            #     print(dic["answers"][0])
            #     print(x)
            #     if(x[0] == log.email):
            #         break

            call_exam_page(a, b, c)
            root2.deiconify()
            self.page1_lob(2)

        def back():
            self.code = ""
            frame_test.destroy()
            header2.destroy()
            self.page1_lob(2)

        global frame3, root2, header1, header2, frame_test, frame_class
        frame_class.destroy()
        # header1.destroy()
        header2 = Frame(root2, width=1000, height=100, bg="white", highlightbackground="black", highlightthickness=1)
        header2.place(x=0, y=0)
        Button(header2, text="Back", command=lambda: back()).place(x=300, y=0)
        s = "Class Code : " + code
        Label(header2, text=s, bg="white", font=("Comic Sans MS", 10)).place(x=500, y=10)
        frame_test = Frame(root2, bg="white", width=1000, height=640)
        frame_test.place(x=0, y=100)
        clas = accounts[log.line][-2]

        # click = lambda x: print(x)

        for i in clas:
            if (i[0] == code):
                if (i[1] == 1):
                    white = "#ffffff"
                    cyan = "#75f0ec"
                    purp = "#d8a9eb"
                    try:
                        style = ttk.Style()

                        style.theme_create( "poly", parent="alt", settings={
                                "TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0]  ,"background" : purp }},
                                "TNotebook.Tab": {
                                    "configure": {"padding": [5, 1], "background": white },
                                    "map":       {"background": [("selected", cyan)],
                                                  "expand": [("selected", [1, 1, 1, 0])] } } } )
                    except:
                        pass

                    style.theme_use("poly")
                    # print("jjojjoo")
                    notebook = ttk.Notebook(frame_test)
                    notebook.place(x=0,y=0)

                    # create frames
                    frame1 = Frame(notebook,bg="white", width=960, height=590)
                    frame2 = Frame(notebook,bg="white", width=960, height=590)
                    frame3 = Frame(notebook,bg="white", width=960, height=590)
                    # frame1.configure(bg="white")
                    frame1.place(x=0,y=0)
                    frame2.place(x=200,y=0)
                    frame3.place(x=200,y=0)
                    # frame1.pack(fill='both', expand=True)
                    # frame2.pack(fill='both', expand=True)

                    # add frames to notebook

                    notebook.add(frame1, text='\t\t\tTests\t\t\t')
                    notebook.add(frame2, text='\t\t\tClassroom\t\t\t')
                    notebook.add(frame3, text='\t\t\tStream\t\t\t   ')
                    Label(frame1,text="hello").place(x=20,y=20)

                    Button(frame1, text="Create new test", command=lambda: transition()).place(x=50, y=50)
                    Label(frame2, text="Students").place(x=60, y=20)
                    students = Text(frame2, width=120, height=15)
                    students.place(x=50,y=100)
                    vsb1 = Scrollbar(orient="vertical", command=students.yview)
                    students.configure(yscrollcommand=vsb1.set)
                    vsb1.pack(side="right", fill="y")
                    students.insert("end", "\n\n")
                    dic = list(rec2.find({"code": self.code}))

                    mem = dic[0]["members"]
                    classstu = []
                    for x in mem:
                        if(x[1] == 0):
                            dic3 = rec1.find_one({"email":x[0]})
                            name= dic3["name"]
                            x.insert(0,name)
                            classstu.append(x)
                    # classstu.append(['1@g.c',0])
                    print(classstu)
                    classstu.sort()
                    print(classstu)

                    for i in range(len(classstu)):
                        b = Button(frame2,borderwidth=0, text=classstu(i), width=60, height=1, bg="azure", font=("Comic Sans MS", 10),
                                   command=lambda idx=i: self.student_details(classstu[idx][0]))
                        students.window_create("end",window=b)
                        students.insert("end","\n\n")
                    break
                else:
                    text1 = Text(frame_test, width=120, height=15)
                    text1.place(x=0, y=30)
                    text2 = Text(frame_test, width=120, height=15)
                    text2.place(x=0, y=320)
                    Label(frame_test, text="Upcoming Tests").place(x=50, y=0)
                    Label(frame_test, text="Ongoing Tests").place(x=50, y=300)
                    dic = list(rec3.find({"class": code}))
                    for i, ele in enumerate(dic):
                        date_now = datetime.today().strftime('%Y-%d-%m').split("-")
                        time_now = datetime.now().strftime('%H-%M-%S').split("-")
                        date_now = [str(int(i)) for i in date_now]
                        date = ele["date"].split("/")
                        start = ele["start time"].split(" ")
                        start = [int(i) for i in start]

                        time_now = [int(i) for i in time_now]
                        end = ele["end time"].split(" ")
                        end = [int(i) for i in end]
                        date[2] = "20" + date[2]
                        date.reverse()
                        if (date == date_now):

                            if (((time_now[0] * 60 + time_now[1]) - (start[0] * 60 + start[1])) > 0):
                                if (((time_now[0] * 60 + time_now[1]) - (end[0] * 60 + end[1])) < 0):
                                    # b = Button(frame_test, padx=25, pady=25, text=str(i + 2),
                                    #            command=lambda idx=i: back_to_main(idx + 1, dic[idx]["class"], end))
                                    b = Button(frame_test, padx=25, pady=25, text=str(i + 2),
                                               command=lambda idx=i: back_to_main(idx + 1, self.code, end))
                                    text2.window_create("end", window=b)
                                    text2.insert("end", "\n\n")

                                else:
                                    tex = i + 1
                                    # b = Button(frame_test, padx=25, pady=25, text=tex,
                                    #            command=lambda idx=i: click([idx + 1, dic[idx]["class"]]))
                                    b = Button(frame_test, padx=25, pady=25, text=tex,
                                               command=lambda idx=i: click([idx + 1, self.code]))
                                    text1.window_create("end", window=b)
                                    text1.insert("end", "\n\n")

    def student_details(self, mail):
        global root2
        win = Toplevel(root2)
        dic1 = rec1.find_one({"email":mail})
        print(dic1)
        hist = dic1["history"]
        for i in range(len(hist)):
            if(hist[i][0] != self.code):
                hist.pop(i)



    def history(self):
        global header1, frame_class, root2, frame_hist1
        try:
            global frame_result
            frame_result.destroy()
        except:
            pass
        frame_class.destroy()
        frame_hist1 = Frame(root2, bg="white", width=1000, height=840)
        frame_hist1.place(x=0, y=150)
        hist1 = Text(frame_hist1, width=120, height=15)
        hist1.place(x=0, y=30)
        dic3 = rec1.find_one({"email": log.email})
        hist = dic3["history"]
        hist1.insert("end", "\n")
        # vsb1 = Scrollbar(orient="vertical", command=hist1.yview)
        # hist1.configure(yscrollcommand=vsb1.set)
        # vsb1.pack(side="right", fill="y")
        # hist1.pack(fill="both", expand=True)
        hist1.insert("end", "\n\n")

        for i in range(len(hist)):
            dic = rec3.find_one({"class": hist[i][0], "test_no": hist[i][1]})
            correct = dic["questions"]
            tot = 0

            for j in correct:
                tot += int(j["scheme"][0])
            hist1.insert("end", "\t\t\t")
            temp = len(hist) - i - 1
            tex = str(temp + 1) + "\t" + str(hist[temp][3]) + "/" + str(tot) + "\t View Result ->"
            b = Button(frame_hist1, text=tex, width=60, height=5, bg="azure", font=("Comic Sans MS", 10),
                       command=lambda idx=temp: self.result(hist[idx]))
            hist1.window_create("end", window=b)
            hist1.insert("end", "\n\n")

    def test_pri(self, correct, qno,ans, marked):
        global root2, view
        view = Toplevel(root2)
        view.geometry("550x500")
        view.configure(bg= "white")
        view.resizable(0,0)
        Label(view,text="Question "+str(qno+1),bg="white",font=("Comic Sans MS", 10)).place(x=0,y=0)
        q=Text(view,width=60, height=8,bg="alice blue")
        q.place(x=0, y=20)
        q.insert("end",correct["que"])
        q.config(state="disabled")
        pos = [140,220,300,380]
        print("marked  :",marked," type ",type(marked))
        print("ans  :", ans, " type ", type(ans))
        tick = ImageTk.PhotoImage(Image.open("assets/checked .png"))
        wrong = ImageTk.PhotoImage(Image.open("assets/cancel.png"))
        unatt = ImageTk.PhotoImage(Image.open("assets/minus.png"))
        for i in range(4):
            s = ""
            if(i == int(marked)):
                if(str(ans)==str(marked)):
                    s = "green yellow"
                    Label(view,image=tick, borderwidth=0).place(x=500, y=pos[i])
                else:
                    s = "coral"
                    Label(view, image=wrong, borderwidth=0).place(x=500, y=pos[i])

            else:
                s = "azure"
                Label(view, image=unatt, borderwidth=0).place(x=500, y=pos[i])
            o=Text(view,width=60, height=4,bg=s)
            o.place(x=0, y=pos[i])
            o.insert("end",correct["options"][0][i])
            o.config(state="disabled")

        view.mainloop()

    def result(self, hist):

        global root2, frame_hist1, frame_result
        frame_hist1.destroy()
        frame_result = Frame(root2, bg="white", width=1000, height=840)
        frame_result.place(x=0, y=150)

        dic = rec3.find_one({"class": hist[0], "test_no": hist[1]})
        correct = dic["questions"]

        dat = []
        view = Text(frame_result, bg="azure", width=100, height=30)
        # view.place(x=550, y=30)
        view.place(x=0, y=30)
        for i in range(len(hist[2])):

            cor = correct[i]["options"][1][0]
            atmp = hist[2][i]
            if str(cor) == str(atmp):
                x = correct[i]["scheme"][0]
            elif str(cor) == " ":
                x = 0
            elif str(cor) != str(atmp):
                x = correct[i]["scheme"][1]
            lis = [[correct[i]["que"], str(cor + 1), str(int(atmp) + 1), x]]
            # dat.append(lis)
            lab = Label(frame_result, text=str(i + 1))
            view.window_create("end", window=lab)
            view.insert("end", "\t")
            sheet = Sheet(frame_result,
                          data=lis, width=600, height=80, row_height=80, show_header=False, show_x_scrollbar=False,
                          show_y_scrollbar=False, show_row_index=False)
            view.window_create("end", window=sheet)
            view.insert("end", "\t")
            c = Button(frame_result, text="click", width=5, height=1, fg="white", bg="#845BB3",
                       font=("Comic Sans MS", 10),
                       command=lambda idx=i: self.test_pri(correct[idx],idx, correct[idx]["options"][1][0], hist[2][idx] ))
            view.window_create("end", window=c)
            view.insert("end", "\n\n")

        # sheet.place(x=0, y=0)
        Label(frame_result, text="Sl.No\t\tQuestion\t\tCorrect\t    Ans Marked\tMarks Obtained\tView Question",
              font=("Comic Sans MS", 10), bg="white").place(x=0, y=0)



class Student:
    def get_tests(self, code):
        dic = list(rec3.find({"class": code}))

    def join_class(self, mail, code):
        dic = rec2.find_one({"code": code})
        mem = dic["members"]
        flag = True
        for i in mem:
            if (mail == i[0]):
                flag = False
                break
        if (flag == True):
            mem.append([mail, 0])
        rec2.update_one({"code": code}, {'$set': {'members': mem}})

        for i in accounts:
            if (i[1] == mail):
                x = i[-1]
        x.append([code, 0])

        rec1.update_one({"email": mail}, {'$set': {'classes': x}})

    def cont_display(self, code, test_no, case, mail, secs):
        global frame2, frame3, frame4, frame5, timer_frame, root4, imgs
        test = rec3.find_one({"class": code, "test_no": test_no})

        questions = test["questions"]
        ans_status = [[["#"], [0, 0, 0]] for i in range(0, int(test["num of q"]))]
        imgs = ["" for i in range(int(test["num of q"]))]
        timer_frame = Frame(root4, height=80, width=300, bg="#12232E", highlightbackground="black",
                            highlightthickness=1)
        timer_frame.place(x=1050, y=0)
        frame2 = Frame(root4, width=600, height=600, bg="#12232E", highlightbackground="black", highlightthickness=1)
        frame2.place(x=0, y=0)
        frame3 = Frame(root4, width=450, height=600, bg="#12232E", highlightbackground="black", highlightthickness=1)
        frame3.place(x=600, y=0)
        frame4 = Frame(root4, width=300, height=520, bg="#12232E", highlightbackground="black", highlightthickness=1)
        frame4.place(x=1050, y=80)
        frame5 = Frame(root4, width=1350, height=200, bg="#12232E", highlightbackground="black", highlightthickness=1)
        frame5.place(x=0, y=600)

        try:

            os.mkdir("temporary")
        except:
            pass
        if (case == 1):
            for i in range(int(test["num of q"])):
                try:
                    t = str(test["test_no"])
                    path_cloud = code + "/" + t + "/" + str(i + 1) + ".png"
                    path_loc = "temporary/" + str(i + 1) + ".png"

                    storage.child(path_cloud).download(path_loc)
                    imgs[i] = ImageTk.PhotoImage(Image.open(path_loc))
                except:
                    pass

        def frames(change):

            global imgs
            global current, var

            ans_status[current - 1][1][0] = 1

            def click(idx):
                navi.destroy()
                vsb.destroy()

                ans_status[idx][1][0] = 1
                frames(idx - current + 1)

            def trans(x):
                navi.destroy()
                vsb.destroy()
                frames(x)

            def review():
                navi.destroy()
                vsb.destroy()
                temp = ans_status[current - 1][1][2]

                if (temp == 1):
                    ans_status[current - 1][1][2] = 0
                elif (temp == 0):
                    ans_status[current - 1][1][2] = 1
                frames(0)

            def save(x):
                navi.destroy()
                vsb.destroy()

                if (x.get() == -1):
                    frames(1)
                else:
                    ans_status[current - 1][0][0] = x.get()
                    ans_status[current - 1][1][1] = 1
                    frames(1)

            def de_select():
                navi.destroy()
                vsb.destroy()
                ans_status[current - 1][0][0] = "#"
                ans_status[current - 1][1][1] = 0
                frames(0)

            def submit():

                def mid(x):
                    if (x.lower() == "submit"):
                        confirm.destroy()
                        self.end_test(code, mail, test_no, ans_status, case=1)
                    else:
                        confirm.destroy()
                        submit()

                confirm = Toplevel(root2)
                confirm.configure(bg="azure")
                confirm.geometry("400x200")
                confirm.iconbitmap("assets/icon.ico")
                Label(confirm, bg="azure", text="Are you sure that you want to submit.You still have time left").place(
                    x=10, y=20)
                Label(confirm, bg="azure", text="Entry \"submit\" to confirm").place(x=10, y=40)
                ent = Entry(confirm)
                ent.place(x=60, y=80)
                Button(confirm, text="Confirm", command=lambda: mid(ent.get())).place(x=120, y=120)

            if (change == -1):
                if (current > 1):
                    current -= 1
            elif (change == 1):

                if (current < int(test["num of q"])):
                    current += 1

            frame2.place(x=0, y=0)
            frame3 = Frame(root4, width=450, height=600, bg="#12232E", highlightbackground="black",
                           highlightthickness=1)
            frame3.place(x=600, y=0)
            frame4.place(x=1050, y=80)
            frame5.place(x=0, y=600)
            question = Text(frame2, width=65, height=8, bg="PaleTurquoise1")
            question.place(x=30, y=60)

            tex = " Question " + str(current)
            Label(frame2, text=tex, font=("Comic Sans MS", 10), fg="white", bg="#007CC7").place(x=30, y=30)

            question.insert(INSERT, questions[current - 1]["que"])
            question.config(state="disabled")

            Label(frame3, image=imgs[current - 1], borderwidth=0).place(x=30, y=40)

            var = IntVar()
            opt = questions[current - 1]["options"]
            x = "#"
            if (ans_status[current - 1][0][0] == "#"):
                x = -1
            else:
                x = ans_status[current - 1][0][0]
            var.set(x)

            sel1 = Radiobutton(frame2, text="a", variable=var, value=0, bg="PaleTurquoise1")
            sel1.place(x=20, y=220)
            sel2 = Radiobutton(frame2, text="b", variable=var, value=1, bg="PaleTurquoise1")
            sel2.place(x=20, y=310)
            sel3 = Radiobutton(frame2, text="c", variable=var, value=2, bg="PaleTurquoise1")
            sel3.place(x=20, y=400)
            sel4 = Radiobutton(frame2, text="d", variable=var, value=3, bg="PaleTurquoise1")
            sel4.place(x=20, y=490)
            option1 = Text(frame2, width=50, height=4)
            option1.place(x=65, y=220)
            option1.insert(INSERT, opt[0][0])
            option2 = Text(frame2, width=50, height=4)
            option2.place(x=65, y=310)
            option2.insert(INSERT, opt[0][1])
            option3 = Text(frame2, width=50, height=4)
            option3.place(x=65, y=400)
            option3.insert(INSERT, opt[0][2])
            option4 = Text(frame2, width=50, height=4)
            option4.place(x=65, y=490)
            option4.insert(INSERT, opt[0][3])

            navi = Text(frame4, width=120, height=40, bg="azure")
            vsb = Scrollbar(orient="vertical", command=navi.yview)
            navi.configure(yscrollcommand=vsb.set)
            vsb.pack(side="right", fill="y")
            navi.pack(fill="both", expand=True)

            col = {"100": "dark orange", "110": "OliveDrab1", "101": "cyan", "000": "white", "111": "yellow"}

            navi.insert("end", "\n  ")

            for i in range(int(test["num of q"])):
                bgb = ans_status[i][1]
                c = str(bgb[0]) + str(bgb[1]) + str(bgb[2])

                b = Button(frame4, padx=10, pady=5, text=str(i + 1), bg=col[c], command=lambda idx=i: click(idx))
                navi.window_create("end", window=b)
                navi.insert("end", "  ")
                if ((i + 1) % 4 == 0):
                    navi.insert("end", "\n\n  ")

            Button(frame5, text=u"\u2190", padx=5, font=("Comic Sans MS", 20, "bold"), fg="white", bg="#007CC7",
                   command=lambda: trans(-1), borderwidth=0).place(x=500, y=60)
            Button(frame5, text=u"\u2192", padx=5, font=("Comic Sans MS", 20, "bold"), fg="white", bg="#007CC7",
                   command=lambda: trans(1), borderwidth=0).place(x=570, y=60)

            Button(frame5, text="Save and Next", font=("Comic Sans MS", 10), fg="white", bg="#007CC7",
                   command=lambda: save(var), borderwidth=0).place(x=40, y=60)
            Button(frame5, text="Review/Un", font=("Comic Sans MS", 10), fg="white", bg="#007CC7",
                   command=lambda: review(), borderwidth=0).place(x=200, y=60)

            Button(frame5, text="Deselect All", font=("Comic Sans MS", 10), fg="white", bg="#007CC7",
                   command=lambda: de_select(), borderwidth=0).place(x=300, y=60)

            Button(frame5, text="Submit", padx=10, pady=6, font=("Comic Sans MS", 10, "bold"), fg="white", bg="#845BB3",
                   command=lambda: submit(), borderwidth=0).place(x=700, y=60)

            cols = [["white", "Not Visited"], ["dark orange", "Unattempted"], ["OliveDrab1", "Answered"],
                    ["cyan", "Marked for Review"], ["yellow", "Answered and Marked for review"]]
            height = 10
            for i in cols:
                Button(frame5, state="disabled", bg=i[0], padx=10, pady=2).place(x=1050, y=height)
                Label(frame5, text=i[1], font=("Comic Sans MS", 10), fg="white", bg="#203647").place(x=1100, y=height)
                height += 30

        Thread(target=stu.timer, args=[secs, mail, code, test_no]).start()

        frames(0)

    def timer(self, secs, mail, code, test_no):
        global root4, ans_status
        temp = secs
        hour = StringVar()
        minute = StringVar()
        second = StringVar()

        Label(timer_frame, text="Time Left:", font=("Comic Sans MS", 14, ""), fg="white", bg="#12232E").place(x=5, y=20)

        hr = Entry(timer_frame, width=3, font=("Comic Sans MS", 18, ""), textvariable=hour)
        hr.place(x=130, y=20)
        mi = Entry(timer_frame, width=3, font=("Comic Sans MS", 18, ""), textvariable=minute)
        mi.place(x=180, y=20)
        se = Entry(timer_frame, width=3, font=("Comic Sans MS", 18, ""), textvariable=second)
        se.place(x=230, y=20)

        hr.configure(state="disabled")
        mi.configure(state="disabled")
        se.configure(state="disabled")
        while True:
            mins, secs = divmod(temp, 60)
            hours = 0
            if mins > 60:
                hours, mins = divmod(mins, 60)
            hour.set("{0:2d}".format(hours))
            minute.set("{0:2d}".format(mins))
            second.set("{0:2d}".format(secs))
            timer_frame.update()
            time.sleep(1)
            if temp == 0 and Toplevel.winfo_exists(root4) == 1:
                root4.destroy()
                # print(ans_status, "please")
                self.end_test(code, mail, test_no)
                break
            temp -= 1

    def exam_page_2(self, mail, secs, code, test_no, case=0):

        global root4, current, imgs, root2, ans_status, frame2, frame3, frame4, frame5, timer_frame

        root4 = Toplevel(root2)
        root4.title("Polymath")

        root4.geometry("1350x800")
        root4.resizable(0, 0)
        root4.iconbitmap("assets/icon.ico")
        root4.focus_force()

        thread1 = Thread(target=stu.cont_display, args=[code, test_no, case, mail, secs])
        thread1.start()

        root4.mainloop()

    def end_test(self, code, mail, test_no, ans_status, case=0):
        global root4
        if (case == 1):
            root4.destroy()
        # print(ans_status,"sstatus")
        dic = rec3.find_one({"class": code, "test_no": test_no})
        ans = dic["answers"]
        # print(ans)
        ans_str = ''.join([str(i[0][0]) for i in ans_status])
        # print(ans_str, "plaease")
        # print(ans_str,len(ans_str))

        correct = dic["questions"]
        score = 0
        for i in range(len(correct)):
            # print(ans_status[i],"1")
            # print(ans_str[i])
            # print(correct[i]["options"][1][0])
            if (str(ans_str[i]) == str(correct[i]["options"][1][0])):
                score += int(correct[i]["scheme"][0])
            elif (str(ans_str[i]) == "#"):
                pass
            else:
                score += int(correct[i]["scheme"][1])
            # print(score)
        ans.append([mail, ans_str, score])
        # print(score)
        rec3.update_one({"class": code, "test_no": test_no}, {'$set': {'answers': ans}})
        dic3 = rec1.find_one({"email": log.email})
        hist = dic3["history"]
        hist.append([code, test_no, ans_str, score])
        rec1.update_one({"email": log.email}, {'$set': {'history': hist}})
        shutil.rmtree("temporary")


class Teacher:
    def create_class(self, details):
        ints = randint(2, 6)
        n = [str(randint(0, 10)) for i in range(ints)]
        s = [chr(randint(97, 123)) for i in range(8 - ints)]
        code = n + s
        shuffle(code)
        code = "".join(code)
        details.append(code)
        details.append([[details[0], 1]])
        # data = {"code" : code,
        #         "msgs" : [""],
        #         "time" : [""]
        # }
        # result = firebase2.post("class",data)
        # details.append(result["name"])
        # fields = ["teacher", "name", "section", "grade", "subject", "code", "members","chat_room"]
        fields = ["teacher", "name", "section", "grade", "subject", "code", "members"]
        clas = {f: d for (f, d) in zip(fields, details)}

        rec2.insert_one(clas)
        x = []
        for i in accounts:
            if (i[1] == details[0]):
                x = i[-1]
        x.append([details[5], 1])
        rec1.update_one({"email": details[0]}, {'$set': {'classes': x}})

    def page1_teach(self, det):
        global flag1, backphoto
        Label(frame1, image=backphoto).place(x=0, y=0)
        frame1.place(x=0, y=0)
        Label(frame1, text="Examination Details", bg="lemon chiffon", font=("Times", 18, "bold"), padx=10,
              pady=10).place(x=300, y=20)
        Label(frame1, text="Select Date", bg="lemon chiffon", padx=5).place(x=600, y=240)
        cal = Calendar(frame1, selectmode="day", year=int(date_now[0]), month=int(date_now[1]), day=int(date_now[2]))
        cal.place(x=600, y=280)

        def back():
            global root3, root2
            root3.destroy()
            root2.deiconify()

        def col(x):
            global flag1, num, start_time, end_time, date, questions, media, media_paths
            if (((x[-1][2] * 60) + x[-1][3]) - ((x[-1][0]) * 60 + x[-1][1]) < 3):
                messagebox.showerror("Error", "Enter valid time")
                self.page1_teach(det)


            else:
                flag1 = True
                num, start_time, end_time = x[0], str(x[1][0]) + " " + str(x[1][1]), str(x[1][2]) + " " + str(x[1][3])
                questions = [{} for i in range(int(num))]
                media_paths = ["" for i in range(int(num))]
                media = ["" for i in range(int(num))]
                date = cal.get_date()
                ele = date.split("/")
                ele[2] = "20" + ele[2]
                ele = [int(i) for i in ele]
                if ((ele[2] * 30 * 12 + ele[1] * 30 + ele[0]) < (
                        int(date_now[0]) * 30 * 12 + int(date_now[1]) * 12 + int(date_now[2]))):
                    messagebox.showerror("Error", "Enter valid date")
                    self.page1_teach(det)

                else:
                    frame1.forget()
                    frame1.destroy()
                    self.page2_teach(det)

        style = ttk.Style()
        style.theme_use('default')
        style.configure('My.TSpinbox', arrowsize=15)

        Label(frame1, text="Number of Questions", padx=4, bg="lemon chiffon").place(x=550, y=80)
        ent1 = Entry(frame1)
        ent1.place(x=700, y=80)
        Label(frame1, text="Enter hour and minute in 24 hour format", bg="lemon chiffon").place(x=550, y=120)

        Label(frame1, text="Start Time", padx=38, bg="lemon chiffon").place(x=550, y=160)
        start_hour = ttk.Spinbox(frame1, style='My.TSpinbox', from_=0, to=23, width=3)
        start_hour.place(x=700, y=160)
        start_min = ttk.Spinbox(frame1, style='My.TSpinbox', from_=0, to=60, width=3)
        start_min.place(x=800, y=160)
        Label(frame1, text="End Time", padx=38, bg="lemon chiffon").place(x=550, y=200)
        end_hour = ttk.Spinbox(frame1, style='My.TSpinbox', from_=0, to=23, width=3)
        end_hour.place(x=700, y=200)
        end_min = ttk.Spinbox(frame1, style='My.TSpinbox', from_=0, to=60, width=3)
        end_min.place(x=800, y=200)

        time = [start_hour, start_min, end_hour, end_min]
        Button(frame1, text="Submit", padx=15, pady=5, bg="lemon chiffon", font=(20),
               command=lambda: col([ent1.get(), [int(i.get()) for i in time]])).place(x=600, y=530)
        Button(frame1, text="Back", bg="lemon chiffon", font=(20), command=lambda: back()).place(x=600, y=580)

        root3.mainloop()

    def page2_teach(self, det):

        def retreive_q(tex):
            questions[current - 1]["que"] = tex.get("1.0", END)

        def retreive_med():
            global path
            media[current - 1] = img
            media_paths[current - 1] = path
            path = ""

        def retreive_opts(opt, correct):
            opt = [i.get("1.0", END) for i in opt]
            coridx = [i for i in range(len(correct)) if correct[i] == "1"]
            questions[current - 1]["options"] = [opt, coridx]

        def retreive_scheme(p, n):
            questions[current - 1]["scheme"] = [p, n]

        def open():
            global img, frame3, path

            root3.filename = filedialog.askopenfilename(initialdir="C:/", title="Select a file", filetypes=(
                ("png files", "*.png"), ("jpg files", "*.jpg"), ("all files", "*.*")))
            img_temp = Image.open(root3.filename)
            ratiox, ratioy = img_temp.width / 300, img_temp.height / 200
            if (ratiox > 1 or ratioy > 1):
                ratio = max(ratiox, ratioy)
                img_temp = img_temp.resize((int(img_temp.width / ratio), int(img_temp.height / ratio)))

            try:
                os.mkdir("temporary")
            except:
                pass
            route = "temporary/" + str(current) + ".png"
            img_temp.save(route, format="png")
            img = ImageTk.PhotoImage(Image.open(route))
            path = root3.filename
            Label(frame3, image=img).place(x=30, y=60)

        frame2 = Frame(root3, width=600, height=310, bg="PaleTurquoise1", highlightbackground="black",
                       highlightthickness=1)
        frame4 = Frame(root3, width=600, height=310, bg="thistle1", highlightbackground="black", highlightthickness=1)
        frame5 = Frame(root3, width=360, height=300, bg="PaleTurquoise1", highlightbackground="black",
                       highlightthickness=1)

        def frames(change):
            global frame3
            frame3 = Frame(root3, width=360, height=340, bg="thistle1", highlightbackground="black",
                           highlightthickness=1)

            global current, img
            if (change == -1):
                if (current > 1):
                    current -= 1
            elif (change == 1):

                if (current < int(num)):
                    current += 1

            frame2.place(x=0, y=0)
            frame3.place(x=600, y=0)
            frame4.place(x=0, y=290)
            frame5.place(x=600, y=301)
            question = Text(frame2, width=65, height=8)
            question.place(x=30, y=60)

            Label(frame2, text="Enter the Question", bg="thistle1").place(x=30, y=30)
            tex = "Enter the Question " + str(current)
            Label(frame2, text=tex, bg="thistle1").place(x=30, y=30)
            Button(frame2, text="Confirm", bg="thistle1", command=lambda: retreive_q(question)).place(x=30, y=200)
            Label(frame3, text="Attach Media", bg="PaleTurquoise1").place(x=20, y=30)
            Button(frame3, text="Select/Change File", bg="PaleTurquoise1", command=lambda: open()).place(x=150, y=30)
            Button(frame3, text="Confirm", bg="PaleTurquoise1", command=lambda: retreive_med()).place(x=100, y=300)

            Label(frame4, text="Select the Options for the entered Question", bg="PaleTurquoise1").place(x=65, y=20)
            var1, var2, var3, var4 = StringVar(), StringVar(), StringVar(), StringVar()
            var1.set(0)
            var2.set(0)
            var3.set(0)
            var4.set(0)
            sel1 = Checkbutton(frame4, text="a", variable=var1, onvalue=1, offvalue=0, bg="PaleTurquoise1")
            sel1.place(x=20, y=55)
            sel2 = Checkbutton(frame4, text="b", variable=var2, onvalue=1, offvalue=0, bg="PaleTurquoise1")
            sel2.place(x=20, y=115)
            sel3 = Checkbutton(frame4, text="c", variable=var3, onvalue=1, offvalue=0, bg="PaleTurquoise1")
            sel3.place(x=20, y=175)
            sel4 = Checkbutton(frame4, text="d", variable=var4, onvalue=1, offvalue=0, bg="PaleTurquoise1")
            sel4.place(x=20, y=235)
            option1 = Text(frame4, width=50, height=2)
            option1.place(x=65, y=55)
            option2 = Text(frame4, width=50, height=2)
            option2.place(x=65, y=115)
            option3 = Text(frame4, width=50, height=2)
            option3.place(x=65, y=175)
            option4 = Text(frame4, width=50, height=2)
            option4.place(x=65, y=235)

            Button(frame4, text="Confirm", bg="PaleTurquoise1",
                   command=lambda: retreive_opts([option1, option2, option3, option4],
                                                 [var1.get(), var2.get(), var3.get(), var4.get()])).place(x=500, y=260)

            try:

                question.insert(INSERT, questions[current - 1]["que"])
            except:
                pass
            try:

                Label(frame3, image=media[current - 1]).place(x=30, y=60)

            except:
                pass

            try:
                opts = questions[current - 1]["options"]
                var = [var1, var2, var3, var4]
                option = [option1, option2, option3, option4]
                for i in opts[1]:
                    var[i].set(1)
                for i in range(len(opts[0])):
                    option[i].insert(INSERT, opts[0][i])

            except:
                pass
            style = ttk.Style()
            style.theme_use('default')
            style.configure('My.TSpinbox', arrowsize=15)

            style.configure('My.TSpinbox', arrowsize=15)
            Label(frame5, text="Marking Scheme", bg="thistle1").place(x=130, y=60)
            Label(frame5, text="Correct:", bg="thistle1").place(x=20, y=75)
            Label(frame5, text="Incorrect", bg="thistle1").place(x=90, y=75)
            pos = ttk.Spinbox(frame5, style='My.TSpinbox', from_=0, to=10, width=3)
            pos.place(x=20, y=100)
            neg = ttk.Spinbox(frame5, style='My.TSpinbox', from_=-10, to=0, width=3)
            neg.place(x=90, y=100)
            Button(frame5, text="Confirm", bg="thistle1", command=lambda: retreive_scheme(pos.get(), neg.get())).place(
                x=160, y=100)
            Button(frame5, text=u"\u2190", padx=5, font=("Times", 20, "bold"), bg="thistle1",
                   command=lambda: frames(-1)).place(x=50, y=220)
            Button(frame5, text=u"\u2192", padx=5, font=("Times", 20, "bold"), bg="thistle1",
                   command=lambda: frames(1)).place(x=120, y=220)
            if (current == int(num)):
                Button(frame5, text="Finalise", padx=5, command=lambda: self.add_test(det)).place(x=50, y=150)

        frames(0)

    def add_test(self, det):
        global questions, num, start_time, date, end_time

        dic = list(rec3.find({'host': det[0]}))
        test_no = len(dic) + 1
        fields = ["host", "test_no", "class", "questions", "num of q", "start time", "end time", "date", "answers"]
        details = [det[0], test_no, det[1], questions, num, start_time, end_time, date, [], []]
        x = {f: d for (f, d) in zip(fields, details)}
        rec3.insert_one(x)
        shutil.rmtree("temporary")

        for i in range(int(num)):
            if (media_paths[i] != ""):
                pyre_path = det[1] + "/" + str(test_no) + "/" + str(i + 1) + ".png"
                storage.child(pyre_path).put(media_paths[i])


log = Login()
tec = Teacher()
lob = lobby()
stu = Student()
log.sign_in_check()
