from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk
from datetime import datetime
import mysql.connector
import os

lP = Tk()
lP.title("Login")
lP.geometry('850x520')
lP.configure(bg="#26A69A")

descLoc = None
lid = None

def database_handle(method,vara=None,varb=None):
    global loginB,registerB,reEntry
    global mn, mt, mc, mp, mq
    global pn ,pa ,pg ,pp
    global tname,descLoc,lid
    
    conn = mysql.connector.connect(host='localhost',user='root', password='sanjay25',database= 'pharmacy')
    cursor = conn.cursor()

    def login():
        cursor.execute(f'SELECT * FROM admins WHERE U_NAME="{vara}" AND U_PASS="{varb}"')
        result = cursor.fetchone()
        if result:
            return '1'

    def register():
        cursor.execute("SELECT U_ID FROM admins")
        result=cursor.fetchall()
        prev_id = list(result[-1])
        new_id = prev_id[0]+1

        cursor.execute(f'INSERT INTO admins(U_ID, U_NAME, U_PASS) VALUES({new_id},"{vara}","{varb}")')
        conn.commit()
        messagebox.showinfo("Registration complete", "New user registered")

    def ret():
        cursor.execute(f"SELECT {vara} from {varb}")
        result=cursor.fetchall()
        return(result)

    def register_med():
        cursor.execute("SELECT M_ID FROM medicine")
        result=cursor.fetchall()
        if mn.get().strip() != "" and mt.get().strip() != "" and mc.get().strip() != "" and mp.get().strip() != "" and mq.get().strip() != "":

            if mt.get() != "Select Medicine Type":

                prev_id = list(result[-1])
                new_id = prev_id[0]+1
                print(new_id)
                cursor.execute(f'INSERT INTO medicine(M_ID,M_NAME,M_TYPE,M_MFN,M_PRICE,M_QUANTITY) VALUES({new_id},"{mn.get()}","{mt.get()}","{mc.get()}",{mp.get()},{mq.get()})')
                conn.commit()
                messagebox.showinfo("Registration complete", "New medicine registered")
                mn.set("")
                mc.set("")
                mt.set("Select Medicine Type")
                mp.set("")
                mq.set("")

            else:
                messagebox.showerror("Registration error", "Select medicine type")
        else:
            messagebox.showerror("Registration error", "Field cannot be empty")

    def register_patient():
        
        cursor.execute('SELECT P_ID from patients')
        result=cursor.fetchall()
        prev_id = list(result[-1])
        new_id = prev_id[0]+1

        print(new_id,pn.get(),pg.get(),pa.get(),pp)

        if pn.get().strip()!='' and pa.get().strip()!='' and pg.get().strip()!='' and pp !='/Users/sanjayumaganesh/Desktop/Pharmacy Management/material/assests/placeholder.jpg':
            if pg != "Select Patient's Gender ":
                cursor.execute(f'INSERT INTO patients(P_ID, P_NAME, P_AGE, P_PICTURE,P_GENDER,L_ID,O_ID) VALUES({new_id},"{pn.get()}","{pa.get()}","{pp}","{pg.get()}",NULL,NULL)')
                conn.commit()
                messagebox.showinfo("Registration complete", "New patient registered")
                
                pn.set("")
                pa.set("")
                pg.set("Select Patient's Gender")
                pp.set("/Users/sanjayumaganesh/Desktop/Pharmacy Management/material/assests/placeholder.jpg")
                
            else:
                messagebox.showerror("Registration error", "Select patients gender")
        else:
            messagebox.showerror("Registration error", "Field cannot be empty")

    def register_lab():
        global lab_tk, lid
        
        if tname.get() != "Select Test Category" and tname.get().strip() != "" :
            print(lid)
            date = datetime.now().strftime("%Y-%m-%d")
            cursor.execute(f'INSERT INTO labs (L_ID, TEST_NAME, DATE, Manager_name) VALUES ({lid},"{tname.get()}","{date}","{userEntry.get()}")')
            cursor.execute(f"UPDATE patients SET L_ID = {lid} WHERE P_NAME = '{vara}'")
            conn.commit()
            messagebox.showinfo("Request", "Request Sent")
            lab_tk.destroy()
                                           
    if(method == 'l'):return login()
    elif(method == 'r'):return register()
    elif(method == 'ret'):return ret()
    elif(method == 'rm'):return register_med()
    elif(method == 'rp'): return register_patient()
    elif(method == 'rl'): return register_lab()

    conn.commit()
    cursor.close()
    conn.close()

