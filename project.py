
import sqlite3
try:
    con=sqlite3.connect(database="banking.sqlite")
    cur=con.cursor()
    cur.execute("create table accounts(acn integer primary key autoincrement,name text,password text,email text,mob text,bal float,type text,opendate text)")
    cur.execute("create table txn_history(acn int,txn_amt float,txn_type float,txn_date text,update_bal float)")
    con.commit()
    print("tables created")
except:
    print("something went wrong,might be table already exist")
con.close()
from tkinter import *
from tkinter.ttk import Combobox
from datetime import datetime
import time
from tkinter import messagebox,filedialog
import random
import gmail
import sqlite3
import smtplib
import winsound
from tkinter.ttk import Style,Treeview,Scrollbar
from PIL import Image,ImageTk
import shutil
import os
win=Tk()
win.state("zoomed")
win.resizable(width=False,height=True)
win.configure(bg='pink')

lbl_title=Label(win,text="Banking Automation",bg='pink',fg='blue',font=('arial',60,'bold','underline'))
lbl_title.pack()

lbl_date=Label(win,text=f"{datetime.now().date()}",bg='pink',fg='black',font=('arial',18,'bold'))
lbl_date.place(relx=.9,rely=.1)
                
def main_screen():
    frm=Frame(win)
    frm.configure(bg='skyblue')
    frm.place(x=0,rely=.15,relwidth=1,relheight=.9)
    
    lbl_name=Label(win,text="Developed by:Yash kumar",bg='pink',fg='black',font=('arial',15,'bold','underline'))
    lbl_name.place(relx=.8,rely=.9)
    
    def forgo_pswrd():
        freq=500
        dur=200
        winsound.Beep(freq,dur)  
        frm.destroy()
        forgopass_screen()
        
    def open_account():
        freq=500
        dur=200
        winsound.Beep(freq,dur)  
        frm.destroy()
        openaccount_screen()
        
        
    def login_account():
        freq=500
        dur=200
        winsound.Beep(freq,dur)  
        global name,acn
        acn=entry_acn.get()
        pwd=entry_pswrd.get()
        if(acn=="" or pwd==""):
            messagebox.showerror("Login","ACN\PASS can't be empty")
            return
        con=sqlite3.connect(database="banking.sqlite")
        cur=con.cursor()
        cur.execute("select name from accounts where acn=? and password=?",(acn,pwd))
        row=cur.fetchone()
        con.close()
        if(row==None):
            messagebox.showerror("Login","Invalid ACN/PASS")
        else:
            name=row[0]
            frm.destroy()
            loginaccount_screen() 
        
    def reset():
        freq=500
        dur=200
        winsound.Beep(freq,dur)  
        entry_acn.delete(0,"end")
        entry_pswrd.delete(0,"end")
        entry_acn.focus()
        
    lbl_acn=Label(frm,text='Account No:',bg='skyblue',font=('arial',20,'bold'))
    lbl_acn.place(relx=.3,rely=.1) 
    
    entry_acn=Entry(frm,font=('arial',20,'bold'),bd=5)
    entry_acn.place(relx=.43,rely=.1)
    entry_acn.focus()
    
    lbl_pswrd=Label(frm,text='Paswword:',bg='skyblue',font=('arial',20,'bold'))
    lbl_pswrd.place(relx=.3,rely=.24)
    
    entry_pswrd=Entry(frm,font=('arial',20,'bold'),bd=5,show="*")
    entry_pswrd.place(relx=.43,rely=.24)
    
    btn_login=Button(frm,command=login_account,text='Login',font=('arial',20,'bold'),bd=4,bg="pink")
    btn_login.place(relx=.46,rely=.37)
    
    btn_reset=Button(frm,command=reset,text='Reset',font=('arial',20,'bold'),bd=4,bg="pink")
    btn_reset.place(relx=.55,rely=.37)
    
    btn_open=Button(frm,command=open_account,text='Open Account',font=('arial',20,'bold'),width=15,bd=4,bg="pink")
    btn_open.place(relx=.444,rely=.5)
    
    btn_forgotpswrd=Button(frm,command=forgo_pswrd,text='Forgot password',font=('arial',20,'bold'),width=18,bd=4,bg="pink")
    btn_forgotpswrd.place(relx=.427,rely=.63)
    
