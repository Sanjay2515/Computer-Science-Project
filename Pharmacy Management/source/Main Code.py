import os
from datetime import datetime
from tkinter import *
from tkinter import filedialog, messagebox, ttk

import mysql.connector
from PIL import Image, ImageTk

lP = Tk()
lP.title("Login")
lP.geometry('600x350')
lP.configure(bg="#26A69A")

descLoc = None
lid = None
pCombo = None
qCombo = None
mCombo = None

pol = []
mol=[]
qol = 0

row = 1
order_map = {}


def database_handle(method,vara=None,varb=None,varc=None,vard=None):
    global loginB,registerB,reEntry
    global mn, mt, mc, mp, mq
    global pn ,pa ,pg, pp
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
    
    def ret_a():    
        cursor.execute(f"SELECT {vara} from {varb} where {varc} = {vard}")
        result=cursor.fetchall()
        return(result)
    
        
    def register_med():
        cursor.execute("SELECT M_ID FROM medicine")
        result=cursor.fetchall()
        if mn.get().strip() != "" and mt.get().strip() != "" and mc.get().strip() != "" and mp.get().strip() != "" and mq.get().strip() != "":

            if mt.get() != "Select Medicine Type":

                prev_id = list(result[-1])
                new_id = prev_id[0]+1
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
        global pp
        cursor.execute('SELECT P_ID from patients order by P_ID')
        result=cursor.fetchall()
        prev_id = list(result[-1])
        new_id = prev_id[0]+1
        
        if pn.get().strip()!='' and pa.get().strip()!='' and pg.get().strip()!='' and pp !='/Users/sanjayumaganesh/Desktop/Pharmacy Management/material/assests/placeholder.jpg':
            if pg != "Select Patient's Gender ":
                cursor.execute(f'INSERT INTO patients(P_ID, P_NAME, P_AGE, P_PICTURE,P_GENDER,L_ID,O_ID) VALUES({new_id},"{pn.get()}","{pa.get()}","{pp}","{pg.get()}",NULL,NULL)')
                conn.commit()
                messagebox.showinfo("Registration complete", "New patient registered")
                
                pn.set("")
                pa.set("")
                pg.set("Select Patient's Gender")
                pp = "/Users/sanjayumaganesh/Desktop/Pharmacy Management/material/assests/placeholder.jpg"
                
            else:
                messagebox.showerror("Registration error", "Select patients gender")
        else:
            messagebox.showerror("Registration error", "Field cannot be empty")

    def register_lab():
        global lab_tk, lid
        
        if tname.get() != "Select Test Category" and tname.get().strip() != "" :
            date = datetime.now().strftime("%Y-%m-%d")
            cursor.execute(f'INSERT INTO labs (L_ID, TEST_NAME, DATE, Manager_name) VALUES ({lid},"{tname.get()}","{date}","{userEntry.get()}")')
            cursor.execute(f"UPDATE patients SET L_ID = {lid} WHERE P_NAME = '{vara}'")
            conn.commit()
            messagebox.showinfo("Request", "Request Sent")
            lab_tk.destroy()
            
    def register_order():
        cursor.execute(f'INSERT INTO orders (O_ID,O_STRING,O_COST) VALUES ("{vara}","{varb}",{varc})')
        conn.commit()
        messagebox.showinfo("Order", "Order placed successfully")
            
            
    def renounce():
        if vara == 'cancelOrder67':
            cursor.execute(f'DELETE FROM orders WHERE O_ID = {varb}')
            conn.commit()
            messagebox.showinfo("Order cancelation","Order Cancelled")
        else:
            cursor.execute(f"UPDATE medicine SET M_QUANTITY = {vara} WHERE M_NAME = {varb}")
            conn.commit()
            cursor.execute(f'DELETE FROM orders WHERE O_ID = {varc}')
            conn.commit()
            messagebox.showinfo("Confirmation","Order Shipped Succuccesfully")

        
            
    def clear_lab():

        conn.commit()
        cursor.execute(f'DELETE FROM labs WHERE L_ID = {vara}')
        conn.commit()
        messagebox.showinfo("Confirmation","Lab Report confirmed")

        
            
        
    if(method == 'l'):return login()
    elif(method == 'r'):return register()
    elif(method == 'ret'):return ret()
    elif(method == 'rm'):return register_med()
    elif(method == 'rp'): return register_patient()
    elif(method == 'rl'): return register_lab()
    elif(method == 'cl'): return clear_lab()
    elif(method == 'rq'): return ret_a()
    elif(method == 'ro'): return register_order()
    elif(method == 'ren'):return renounce()
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
        lP.withdraw()
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
        
    lP.withdraw()