########################################################################################################################################################
########################################################################################################################################################
def handle_login():
    user = userEntry.get()
    pwd = passEntry.get()
    s = database_handle('l', user, pwd)
    if s == '1':   
        main_page()   
    else:
        messagebox.showerror("Login Failed", "Invalid username or password.")

def handle_register():
    user = userEntry.get()
    pwd = passEntry.get()
    repw = reEntry.get()

    if user.strip() != "" and pwd.strip() != "" :
        if pwd == repw:
            database_handle('r',user, pwd)
            main_page()
        else:
            messagebox.showerror("Registration Error", "Password not matching in confirmation")
    else:
        messagebox.showerror("Registration Error", "Username or password cannot be empty")

def register_mode():
    global loginB, registerB, reEntry

    user = userEntry.get()
    pwd = passEntry.get()

    reLabel = Label(l_frame, text="Confim Pass", font=("Courier New",18),bg="white",fg="blue").place(x=230,y=250)
    reEntry = Entry(l_frame, font=("Courier New",20) ,textvariable = reEntry, width=16, show="*",bg="white",fg='blue')
    reEntry.place(x=360,y=245)

    cLabel =  Label(l_frame,fg='blue',bg="white",text="Click on the register button to register new account",font=("Courier New",13)).place(x=230,y=290)

    loginB.place(x=355,y=1000,height=40)
    registerB.place(x=423,y=1000,height=40)

    registerB2 = Button(l_frame,text="Register",font=('Calabri',15),width=7,command = handle_register,bg="white")
    registerB2.place(x=410,y=310,height=40)

def lab_result_display(name, age, iD):
    global tname, lid, lab_tk

    r_tk = Toplevel()
    r_tk.geometry("600x850")  
    r_tk.title("Lab Request")
    r_tk.config(bg="#26A69A")

    r_frame = Frame(r_tk, width=580, height=830, bg="white")
    r_frame.place(x=10, y=10)

    Label(r_frame, text="LAB RESULTS", bg="white", fg="blue", font=("Courier New", 20, "bold")).place(x=200, y=20)

    Label(r_frame, text="PATIENT NAME:", bg="white", fg="blue", font=("Courier New", 14)).place(x=30, y=80)
    Label(r_frame, text="REQUEST ID:", bg="white", fg="blue", font=("Courier New", 14)).place(x=30, y=130)
    Label(r_frame, text="TEST REQUEST:", bg="white", fg="blue", font=("Courier New", 14)).place(x=30, y=180)

    Label(r_frame, text=name, bg="white", fg="black", font=("Courier New", 14)).place(x=250, y=80)
    Label(r_frame, text=age, bg="white", fg="black", font=("Courier New", 14)).place(x=250, y=130)
    Label(r_frame, text=lid, bg="white", fg="black", font=("Courier New", 14)).place(x=250, y=180)

    note_box = Text(r_frame, width=65, height=28, bg="white", fg="black", font=("Courier New", 12))
    note_box.place(x=30, y=240)
    
    check = database_handle('ret', '*', 'patients')
    l_id = ""
    for i in check:
        if i[1]==name:
            l_id=i[5]

    lab = database_handle('ret','*','labs')
    loc=""
    date =""
    admin=""
    for i in lab:
        if i[0]==l_id:
            loc=i[1]
            date=str(i[2])
            admin=i[3]
            
    text = ""
    with open(f'/Users/sanjayumaganesh/Desktop/Pharmacy Management/material/assests/{loc}.txt', 'r') as desc:
        text = desc.read()
        text = text.replace("[date]", date)
        text = text.replace("[Your Name]", admin)
        
    note_box.insert(END,text)
    Button(r_frame, text="CONFIRM RESULT", font=('Courier New', 14), fg="blue", width=55, height=2).place(x=20, y=680)
    Button(r_frame, text="CANCEL", font=('Courier New', 14), fg="#941e1e", width=55, height=2).place(x=20, y=740)
    

