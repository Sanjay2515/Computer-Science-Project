    f7 =  LabelFrame(mainframe,bg='white',height=553,width=650,text="REGISTER ORDER",fg="#2196F3",highlightbackground="black", highlightthickness=10,font=('Consolas',30))
    f7.place(x=300,y=100)

    ff7=Frame(f7,bg='white',height=350,width=600,highlightbackground="black", highlightthickness=2)
    ff7.place(x=10,y=20)
    
    p_get= database_handle('ret','P_NAME','patients')
    p_list = []
    for i in p_get:
        p_list.append(i[0])

    
    Label(ff7, text="PATIENT NAME: ",font=('Courier New', 18),fg='blue', bg='white').place(x=10,y=20)
    Label(ff7, text="MED TYPE: ",font=('Courier New', 18),fg='blue', bg='white').place(x=10,y=70)
    Label(ff7, text="MANUFACTURER: ",font=('Courier New', 18),fg='blue', bg='white').place(x=10,y=120)
    Label(ff7, text="PRICE: ",font=('Courier New', 18),fg='blue', bg='white').place(x=10,y=170)
    Label(ff7, text="QUANTITY: ",font=('Courier New', 18),fg='blue', bg='white').place(x=10,y=220)

    opE = Entry(ff7, width=20, font=('Courier New', 14), fg='blue', bg='white', textvariable=mn)
    mnE.place(x=400, y=20)

    mcE = Entry(ff7, textvariable = mc, width=20, font=('Courier New', 14) ,fg='blue', bg='white')
    mcE.place(x=400,y=120)

    mtE = ttk.Combobox(ff7, values=p_list,width=18,background="pink", textvariable = mt)
    mtE.set("Select Medicine Type")
    mtE.place(x=400,y=70)

    mpE = Entry(ff7,width=20,font=('Courier New', 14),fg='blue', bg='white', textvariable = mp)
    mpE.place(x=400,y=170)

    mqE = Entry(ff7,width=20,font=('Courier New', 14),fg='blue', bg='white', textvariable = mq)
    mqE.place(x=400,y=220)

    Button(ff7,text="Register",font=('Courier New',14),bg="white",width=60,height=3,command= lambda: database_handle('rm')).place(x=10,y=280)