def register_mode():
    global loginB, registerB
    global reEntry, reLabel, cLabel, cancelB, registerB2   

    user = userEntry.get()
    pwd = passEntry.get()

    reLabel = Label(
        l_frame, text="Confirm Pass",
        font=("Courier New",18), bg="white", fg="blue"
    )
    reLabel.place(x=120, y=215)
    
    reEntry = Entry(
        l_frame, font=("Courier New",20), width=16, show="*",
        bg="white", fg='blue'
    )
    reEntry.place(x=250, y=215)

    cLabel = Label(
        l_frame, fg='blue', bg="white",
        text="Click on the register button to register new account",
        font=("Courier New",13)
    )
    cLabel.place(x=100, y=260)

    loginB.place(x=355, y=1000, height=40)
    registerB.place(x=423, y=1000, height=40)

    registerB2 = Button(
        l_frame, text="Register", font=('Calabri', 15),
        width=7, command=handle_register, bg="white"
    )
    registerB2.place(x=370, y=280, height=30)

    def cancel():
        global cLabel, reEntry, reLabel, cancelB, registerB2

        loginB.place(x=245, y=260, height=40)
        registerB.place(x=363, y=260, height=40)

        cLabel.place(x=1000, y=1000)
        reLabel.place(x=1000, y=1000)
        reEntry.place(x=1000, y=1000)
        cancelB.place(x=1000, y=1000)
        registerB2.place(x=1000, y=1000)   

    cancelB = Button(
        l_frame, text="Cancel", font=('Calabri', 15),
        width=7, bg="white", command=cancel
    )
    cancelB.place(x=230, y=280, height=30)


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
    Label(r_frame, text="PATIENTS ID:", bg="white", fg="blue", font=("Courier New", 14)).place(x=30, y=130)
    Label(r_frame, text="REQUEST ID", bg="white", fg="blue", font=("Courier New", 14)).place(x=30, y=180)

    Label(r_frame, text=name, bg="white", fg="black", font=("Courier New", 14)).place(x=250, y=80)
    Label(r_frame, text=age, bg="white", fg="black", font=("Courier New", 14)).place(x=250, y=130)
    Label(r_frame, text=iD, bg="white", fg="black", font=("Courier New", 14)).place(x=250, y=180)

    note_box = Text(r_frame, width=65, height=28, bg="white", fg="black", font=("Courier New", 12))
    note_box.place(x=30, y=240)
    
    check = database_handle('ret', '*', 'patients')
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

    def del_rec():
        database_handle('cl',iD)
        r_tk.destroy()
        
    Button(r_frame, text="CONFIRM RESULT", font=('Courier New', 14), fg="blue", width=55, height=2,command = lambda:del_rec()).place(x=20, y=680)
    Button(r_frame, text="CANCEL", font=('Courier New', 14), fg="#941e1e", width=55, height=2,command = lambda: r_tk.destroy()).place(x=20, y=740)
    