def lab_register_display(name, age, iD):
    
    check = database_handle('ret', '*', 'patients')
    patient_request_check = ""
    for i in check:
        if i[1]==name:
            print(i)
            if i[5]==None:
                global tname, lid, lab_tk
                lab_tk = Toplevel()
                lab_tk.geometry("400x800")
                lab_tk.title("Lab Request")
                lab_tk.config(bg="#26A69A")

                result = database_handle('ret', 'L_ID', 'labs')
                prev_id = list(result[-1])
                lid = prev_id[0] + 1
                
                tname = StringVar()
                descLoc = ""
                date = datetime.now().strftime("[%Y/%m/%d]")

                options = [
                    "Hematology Panel",
                    "Biochemistry Metabolic Panel",
                    "Urine and Stool Analysis",
                    "Hormonal and Thyroid Panel"
                ]

                description_text = ""
                lab_frame = Frame(lab_tk, width=380, height=780, bg="white")
                lab_frame.place(x=10, y=10)

                Label(lab_frame, text="LAB REQUEST FORM", bg="white", fg="blue", font=("Courier New", 18)).place(x=100, y=20)
                Label(lab_frame, text="PATIENT NAME:", bg="white", fg="blue", font=("Courier New", 14)).place(x=20, y=70)
                Label(lab_frame, text="PATIENT AGE:", bg="white", fg="blue", font=("Courier New", 14)).place(x=20, y=120)
                Label(lab_frame, text="REQUEST ID:", bg="white", fg="blue", font=("Courier New", 14)).place(x=20, y=170)
                Label(lab_frame, text="TEST REQUEST:", bg="white", fg="blue", font=("Courier New", 14)).place(x=20, y=220)

                Label(lab_frame, text=name, bg="white", fg="blue", font=("Courier New", 14)).place(x=250, y=70)
                Label(lab_frame, text=age, bg="white", fg="blue", font=("Courier New", 14)).place(x=250, y=120)
                Label(lab_frame, text=lid, bg="white", fg="blue", font=("Courier New", 14)).place(x=250, y=170)

                tType = ttk.Combobox(lab_frame, values=options, width=14, textvariable=tname)
                tType.set("Select Test Category")
                tType.place(x=220, y=220)

                note_box = Text(lab_frame, width=55, height=30, bg="white", fg="black", font=("Courier New", 10))
                note_box.place(x=20, y=270)
                note_box.insert(END, description_text)


                note_box.insert(END, description_text)
                def update_description(event):
                    
                    selected_test = tname.get()
                    print(selected_test)
                    description_text = ""
                    if selected_test in options:
                        try:
                            with open(f'/Users/sanjayumaganesh/Desktop/Pharmacy Management/material/assests/{selected_test}.txt', 'r') as desc:
                                description_text = desc.read()
                                
                        except FileNotFoundError:
                            description_text = "Description file not found for the selected test."

                    description_text = description_text.replace("[date]", date)
                    description_text = description_text.replace("[Your Name]", userEntry.get())
                    
                    note_box.delete(1.0, END)
                    note_box.insert(END, description_text)
                    
                tType.bind("<<ComboboxSelected>>", update_description)

                Button(lab_frame, text="SEND REQUEST", font=('Courier New', 14),command=lambda:database_handle('rl',name), fg="blue", width=33, height=2).place(x=20, y=640)
                Button(lab_frame, text="CANCEL REQUEST", font=('Courier New', 14), fg="#941e1e", width=33, height=2,command=lambda:lab_tk.destroy()).place(x=20, y=700)
                
            else:
                messagebox.showerror("Registration error", "Previous Lab Request Pending")