def forgopass_screen():
    frm=Frame(win)
    frm.configure(bg='skyblue')
    frm.place(x=0,rely=.15,relwidth=1,relheight=.9)
    
    def back():
        freq=500
        dur=200
        winsound.Beep(freq,dur)  
        frm.destroy()
        main_screen()  
        
    def send_otp():
        freq=500
        dur=200
        winsound.Beep(freq,dur)  
        acn=entry_acn.get()
        email=entry_email.get()
        
        con=sqlite3.connect(database="banking.sqlite")
        cur=con.cursor()
        cur.execute("select email,password from accounts where acn=?",(acn,))
        row= cur.fetchone()
        if(row==None):
            messagebox.showerror("Password Recovery","ACN does not exist")
        else:
            if(row[0]==email):
                otp=''.join([str(random.randint(0,9)) for i in range(4)])
                print(otp)
                
                try:
                    server=smtplib.SMTP('smtp.gmail.com',587)
                    server.starttls()
                    server.login('kumars15651@gmail.com','yvctnxrpkkusmjvh')
                    msg='Hello,your otp for yash bank project forgot password is '+str(otp)
                    server.sendmail('kumars15651@gmail.com',f'{email}',msg)
                    server.quit()
                    messagebox.showinfo("Password Recovery","OTP send,Pls check your Email")
                
                except:
                    messagebox.showerror("Password Recovery","Somthingn went wrong")
                
                
                
                lbl_otp=Label(frm,text='OTP:',bg='skyblue',font=('arial',15,'bold'))
                lbl_otp.place(relx=.43,rely=.52)
                
                entry_otp=Entry(frm,font=('arial',20,'bold'),bd=5)
                entry_otp.place(relx=.43,rely=.6)
                entry_otp.focus()
                
                def getpass():
                    verify_otp=entry_otp.get()
                    if(otp==verify_otp):
                        messagebox.showinfo("Password Recovery",f"Your password:{row[1]}")
                    else:
                        messagebox.showerror("Password Recovery","Incorrect otp")
                
                
                btn_verify=Button(frm,command=getpass,text='Verify',font=('arial',20,'bold'),bd=4,bg="pink")
                btn_verify.place(relx=.6,rely=.7)
                
                
            else:
                messagebox.showerror("Password Recovery","Email is not correct")
        
        con.close()
            
        
        
        
    btn_back=Button(frm,command=back,text='Back',font=('arial',20,'bold'),bd=4,bg="pink")
    btn_back.place(relx=0,rely=0)
     
    lbl_frmtitle=Label(frm,text='This is Forgot Password Screen',bg='skyblue',font=('arial',20,'bold'),fg='green')
    lbl_frmtitle.place(relx=.38,rely=.05)
    
    lbl_acn=Label(frm,text='Account No:',bg='skyblue',font=('arial',20,'bold'))
    lbl_acn.place(relx=.3,rely=.2) 
    
    entry_acn=Entry(frm,font=('arial',20,'bold'),bd=5)
    entry_acn.place(relx=.43,rely=.2)
    entry_acn.focus()
    
    lbl_email=Label(frm,text='Email:',bg='skyblue',font=('arial',20,'bold'))
    lbl_email.place(relx=.3,rely=.3)
    
    entry_email=Entry(frm,font=('arial',20,'bold'),bd=5)
    entry_email.place(relx=.43,rely=.3)
    
    btn_back=Button(frm,command=send_otp,text='Send OTP',font=('arial',20,'bold'),bd=4,bg="pink")
    btn_back.place(relx=.6,rely=.4)
    