def lab_register_display(name, age, iD):
    
    check = database_handle('ret', '*', 'patients')
    patient_request_check = ""
    for i in check:
        if i[1]==name:
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

                Label(lab_frame, text=name, bg="white", fg="blue", font=("Courier New", 14)).place(x=250, y=70)
                Label(lab_frame, text=age, bg="white", fg="blue", font=("Courier New", 14)).place(x=250, y=120)

                tType = ttk.Combobox(lab_frame, values=options, width=14, textvariable=tname)
                tType.set("Select Test Category")
                tType.place(x=220, y=220)

                note_box = Text(lab_frame, width=55, height=30, bg="white", fg="black", font=("Courier New", 10))
                note_box.place(x=20, y=270)
                note_box.insert(END, description_text)


                note_box.insert(END, description_text)
                def update_description(event):
                    
                    selected_test = tname.get()
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

    
    T = Text(f, width=12, height=2, bg="black", fg="white",font=("Courier New",15))
    T.place(x=412, y=10)
    T.insert(END, qty)
    
   


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


    def handle_lab_pull():
        if lid == None:
            messagebox.showerror("Lab Request", "No Lab Requested for this patients")
        else:
            lab_result_display(name,age,lid)
        
    Button(f,text='SHOW LAB REPORT',font=('Courier New', 12), width=11,height=2, command = handle_lab_pull).place(x=10,y=130)
    Button(f,text='SEND LAB REQUEST',font=('Courier New', 12), width=11,height=2, command = lambda: lab_register_display(name,age,iD)).place(x=150,y=130)

    pimg = Image.open(picture)
    pimg = pimg.resize((100, 100))
    pimgTk = ImageTk.PhotoImage(pimg)
    image_label = Label(f, image=pimgTk)
    image_label.image = pimgTk
    image_label.place(x=450,y=30)

def order_frame(frame_name, name, qty, cost,pname):
    global row
    global order_map

    cost = int(cost)
    qty_var = [int(qty)]  

    f = Frame(frame_name, width=570, bg="white", height=90)
    f.grid(row=row, column=0, sticky='NSEW', padx=10, pady=10)

    Label(f, text="MED NAME: ", font=('Courier New', 20), fg='blue', bg='white').place(x=10, y=10)
    Label(f, text=name, font=('Courier New', 20), fg='blue', bg='white').place(x=160, y=10)

    Label(f, text="PRICE: ", font=('Courier New', 14), fg='black', bg='white').place(x=10, y=40)

    qty_label = Label(f, text=f'-- Rs./{cost} x {qty_var[0]}', font=('Courier New', 14), fg='black', bg='white')
    qty_label.place(x=160, y=40)

    total_label = Label(f, text=f'-- Rs./{cost * qty_var[0]}', font=('Courier New', 14), fg='black', bg='white')
    total_label.place(x=160, y=60)

    T = Text(f, width=10, height=1, bg="black", fg="white", font=("Courier New", 15))
    T.place(x=412, y=10)
    T.insert(END, qty_var[0])
    
    def delete():
        global row
        f.grid_forget()
        order_map[pname].pop(name)
        
        
    def edit(func):
        if func == 0:
            if qty_var[0] < 20:
                qty_var[0] += 1
        elif func == 1 and qty_var[0] > 0:
            qty_var[0] -= 1
        order_map[pname][name] = qty_var[0]
            
        T.delete("1.0", END)
        T.insert(END, qty_var[0])

        qty_label.config(text=f'-- Rs./{cost} x {qty_var[0]}')
        total_label.config(text=f'-- Rs./{cost * qty_var[0]}')

    Button(f, text='−', font=('Courier New', 14), width=3, height=1, command=lambda: edit(1)).place(x=350, y=9)
    Button(f, text='+', font=('Courier New', 14), width=3, height=1, command=lambda: edit(0)).place(x=500, y=9)

    Button(f, text='DELETE FROM CART', fg="red", bg="white", font=('Courier New', 12), width=22, height=1,command = lambda:delete()).place(x=353, y=45)