def inventory_frame (frame_name,name, iD, price, company, typ, qty,row):
        
    f = Frame(frame_name, width=600, bg="white", height=150,)
    f.grid(row=row, column=0, sticky='NSEW', padx=10, pady=10)

    Label(f, text="MED NAME: ", font=('Courier New', 20),fg='blue', bg='white').place(x=10,y=10)
    Label(f, text=name, font=('Courier New', 20),fg='blue', bg='white').place(x=160,y=10)


    Label(f, text="MED ID: ", font=('Courier New', 14),fg='black', bg='white').place(x=10,y=40)
    Label(f, text=iD, font=('Courier New', 14),fg='black', bg='white').place(x=160,y=40)

    Label(f, text="MED PRICE: ", font=('Courier New', 14),fg='black', bg='white').place(x=10,y=60)
    Label(f, text=price, font=('Courier New', 14),fg='black', bg='white').place(x=160,y=60)

    Label(f, text="MANUFACTURER: ", font=('Courier New', 14),fg='black', bg='white').place(x=10,y=80)
    Label(f, text=company, font=('Courier New', 14), fg='black', bg='white').place(x=160,y=80)

    Label(f, text="MED TYPE: ", font=('Courier New', 14),fg='black', bg='white').place(x=10,y=100)
    Label(f, text=typ, font=('Courier New', 14), fg='black', bg='white').place(x=160,y=100)

    Button(f, text='−', font=('Courier New', 14), width=3,height=2).place(x=350,y=10)
    
    T = Text(f, width=12, height=2, bg="black", fg="white",font=("Courier New",15))
    T.place(x=412, y=10)
    T.insert(END, qty)
    
    Button(f, text='+', font=('Courier New', 14), width=3,height=2).place(x=500,y=10)
   


def patient_frame (iD, name, age, picture, gender, lid, oid, row):
        
    f = Frame(sf5, width=600, bg="white", height=200)
    f.grid(row=row, column=0, sticky='NSEW', padx=10, pady=10)

    Label(f, text="PATIENT NAME: ", font=('Courier New', 20),fg='blue', bg='white').place(x=10,y=10)
    Label(f, text=name, font=('Courier New', 20),fg='blue', bg='white').place(x=180,y=10)


    Label(f, text="PATIENT ID: ", font=('Courier New', 14),fg='black', bg='white').place(x=10,y=40)
    Label(f, text=iD, font=('Courier New', 14),fg='black', bg='white').place(x=180,y=40)

    Label(f, text="PATIENT GENDER: ", font=('Courier New', 14),fg='black', bg='white').place(x=10,y=60)
    Label(f, text=gender, font=('Courier New', 14),fg='black', bg='white').place(x=180,y=60)

    Label(f, text="LAB ID: ", font=('Courier New', 14),fg='black', bg='white').place(x=10,y=80)
    Label(f, text=lid, font=('Courier New', 14), fg='black', bg='white').place(x=180,y=80)

    Label(f, text="ORDER ID: ", font=('Courier New', 14),fg='black', bg='white').place(x=10,y=100)
    Label(f, text=oid, font=('Courier New', 14), fg='black', bg='white').place(x=180,y=100)

    Button(f,text='SHOW LAB REPORT',font=('Courier New', 12), width=11,height=2, command = lambda: lab_result_display(name,age,iD)).place(x=10,y=130)
    Button(f,text='SEND LAB REQUEST',font=('Courier New', 12), width=11,height=2, command = lambda: lab_register_display(name,age,iD)).place(x=150,y=130)

    pimg = Image.open(picture)
    pimg = pimg.resize((100, 100))
    pimgTk = ImageTk.PhotoImage(pimg)
    image_label = Label(f, image=pimgTk)
    image_label.image = pimgTk
    image_label.place(x=450,y=30)



def med_display():
    f1.tkraise()
    medicines = database_handle('ret','*','medicine')
    for i in medicines:
           inventory_frame(sf1,i[1],i[0],i[4],i[3],i[2],i[5],medicines.index(i)*10)

def patient_display():
    f5.tkraise()
    patients = database_handle('ret','*','patients')
    for i in patients:
           patient_frame(i[0], i[1], i[2], i[3], i[4], i[5], i[6], patients.index(i)*10)
        
def order_display():
    f7.tkraise()
    medicines = database_handle('ret','*','medicine')
    for i in medicines:
           inventory_frame(sf7,i[1],i[0],i[4],i[3],i[2],i[5],medicines.index(i)*10)

           