def openaccount_screen():
    frm=Frame(win)
    frm.configure(bg='skyblue')
    frm.place(x=0,rely=.15,relwidth=1,relheight=.9)
    
    def back():
        freq=500
        dur=200
        winsound.Beep(freq,dur)  
        frm.destroy()
        main_screen()
        
    def open_acn():
        name=entry_name.get()
        pwd=entry_pswrd.get()
        email=entry_email.get()
        mob=entry_mob.get()
        acn_type=combo_type.get()
        opendate=time.ctime()
        bal=1000
        
        con=sqlite3.connect(database="banking.sqlite")
        cur=con.cursor()
        cur.execute("insert into accounts(name,password,email,mob,bal,type,opendate) values(?,?,?,?,?,?,?)",(name,pwd,email,mob,bal,acn_type,opendate))
        con.commit()
        con.close()
                                                                                                            
        con=sqlite3.connect(database="banking.sqlite")
        cur=con.cursor()
        cur.execute("select max(acn) from accounts")
        row= cur.fetchone()
        lbl_acn_open=Label(frm,text=f"Account opend with ACN:{row[0]}",bg='skyblue',font=('arial',20,'bold'),fg="green")
        lbl_acn_open.place(relx=.4,rely=.75)                 
        con.close
        
        entry_name.delete(0,"end")
        entry_mob.delete(0,"end")
        entry_pswrd.delete(0,"end")
        entry_email.delete(0,"end")
        entry_name.focus()
        
                                                                                                                            
        
    btn_back=Button(frm,command=back,text='Back ',font=('arial',20,'bold'),bd=4,bg="pink")
    btn_back.place(relx=0,rely=0)
    
    lbl_frmtitle=Label(frm,text='This is Open Account Screen',bg='skyblue',font=('arial',20,'bold'),fg='green')
    lbl_frmtitle.pack()
    
    lbl_name=Label(frm,text='Name:',bg='skyblue',font=('arial',20,'bold'))
    lbl_name.place(relx=.3,rely=.1) 
    
    entry_name=Entry(frm,font=('arial',20,'bold'),bd=5)
    entry_name.place(relx=.42,rely=.1)
    entry_name.focus()
    
    lbl_pswrd=Label(frm,text='Password:',bg='skyblue',font=('arial',20,'bold'))
    lbl_pswrd.place(relx=.3,rely=.2)
    
    entry_pswrd=Entry(frm,font=('arial',20,'bold'),bd=5,show="*")
    entry_pswrd.place(relx=.42,rely=.2)
    
    lbl_email=Label(frm,text='Email:',bg='skyblue',font=('arial',20,'bold'))
    lbl_email.place(relx=.3,rely=.3) 
    
    entry_email=Entry(frm,font=('arial',20,'bold'),bd=5)
    entry_email.place(relx=.42,rely=.3)
    
    lbl_mob=Label(frm,text='Mobile No:',bg='skyblue',font=('arial',20,'bold'))
    lbl_mob.place(relx=.3,rely=.4)
    
    entry_mob=Entry(frm,font=('arial',20,'bold'),bd=5)
    entry_mob.place(relx=.42,rely=.4)
    
    lbl_type=Label(frm,text='Type:',bg='skyblue',font=('arial',20,'bold'))
    lbl_type.place(relx=.3,rely=.5)
    
    combo_type=Combobox(frm,font=('arial',20,'bold'),values=['Saving','Current'])
    combo_type.current(0)
    combo_type.place(relx=.42,rely=.5)
    
    btn_open=Button(frm,command=open_acn,text='Open',font=('arial',20,'bold'),width=5,bd=5,bg="pink")
    btn_open.place(relx=.444,rely=.6)
    
    btn_reset=Button(frm,text='Reset',font=('arial',20,'bold'),width=5,bd=5,bg="pink")
    btn_reset.place(relx=.53,rely=.6)
    