#DEALS WITH ORDER PAGE
def order_handle():
    global order_map,sf7,row
    
    patient = cart_p.get()
    med = '"'+cart_m.get()+'"'
    qty = cart_q.get()
    qty = int(qty)
    price = database_handle('rq', 'M_PRICE','medicine','M_NAME',med)
    
    if patient not in order_map:
        order_map[patient] = {}
        
    if med != "Select Medicine" and med not in order_map[patient]:
        if qty != 0 or 0 < qty < 20 :
            
            cd = order_map[patient]
            nmed = med.strip('"')
            cd.update({nmed:qty})
            order_map.update({patient:cd})
            messagebox.showinfo("Cart Updated", "Medication added to cart")
            cart_m.set("Select Medicine")
            cart_q.set(0)
            order_frame(sf7,med,qty,price[0][0],patient)
            row+=1


        else:
            messagebox.showerror("Invalid quantity", "Quantity can not be 0 or more than 20")
    else:
        if med in order_map[patient]:
            messagebox.showerror("Cannot add", "Medication already in cart")
        else:    
            messagebox.showerror("Invalid Medication", "No Medication Selected")
        
    

#DEALS WITH BILLING POP UP
def billing():
    global sf7
    
    if len(order_map)!= 0:
        
        tC = 0
        items = 0
        names = []
        for name,lis in order_map.items():
            names.append(name)
            for i,f in lis.items():
                items = items + f
                i = '"'+i+'"'
                price = database_handle('rq', 'M_PRICE','medicine','M_NAME',i)
                mC = price[0][0]*f
                tC = tC+mC
        tC = 120 + tC + (18/100 * tC)
        oStr = names[0]+"->"+str(order_map[names[0]])
        id_ret = database_handle('ret','O_ID','orders')
        try:
            prev_id = list(id_ret[-1])
            new_id = prev_id[0] + 1
        except:
            new_id = 1
        
        bill_tk = Toplevel()
        bill_tk.geometry("420x400")
        bill_tk.title("Confirm order")
        bill_tk.configure(bg="#26A69A")

        f = Frame(bill_tk,width=400,height=380,bg="white",highlightbackground="black", highlightthickness=2)
        f.place(x=10,y=10)

        Label(f,text="Patient Name:",font=("Courier New",20),bg="white",fg="Blue").place(x=15,y=30)
        Label(f,text="No of items:",font=("Courier New",20),bg="white",fg="Blue").place(x=15,y=70)
        Label(f,text="GST tax %:",font=("Courier New",20),bg="white",fg="Blue").place(x=15,y=110)
        Label(f,text="Delivery Charge:",font=("Courier New",20),bg="white",fg="Blue").place(x=15,y=150)
        Label(f,text="Total cost:",font=("Courier New",20),bg="white",fg="Blue").place(x=15,y=190)

        Label(f,text=names[0],font=("Courier New",20),bg="white",fg="Blue").place(x=200,y=30)
        Label(f,text=items,font=("Courier New",20),bg="white",fg="Blue").place(x=200,y=70)
        Label(f,text="18%",font=("Courier New",20),bg="white",fg="Blue").place(x=200,y=110)
        Label(f,text="Rs./120",font=("Courier New",20),bg="white",fg="Blue").place(x=200,y=150)
        Label(f,text=tC,font=("Courier New",20),bg="white",fg="Blue").place(x=200,y=190)

        def bill_integrate():
            database_handle("ro",new_id,oStr,tC)
            bill_tk.destroy()
            for i in sf7.winfo_children():
                i.destroy()

            
        Button(f, text="PLACE ORDER", font=('Courier New', 14), fg="blue", width=39, height=2,command = lambda:bill_integrate()).place(x=18, y=280)
        Button(f, text="CANCEL", font=('Courier New', 14), fg="#941e1e", width=39, height=2,command = lambda: bill_tk.destroy()).place(x=18, y=320)
            
    else:
        messagebox.showerror("Cart empty", "No Medication In Cart")