def select_image():
    global img_tk,pp
    pp = filedialog.askopenfilename(
        title="Select a Picture",
        filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp *.gif")]
    )
    if pp:
        img = Image.open(pp)
        img = img.resize((100, 100))
        img_tk = ImageTk.PhotoImage(img)

        image_label.config(image=img_tk)
        image_label.image = img_tk


########################################################################################################################################################
##MAIN PAGE##
########################################################################################################################################################


def main_page():
    global mn, mt, mc, mp, mq
    global f1,f5,sf1,sf5,f7,sf7
    global pn,pa,pg,image_label,pp

    mainframe = Toplevel()
    mainframe.title('Henrys Pharma')
    mainframe.geometry('960x700')
    mainframe.configure(bg="#26A69A")

    mn = StringVar()
    mt = StringVar()
    mc = StringVar()
    mp = StringVar()
    mq = StringVar()

    pn = StringVar()
    pa = StringVar()
    pg = StringVar()
    pp = "/Users/sanjayumaganesh/Desktop/Pharmacy Management/material/assests/placeholder.jpg"

    oa = StringVar()
    ostr = StringVar()
    oc = StringVar()

    tn = StringVar()
    tn = StringVar()

    Label(mainframe,text="HENRY'S PHARMACY",font=('Consolas',50),bg="#26A69A",fg="white",width=30,anchor='w').place(x=5,y=10)
    Label(mainframe,text = 'Hi ' + userEntry.get(),font=('Consolas',30),bg="#26A69A",fg="white",anchor='e').place(x=800,y=10)
    Button(mainframe,text = "LOG OUT",font=('Consolas',10),bg="#26A69A",width=10).place(x=800,y=50)
    
########################################################################################################################################################
    
    f1 = LabelFrame(mainframe,bg='white',height=553,width=650,text="INVENTORY",fg="#2196F3",font=('Consolas',30),highlightbackground="black", highlightthickness=10)
    f1.place(x=300,y=100)

    c1 = Canvas(f1, width=620, height=505, bg='white', scrollregion=(0,0,500,500))
    bar1 = Scrollbar(f1,orient=VERTICAL,command=c1.yview)
    sf1 = Frame(c1)

    sf1.bind(
        "<Configure>",
        lambda e: c1.configure(
            scrollregion=c1.bbox("all")))

    c1.create_window((0, 0), window = sf1, anchor = NW)
    c1.configure(yscrollcommand = bar1.set)

    c1.grid(row = 0, column = 0, sticky = NSEW)
    bar1.grid(row = 0, column = 1, sticky = NS)

######################################################################################################################################################## 

    f2 =  LabelFrame(mainframe,bg='white',height=560,width=645,text="REGISTER PATIENT",fg="#2196F3",highlightbackground="black", highlightthickness=10,font=('Consolas',30))
    f2.place(x=300,y=100)

    ff2=Frame(f2,bg='white',height=350,width=600,highlightbackground="black", highlightthickness=2)
    ff2.place(x=10,y=20)

    Label(ff2, text="PATIENT NAME: ", font=('Courier New', 18),fg='blue', bg='white').place(x=10,y=20)
    Label(ff2, text="PATIENT AGE: ", font=('Courier New', 18),fg='blue', bg='white').place(x=10,y=70)
    Label(ff2, text="PATIENT GENDER: ", font=('Courier New', 18),fg='blue', bg='white').place(x=10,y=120)
    Label(ff2, text="PATIENT PICTURE: ", font=('Courier New', 18),fg='blue', bg='white').place(x=10,y=170)
    
    pnE = Entry(ff2,textvariable = pn,width=20,font=('Courier New', 14),fg='blue', bg='white')
    pnE.place(x=400,y=20)

    ageE = Entry(ff2,textvariable = pa,width=20,font=('Courier New', 14),fg='blue', bg='white')
    ageE.place(x=400,y=70)

    genE = ttk.Combobox(ff2, values=['Male','Female','Other'],width=18, textvariable = pg)
    genE.set("Select Patient's Gender")
    genE.place(x=400,y=120)

    placeholder = Image.open(pp)
    placeholder = placeholder.resize((100, 100))
    placeholder_tk = ImageTk.PhotoImage(placeholder)
    image_label = Label(ff2, image=placeholder_tk)
    image_label.image = placeholder_tk
    image_label.place(x=480,y=170)

    Button(ff2,text="Select Image",font=('Courier New',14),bg="white",width=15,height=2,command=select_image).place(x=10,y=200)

    Button(ff2,text="Register",font=('Courier New',14),bg="white",width=60,height=3,command=lambda:database_handle('rp')).place(x=10,y=280)
    