def loginaccount_screen():
    frm=Frame(win)
    frm.configure(bg='skyblue')
    frm.place(x=0,rely=.15,relwidth=1,relheight=.9)
    
    def back():
        freq=500
        dur=200
        winsound.Beep(freq,dur)  
        frm.destroy()
        main_screen()
        
    def details():
        freq=500
        dur=200
        winsound.Beep(freq,dur)  
        ifrm=Frame(frm,highlightthickness=3,highlightbackground='black')
        ifrm.configure(bg='white')
        ifrm.place(relx=.3,rely=.15,relwidth=.4,relheight=.6)
        lbl_frmtitle.configure(text='This is Check Detail Screen')
        
        con=sqlite3.connect(database="banking.sqlite")
        cur=con.cursor()
        cur.execute("select acn,bal,opendate,type from accounts where acn=?",(acn))
        row=cur.fetchone()
        con.close()
        
        Label(ifrm,text=f"Account No.\t{row[0]}",font=('',15),bg="white",fg="purple").place(relx=.2,rely=.1)
        Label(ifrm,text=f"Account Bal\t{row[1]}",font=('',15),bg="white",fg="purple").place(relx=.2,rely=.2)
        Label(ifrm,text=f"Account opendate\t{row[2]}",font=('',15),bg="white",fg="purple").place(relx=.2,rely=.3)
        Label(ifrm,text=f"Account type\t{row[3]}",font=('',15),bg="white",fg="purple").place(relx=.2,rely=.4)
        
        
        
    def update():
        freq=500
        dur=200
        winsound.Beep(freq,dur)  
        ifrm=Frame(frm,highlightthickness=3,highlightbackground='black')
        ifrm.configure(bg='white')
        ifrm.place(relx=.3,rely=.15,relwidth=.4,relheight=.6)
        lbl_frmtitle.configure(text='This is Update Profile Screen')
        
        def update_profile_afterlogin():
            name=entry_name.get()
            pwd=entry_pass.get()
            email=entry_email.get()
            mob=entry_mob.get()
            
            con=sqlite3.connect(database="banking.sqlite")
            cur=con.cursor()
            cur.execute("update accounts set name=?,password=?,email=?,mob=? where acn=?",(name,pwd,email,mob,acn,))
            con.commit()
            con.close()
            
            messagebox.showinfo("Update Profile","Profile Updated")
            lbl_wel.configure(text=f"Welcome,{name}")
        
        lbl_name=Label(frm,text="Name",bg='white',font=('arial',11,'bold'))
        lbl_name.place(relx=.314,rely=.23)
        
        entry_name=Entry(ifrm,font=('arial',15,'bold'),bd=5)
        entry_name.place(relx=.03,rely=.2)
        entry_name.focus() 
        
        lbl_pass=Label(frm,text="Password",bg='white',font=('arial',11,'bold'))
        lbl_pass.place(relx=.51,rely=.23)
        
        entry_pass=Entry(ifrm,font=('arial',15,'bold'),bd=5)
        entry_pass.place(relx=.53,rely=.2)
        
        lbl_email=Label(frm,text="Email",bg='white',font=('arial',11,'bold'))
        lbl_email.place(relx=.314,rely=.41)
        
        entry_email=Entry(ifrm,font=('arial',15,'bold'),bd=5)
        entry_email.place(relx=.03,rely=.52)
        entry_email.focus() 
        
        lbl_mob=Label(frm,text="Mobile No",bg='white',font=('arial',11,'bold'))
        lbl_mob.place(relx=.51,rely=.41)
        
        entry_mob=Entry(ifrm,font=('arial',15,'bold'),bd=5)
        entry_mob.place(relx=.53,rely=.52)
        
        btn_update=Button(frm,command=update_profile_afterlogin,text='Update',font=('arial',15,'bold'),bd=4,bg="pink")
        btn_update.place(relx=.46,rely=.56)
        
        con=sqlite3.connect(database="banking.sqlite")
        cur=con.cursor()
        cur.execute("select name,password,email,mob from accounts where acn=?",(acn,))
        row=cur.fetchone()
        con.close()
        
        entry_name.insert(0,row[0])
        entry_pass.insert(0,row[1])
        entry_email.insert(0,row[2])
        entry_mob.insert(0,row[3])
        
       
        
        
        
    def deposite():
        freq=500
        dur=200
        winsound.Beep(freq,dur)  
        ifrm=Frame(frm,highlightthickness=3,highlightbackground='black')
        ifrm.configure(bg='white')
        ifrm.place(relx=.3,rely=.15,relwidth=.4,relheight=.6)
        lbl_frmtitle.configure(text='This is Deposite Screen')
        
        def deposit_acn():
            amt=float(entry_amt.get())
            
            con=sqlite3.connect(database="banking.sqlite")
            cur=con.cursor()
            cur.execute("select bal from accounts where acn=?",(acn,))
            bal=cur.fetchone()[0]
            cur.close()
            
            cur=con.cursor()
            cur.execute("update accounts set bal=bal+? where acn=?",(amt,acn))
            cur.execute("insert into txn_history values(?,?,?,?,?)",(acn,amt,"Cr",time.ctime(),bal+amt))
            con.commit()
            con.close()
            
            messagebox.showinfo("Deposit",f"Amount {amt} credited to ACN:{acn}")
            
        
        lbl_amt=Label(frm,text="Amount",bg='white',font=('arial',20,'bold'))
        lbl_amt.place(relx=.34,rely=.28)
        
        entry_amt=Entry(ifrm,font=('arial',20,'bold'),bd=5)
        entry_amt.place(relx=.35,rely=.2)
        entry_amt.focus() 
        
        btn_dept=Button(frm,command=deposit_acn,text='Deposite',font=('arial',20,'bold'),bd=4,bg="pink")
        btn_dept.place(relx=.53,rely=.37)
        
        
    def withdraw():
        freq=500
        dur=200
        winsound.Beep(freq,dur)  
        ifrm=Frame(frm,highlightthickness=3,highlightbackground='black')
        ifrm.configure(bg='white')
        ifrm.place(relx=.3,rely=.15,relwidth=.4,relheight=.6)
        lbl_frmtitle.configure(text='This is Withdraw Screen')
        
        def withdraw_acn():
            amt=float(entry_amt.get())
            
            con=sqlite3.connect(database="banking.sqlite")
            cur=con.cursor()
            cur.execute("select bal from accounts where acn=?",(acn,))
            bal=cur.fetchone()[0]
            cur.close()
            
            
            if(bal>amt):
                cur=con.cursor()
                cur.execute("update accounts set bal=bal-? where acn=?",(amt,acn))
                cur.execute("insert into txn_history values(?,?,?,?,?)",(acn,amt,"Cr",time.ctime(),bal-amt))
                con.commit()
                con.close()
            
                messagebox.showinfo("Withdraw",f"Amount {amt} withdrawn from ACN:{acn}")
            else:
                messagebox.showerror("Withdraw",f"Insufficent Bal:{bal}")
                
                
            
            
            
        lbl_amt=Label(frm,text="Amount",bg='white',font=('arial',20,'bold'))
        lbl_amt.place(relx=.34,rely=.28)
        entry_amt=Entry(ifrm,font=('arial',20,'bold'),bd=5)
        entry_amt.place(relx=.35,rely=.2)
        entry_amt.focus()
        btn_widrw=Button(frm,command=withdraw_acn,text='Withdraw',font=('arial',20,'bold'),bd=4,bg="pink")
        btn_widrw.place(relx=.53,rely=.37)
        
        
        
        
    def transfer():
        freq=500
        dur=200
        winsound.Beep(freq,dur)  
        ifrm=Frame(frm,highlightthickness=3,highlightbackground='black')
        ifrm.configure(bg='white')
        ifrm.place(relx=.3,rely=.15,relwidth=.4,relheight=.6)
        lbl_frmtitle.configure(text='This is Transfer Screen')
        
        def transfer_acn():
            to_acn=entry_to.get()
            frm_amt=float(entry_amt.get())
            
            con=sqlite3.connect(database="banking.sqlite")
            cur=con.cursor()
            cur.execute("select acn,bal from accounts where acn=?",(to_acn,))
            to_row=cur.fetchone()
            cur.close()
            if(to_row==None):
                messagebox.showerror("Transfer","To Account does not exist")
            else:
                cur=con.cursor()
                cur.execute("select bal from accounts where acn=?",(acn,))
                bal=cur.fetchone()[0]
                cur.close()
                if(bal>frm_amt):
                    cur=con.cursor()
                    cur.execute("update accounts set bal=bal+? where acn=?",(frm_amt,to_acn))
                    cur.execute("update accounts set bal=bal-? where acn=?",(frm_amt,acn))
                    cur.execute("insert into txn_history values(?,?,?,?,?)",(acn,frm_amt,"Db",time.ctime(),bal-frm_amt))
                    cur.execute("insert into txn_history values(?,?,?,?,?)",(to_acn,frm_amt,"Cr",time.ctime(),to_row[1]+frm_amt))
                    con.commit()
                    con.close()
                    messagebox.showinfo("Transfer","Txn Done")
                    
                else:
                     messagebox.showerror("Transfer",f"Insufficent Bal:{bal}")
                    
            
                
            
        lbl_to=Label(ifrm,text="To",bg='white',font=('arial',20,'bold'))
        lbl_to.place(relx=.1,rely=.2)
        
        entry_to=Entry(ifrm,font=('arial',20,'bold'),bd=5)
        entry_to.place(relx=.3,rely=.2)
        entry_to.focus()
        
        lbl_amt=Label(ifrm,text="Amount",bg='white',font=('arial',20,'bold'))
        lbl_amt.place(relx=.09,rely=.4)
        
        entry_amt=Entry(ifrm,font=('arial',20,'bold'),bd=5)
        entry_amt.place(relx=.3,rely=.4)
        
        btn_trans=Button(ifrm,command=transfer_acn,text='Transfer',font=('arial',20,'bold'),bd=4,bg="pink")
        btn_trans.place(relx=.4,rely=.6)
        
        
        
        
    def txn():
        freq=500
        dur=200
        winsound.Beep(freq,dur)  
        ifrm=Frame(frm,highlightthickness=3,highlightbackground='black')
        ifrm.configure(bg='white')
        ifrm.place(relx=.3,rely=.15,relwidth=.4,relheight=.6)
        lbl_frmtitle.configure(text='This is Txn History Screen')
        
        tv=Treeview(ifrm)
        tv.place(x=0,y=0,height=100,width=500)
        
        style = Style()
        style.configure("Treeview.Heading",font=('Arial',15,'bold'),foreground='brown')
                                                 
        sb=Scrollbar(ifrm,orient='vertical',command=tv.yview)
        sb.place(x=498,y=0,height=100)
        tv.configure(yscrollcommand=sb.set)
                                                 
        tv['columns']=('col1','col2','col3','col4')
                                                 
        tv.column('col1',width=120,anchor='c')
        tv.column('col2',width=80,anchor='c')
        tv.column('col3',width=80,anchor='c')                                         
        tv.column('col4',width=100,anchor='c')     
        
                                                 
        tv.heading('col1',text='Date')
        tv.heading('col2',text='Amt')                                          
        tv.heading('col3',text='Type')
        tv.heading('col4',text='Updated amt')                                         
                                                 
        tv['show']='headings'
                                                 
        con=sqlite3.connect(database='banking.sqlite')
        cur=con.cursor()
        cur.execute("select * from txn_history where acn=?",(acn,))
                                                 
        for row in cur:
            tv.insert("","end",values=(row[3],row[1],row[2],row[4]))
                                                 
    def updatepic():
        img=filedialog.askopenfilename()
        shutil.copy(img,f"{acn}.png")
        img=Image.open(f"{acn}.png").resize((100,130))
        imgtk=ImageTk.PhotoImage(img,master=win)
        lbl_img.image=imgtk
        lbl_img['image']=imgtk
    
    
    btn_back=Button(frm,command=back,text='Logout',font=('arial',20,'bold'),bd=4,bg="pink")
    btn_back.place(relx=.91,rely=0)
    
    lbl_frmtitle=Label(frm,text='This is Login Account Screen',bg='skyblue',font=('arial',20,'bold'),fg='green')
    lbl_frmtitle.place(relx=.38,rely=.05)
    
    global lbl_wel
    lbl_wel=Label(frm,text=f"WELCOME,{name}",bg='skyblue',font=('arial',20,'bold'),fg='green')
    lbl_wel.place(relx=0,rely=0)
   
    global img,imgtk,lbl_img
    
    if(os.path.exists(f"{acn}.png")):
        img=Image.open(f"{acn}.png").resize((100,130))
        imgtk=ImageTk.PhotoImage(img,master=win)
    else:
        img=Image.open("profile.jpg").resize((100,130))
        imgtk=ImageTk.PhotoImage(img,master=win)
    
        
    lbl_img=Label(frm,image=imgtk)
    lbl_img.place(relx=.01,rely=.05)
    
    btn_propic=Button(frm,command=updatepic,text='Update pic',bd=4,bg="pink")
    btn_propic.place(relx=.09,rely=.23)
    
    btn_details=Button(frm,command=details,width=12,text='Check Details',font=('arial',20,'bold'),bd=4,bg="pink")
    btn_details.place(relx=.0,rely=.29)
    

    btn_update_profile=Button(frm,command=update,width=12,text='Update Profile',font=('arial',20,'bold'),bd=4,bg="pink")
    btn_update_profile.place(relx=.0,rely=.4)
    
    btn_deposite=Button(frm,command=deposite,width=12,text='Deposit',font=('arial',20,'bold'),bd=4,bg="pink")
    btn_deposite.place(relx=.0,rely=.51)
    
    btn_withdraw=Button(frm,command=withdraw,width=12,text='Withdraw',font=('arial',20,'bold'),bd=4,bg="pink")
    btn_withdraw.place(relx=.0,rely=.62)
    
    btn_transfer=Button(frm,command=transfer,width=12,text='Transfer',font=('arial',20,'bold'),bd=4,bg="pink")
    btn_transfer.place(relx=.0,rely=.73)
    
    btn_txn=Button(frm,command=txn,width=12,text='Trans. History',font=('arial',20,'bold'),bd=4,bg="pink")
    btn_txn.place(relx=.0,rely=.84)
        
    
    
main_screen()
win.mainloop()