def godfather(handlerList=None,cancel = False):
    global tV
   
    selected = tV.focus()  # Get ID of selected row
    row = tV.item(selected, "values")
    
    iD = row[0]
    result = database_handle('rq','O_STRING','orders','O_ID',iD)
    result = result[0][0].split('->')
    fl = result[1].strip("{").strip('}').split(':')
    
    if cancel==True:
        selected_order = tV.selection()[0]
        tV.delete(selected_order)
        database_handle('ren',"cancelOrder67",int(row[0]))
        
    else:
        target = database_handle('rq','M_QUANTITY','medicine','M_NAME',fl[0])
        new_qty = target[0][0] - int(fl[1])
        
        selected_order = tV.selection()[0]
        tV.delete(selected_order)

        database_handle('ren',new_qty,fl[0],int(row[0]))
    
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

    
def select_image():
    global img_tk, pp
    
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

def logout():
    global mainframe
    
    lP.deiconify()
    mainframe.destroy()
    userE.set("")
    passE.set("")

    
########################################################################################################################################################
## MAIN PAGE ##
########################################################################################################################################################


def main_page():
    global tV
    global mn, mt, mc, mp, mq
    global f1,f5,sf1,sf5,f7,sf7
    global pn,pa,pg,image_label,pp
    global pco,mco,qco,pCombo,mCombo,qCombo,sel_mname
    global cart_p,cart_m,cart_q
    global mainframe
    
    
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

    pco = StringVar()
    mco = StringVar()
    qco = StringVar()

    cart_p = StringVar()
    cart_m = StringVar()
    cart_q = StringVar()

    Label(mainframe,text="PHARMACY MANAGEMENT SYSTEM",font=('Courier New',50,"bold"),bg="#26A69A",fg="white",width=30,anchor='w').place(x=5,y=20)
    Button(mainframe,text = "LOG OUT",font=('Consolas',10),bg="#26A69A",command=lambda:logout()).place(x=850,y=50,width=100,height=30)
    
########################################################################################################################################################
#INVENTORY FRAME  
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
#PATIENT REGISTER
    f2 =  LabelFrame(mainframe,bg='white',height=560,width=650,text="REGISTER PATIENT",fg="#2196F3",highlightbackground="black", highlightthickness=10,font=('Consolas',30))
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
    
############################################################################################################################################################################################

# PATIENT LIST

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
    
#######################################################################################################################################################################################################################################

#SHIP ORDERS
    
    f6 = LabelFrame(mainframe, bg='white', height=553, width=650, text="SHIP ORDERS",fg="#2196F3", font=('Consolas', 30),highlightbackground="black", highlightthickness=10)
    f6.place(x=300, y=100)
    
    tV = ttk.Treeview(f6, columns=("iD", "name"), show='headings')

    tV.tag_configure('whitebg', background='white', foreground='black')  
    tV.place(x=10, y=10, width=600, height=350)

    tV.heading("iD", text="Order Id")
    tV.heading("name", text="Customer name")
    
    tV.column("iD", width=10)
    tV.column("name", width=150)
    
    handlerData = []
    
    
    def update_tree():
        f6.tkraise()
        order_data = database_handle("ret","*",'orders')
        for i in order_data:
            if i not in handlerData:
                ordId = i[0]
                ostr = i[1].split('->')
                pdname = ostr[0]
                tV.insert("", "end", values=(ordId,pdname))
                handlerData.append(i)
        
    Button(f6,text="Ship out order",font=('Courier New',16),bg="#26A69A",width=55,height=2,command=lambda:godfather(handlerData)).place(x=10,y=380)
    Button(f6,text="Delete order",font=('Courier New',16),fg="red",width=55,height=2,command = lambda:godfather(cancel=True)).place(x=10,y=430)
    
#######################################################################################################################################################################################################################################