########################################################################################################################################################
    f3 =  LabelFrame(mainframe,bg='white',height=553,width=650,text="LAB ",fg="#2196F3",highlightbackground="black", highlightthickness=10,font=('Consolas',30))
    f3.place(x=300,y=100)
########################################################################################################################################################
    f4 =  LabelFrame(mainframe,bg='white',height=553,width=650,text="ORDER LIST",fg="#2196F3",highlightbackground="black", highlightthickness=10,font=('Consolas',30))
    f4.place(x=300,y=100)
########################################################################################################################################################
    
    f5 =  LabelFrame(mainframe,bg='white',height=553,width=650,text="PATIENT LIST ",fg="#2196F3",highlightbackground="black", highlightthickness=10,font=('Consolas',30))
    f5.place(x=300,y=100)

    c5 = Canvas(f5, width=620, height=505, bg='white', scrollregion=(0,0,500,500))
    bar5 = Scrollbar(f5,orient=VERTICAL,command=c5.yview)
    sf5= Frame(c5)

    sf5.bind(
        "<Configure>",
        lambda e: c5.configure(
            scrollregion=c5.bbox("all")))

    c5.create_window((0, 0), window = sf5, anchor = NW)
    c5.configure(yscrollcommand = bar5.set)

    c5.grid(row = 0, column = 0, sticky = NSEW)
    bar5.grid(row = 0, column = 1, sticky = NS)
    
########################################################################################################################################################
    f6 =  LabelFrame(mainframe,bg='white',height=553,width=650,text="REGISTER ORDER",fg="#2196F3",highlightbackground="black", highlightthickness=10,font=('Consolas',30))
    f6.place(x=300,y=100)
    
########################################################################################################################################################    
    f7 = LabelFrame(mainframe, bg='white', height=553, width=650, text="REGISTER ORDER",  fg="#2196F3", font=('Consolas', 30), highlightbackground="black", highlightthickness=10)
    f7.place(x=300, y=100)

    ff7=Frame(f7,bg='white',height=150,width=600,highlightbackground="black", highlightthickness=2)
    ff7.place(x=10,y=20)
    
    Label(ff7, text="PATIENT NAME: ", font=('Courier New', 18),fg='blue', bg='white').place(x=10,y=10)
    Label(ff7, text="PATIENT AGE: ", font=('Courier New', 18),fg='blue', bg='white').place(x=10,y=70)
    Label(ff7, text="PATIENT GENDER: ", font=('Courier New', 18),fg='blue', bg='white').place(x=10,y=120)

    canvas_width = 600
    canvas_height = 276

    c7 = Canvas(f7, width=canvas_width, height=canvas_height, bg='white')
    bar7 = Scrollbar(f7, orient=VERTICAL, command=c7.yview)

    sf7 = Frame(c7, bg='white')
    sf7.bind(
        "<Configure>",
        lambda e: c7.configure(
            scrollregion=c7.bbox("all"))
    )

    c7.create_window((0, 0), window=sf7, anchor=NW)
    c7.configure(yscrollcommand=bar7.set)
    c7.place(x=10, y=200)
    bar7.place(x=610, y=200, height=canvas_height)