#REGISTER ORDERS

    f7 = LabelFrame(mainframe, bg='white', height=553, width=650, text="REGISTER ORDER",fg="#2196F3", font=('Consolas', 30),highlightbackground="black", highlightthickness=10)
    f7.place(x=300, y=100)

    ff7=Frame(f7,bg='white',height=200,width=600,highlightbackground="black", highlightthickness=2)
    ff7.place(x=10,y=20)
    
    Label(ff7, text="PATIENT NAME: ", font=('Courier New', 18),fg='blue', bg='white').place(x=10,y=10)
    Label(ff7, text="SELECT MED: ", font=('Courier New', 18),fg='blue', bg='white').place(x=10,y=50)
    Label(ff7, text="SELECT QUANTITY: ", font=('Courier New', 18),fg='blue', bg='white').place(x=10,y=90)
    
    pCombo = ttk.Combobox(ff7,state="readonly", values= pol,width=18,background="pink",textvariable = cart_p)
    pCombo.place(x=300,y=10)
    pCombo.set("Select Patient")
    
    mCombo = ttk.Combobox(ff7,state="readonly", values= mol,width=18,background="pink",textvariable = cart_m)
    mCombo.place(x=300,y=50)
    mCombo.set("Select Medicine")
    
    qCombo = Spinbox(ff7,from_=0, to=20, textvariable = cart_q)
    qCombo.place(x=300,y=90)

    Button(ff7,text="Add to cart",font=('Courier New',14),bg="white",width=20,height=2,command = lambda:order_handle()).place(x=300,y=140)
    Button(ff7,text="Proceed to billing",font=('Courier New',14),fg="#26A69A",width=20,height=2,command = lambda:billing()).place(x=10,y=140)

    medicines = database_handle('ret','M_NAME','medicine')
    patients = database_handle('ret','P_NAME','patients')
    for i in patients:
        pol.append(i[0])
    for i in medicines:
        mol.append(i[0])
        
    mCombo.config(values=mol)
    pCombo.config(values=pol)

    canvas_width = 590
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
    c7.place(x=10, y=250)
    bar7.place(x=610, y=200, height=canvas_height)

##################################################################################################################################################################################################################

# REGISTER MEDICATION

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

#MENU BUTTONS

    b1= Button(mainframe,text='MEDICINE STOCK',width=26,height=4,command= med_display).place(x=10,y= 100)
    b2= Button(mainframe,text='PATIENT REGISTER',width=26,height=4,command= lambda:f2.tkraise()).place(x=10,y= 400)
    b3= Button(mainframe,text='PATIENT DATA',width=26,height=4,command= patient_display).place(x=10,y= 300)
    b4= Button(mainframe,text='PENDING ORDERS',width=26,height=4,command= lambda:update_tree()).place(x=10,y= 600)
    b5= Button(mainframe,text='REGISTER MEDICINE',width=26,height=4,command= lambda:f8.tkraise()).place(x=10,y= 200)
    b6= Button(mainframe,text='PLACE ORDER',width=26,height=4,command= lambda:f7.tkraise()).place(x=10,y= 500)
    
########################################################################################################################################################
########################################################################################################################################################

#BASE LOGIN PAGE START
    
userE = StringVar()
passE = StringVar()
reEntry=StringVar()

l_frame = Frame(lP,width=500,height=300,bg="white",highlightbackground="black", highlightthickness=2).place(x=50,y=30)

mainL = Label(l_frame,text="WELCOME TO HENRY'S PHARMA",font=("Courier New",30),bg="white",fg="blue",).place(x=80,y=50)

Label(l_frame,text="Username",font=("Courier New",18),bg="white",fg="blue").place(x=130,y=120)
Label(l_frame,text="Password",font=("Courier New",18),bg="white",fg="blue").place(x=130,y=170)

userEntry = Entry(l_frame,font=("Courier New",20), textvariable = userE, width=16,bg="white",fg="blue")
userEntry.place(x=250,y=120)

passEntry = Entry(l_frame,font=("Courier New",20), textvariable = passE, width=16,show="*",bg="white",fg='blue')
passEntry.place(x=250,y=170)

loginB = Button(l_frame,text="Login",font=('Calabri',15),width=7,command=handle_login,bg="white")
loginB.place(x=245,y=260,height=40)

registerB = Button(l_frame,text="Register",font=('Calabri',15),width=7,command=register_mode,bg="white")
registerB.place(x=363,y=260,height=40)

lP.mainloop()