########################################################################################################################################################

    f8 =  LabelFrame(mainframe,bg='white',height=553,width=650,text="REGISTER MED",fg="#2196F3",highlightbackground="black", highlightthickness=10,font=('Consolas',30))
    f8.place(x=300,y=100)

    ff8=Frame(f8,bg='white',height=350,width=600,highlightbackground="black", highlightthickness=2)
    ff8.place(x=10,y=20)

    Label(ff8, text="MED NAME: ",font=('Courier New', 18),fg='blue', bg='white').place(x=10,y=20)
    Label(ff8, text="MED TYPE: ",font=('Courier New', 18),fg='blue', bg='white').place(x=10,y=70)
    Label(ff8, text="MANUFACTURER: ",font=('Courier New', 18),fg='blue', bg='white').place(x=10,y=120)
    Label(ff8, text="PRICE: ",font=('Courier New', 18),fg='blue', bg='white').place(x=10,y=170)
    Label(ff8, text="QUANTITY: ",font=('Courier New', 18),fg='blue', bg='white').place(x=10,y=220)

    mnE = Entry(ff8, width=20, font=('Courier New', 14), fg='blue', bg='white', textvariable=mn)
    mnE.place(x=400, y=20)

    mcE = Entry(ff8, textvariable = mc, width=20, font=('Courier New', 14) ,fg='blue', bg='white')
    mcE.place(x=400,y=120)

    mtE = ttk.Combobox(ff8, values=['Tablet','Drop','Tonic'],width=18,background="pink", textvariable = mt)
    mtE.set("Select Medicine Type")
    mtE.place(x=400,y=70)

    mpE = Entry(ff8,width=20,font=('Courier New', 14),fg='blue', bg='white', textvariable = mp)
    mpE.place(x=400,y=170)

    mqE = Entry(ff8,width=20,font=('Courier New', 14),fg='blue', bg='white', textvariable = mq)
    mqE.place(x=400,y=220)

    Button(ff8,text="Register",font=('Courier New',14),bg="white",width=60,height=3,command= lambda: database_handle('rm')).place(x=10,y=280)

########################################################################################################################################################
    b1= Button(mainframe,text='INVENTORY',width=10,height=3,command= med_display).place(x=10,y= 100)
    b2= Button(mainframe,text='REGISTER PATIENT',width=10,height=3,command= lambda:f2.tkraise()).place(x=10,y= 300)
    b3= Button(mainframe,text='LAB',width=10,height=3,command= lambda:f3.tkraise()).place(x=160,y= 100)
    b4= Button(mainframe,text='ORDERS LIST',width=10,height=3,command= lambda:f4.tkraise()).place(x=160,y= 200)
    b5= Button(mainframe,text='PATIENT LIST',width=10,height=3,command= patient_display).place(x=10,y= 200)
    b6= Button(mainframe,text='REGISTER ORDER',width=10,height=3,command= lambda:f6.tkraise()).place(x=160,y= 300)
    b7= Button(mainframe,text='REGISTER MED',width=10,height=3,command= lambda:f8.tkraise()).place(x=10,y= 400)
    b8= Button(mainframe,text='EXTRA',width=10,height=3,command= order_display).place(x=160,y= 400)

########################################################################################################################################################
########################################################################################################################################################
    
userE = StringVar()
passE = StringVar()
reEntry=StringVar()

l_frame = Frame(lP,width=500,height=300,bg="white",highlightbackground="black", highlightthickness=2).place(x=200,y=60)

mainL = Label(l_frame,text="WELCOME TO HENRY'S PHARMA",font=("Courier New",30),bg="white",fg="blue",).place(x=230,y=80)

Label(l_frame,text="Username",font=("Courier New",18),bg="white",fg="blue").place(x=240,y=150)
Label(l_frame,text="Password",font=("Courier New",18),bg="white",fg="blue").place(x=240,y=200)

userEntry = Entry(l_frame,font=("Courier New",20), textvariable = userE, width=16,bg="white",fg="blue")
userEntry.place(x=360,y=150)

passEntry = Entry(l_frame,font=("Courier New",20), textvariable = passE, width=16,show="*",bg="white",fg='blue')
passEntry.place(x=360,y=200)

loginB = Button(l_frame,text="Login",font=('Calabri',15),width=7,command=handle_login,bg="white")
loginB.place(x=355,y=290,height=40)

registerB = Button(l_frame,text="Register",font=('Calabri',15),width=7,command=register_mode,bg="white")
registerB.place(x=473,y=290,height=40)

lP.mainloop()
