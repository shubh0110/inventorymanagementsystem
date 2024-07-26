from tkinter import *
import tkinter.messagebox as tkMessageBox
import sqlite3
import tkinter.ttk as ttk
import datetime
import time
global nusername
global npassword
from PIL import Image, ImageTk

root = Tk()
root.title("Inventory System")
root.geometry("800x600")
#root.resizable(0, 0)
root.config(bg="#FF4500")

#================================================================================= WINDOW MAIN PAGE FRAME =======================================================================================#

class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.pack(fill=BOTH, expand=20)
    
        try:
            load = Image.open("Inventory.png")
            render = ImageTk.PhotoImage(load)
            img = Label(self, image=render)
            img.image = render
            img.place(x=5, y=10)
        except FileNotFoundError:
            print("Error: Image file 'Inventory.png' not found.")
app = Window(root)
date=datetime.datetime.now().date()
time=time.strftime("%I:%M %p")
USERNAME = StringVar()
PASSWORD = StringVar()
PRODUCT_NAME = StringVar()
PRODUCT_COST_PRICE = []
PRODUCT_SELLING_PRICE = []
PRODUCT_QTY = []
SEARCH = StringVar()
PRODUCT_ID = []
PRODUCT_LIST = []
PRODUCT_TOTALSELLING_PRICE=[]
PRODUCT_TOTALCOST_PRICE=[]

#==================================================================================== DATABASE =======================================================================================#


def Database():
    global nusername
    global npassword
    global conn, cursor
    conn = sqlite3.connect("pythontut.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS `admin` (admin_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT, password TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS `product` (product_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, product_name TEXT, product_qty TEXT, product_cost_price TEXT,product_selling_price TEXT,product_totalcost_price TEXT,product_totalselling_price TEXT,assumed_price TEXT)")
    cursor.execute("SELECT * FROM `admin` WHERE `username` = 'Shubh' AND `password` = 'shubh@123'")
    conn.commit()


#=============================================================================== EXIT MAIN PAGE =======================================================================================#

    
def Exit():
    result = tkMessageBox.askquestion('Inventory System', 'Are you sure you want to exit?', icon="warning")
    if result == 'yes':
        root.destroy()
        exit()



#============================================================================= LOGIN PAGE INVENTORY ================================================================================#


def ShowLoginForm():
    global loginform
    loginform = Toplevel()
    loginform.title("Inventory System/Account Login")
    loginform.resizable(0, 0)
    loginform.geometry("800x500")
    LoginForm()
    
def LoginForm():
    global lbl_result
    TopLoginForm = Frame(loginform, width=600, height=100)
    TopLoginForm.pack(side=TOP, pady=20)
    lbl_text = Label(TopLoginForm, text="Administrator Login", font=('arial', 20), width=600)
    lbl_text.pack(fill=X)
    MidLoginForm = Frame(loginform, width=600)
    MidLoginForm.pack(side=TOP, pady=50)
    lbl_username = Label(MidLoginForm, text="Username:", font=('arial', 25))
    lbl_username.grid(row=0)
    lbl_password = Label(MidLoginForm, text="Password:", font=('arial', 25))
    lbl_password.grid(row=1)
    lbl_result = Label(MidLoginForm, text="", font=('arial', 18))
    lbl_result.grid(row=3, columnspan=2)
    username = Entry(MidLoginForm, textvariable=USERNAME, font=('arial', 25), width=15)
    username.grid(row=0, column=1)
    password = Entry(MidLoginForm, textvariable=PASSWORD, font=('arial', 25), width=15, show="*")
    password.grid(row=1, column=1)
    btn_login = Button(MidLoginForm, text="Login", font=('arial', 18), width=30, command=Login)
    btn_login.grid(row=2, columnspan=2, pady=20)
    btn_login.bind('<Return>', Login)

def Login(event=None):
    global admin_id
    Database()
    if USERNAME.get == "" or PASSWORD.get() == "":
        lbl_result.config(text="Please complete the required field!")
    else:
        cursor.execute("SELECT * FROM `admin` WHERE `username` = ? AND `password` = ?", (USERNAME.get(), PASSWORD.get()))
        if cursor.fetchone() is not None:
            cursor.execute("SELECT * FROM `admin` WHERE `username` = ? AND `password` = ?", (USERNAME.get(), PASSWORD.get()))
            data = cursor.fetchone()
            admin_id = data[0]
            USERNAME.set("")
            PASSWORD.set("")
            lbl_result.config(text="")
            ShowHome()
        else:
            lbl_result.config(text="Invalid username or password")
            USERNAME.set("")
            PASSWORD.set("")
    cursor.close()
    conn.close() 





#============================================================================= HOME INVENTORY ================================================================================


def Home():
    global Home
    Home = Tk()
    Home.title("Inventory System/Home")
    Home.geometry("1000x400")
    
    Home.config(bg="#F08080")
    Title = Frame(Home, bd=1, relief=SOLID)
    Title.pack(pady=10)
   
    lbl_display = Label(Title, text="Welcome to Super Store", font=('arial', 45))
    lbl_display.pack()
    lbl_display = Label(Title, text="Inventory Management System", font=('arial', 45))
    lbl_display.pack()
   
    menubar = Menu(Home)
    filemenu = Menu(menubar, tearoff=0)
    filemenu2 = Menu(menubar, tearoff=0)
    filemenu3 = Menu(menubar, tearoff=0)
    filemenu.add_command(label="Password",command=Password)
    filemenu.add_command(label="Logout", command=Logout)
    filemenu.add_command(label="Exit", command=Exit2)
    filemenu2.add_command(label="Add new", command=ShowAddNew)
    filemenu2.add_command(label="View", command=ShowView)
    filemenu3.add_command(label="Show User View",command=ShowUserView)
    menubar.add_cascade(label="Account", menu=filemenu)
    menubar.add_cascade(label="Inventory", menu=filemenu2)
    menubar.add_cascade(label="User View Inventory",menu=filemenu3)
    Home.config(menu=menubar)



#========================================================================= CHANGE PASSWORD ================================================================================#
    
    
def Password():
   global pas
   global nusername
   global npassword
   pas=Tk()
   pas.title("Change Username and Password")
   pas.geometry("500x300")
   pas.resizable(0,0)
   pas.config(bg="#54FF9F")
   lbl_text = Label(pas,text="Change Username and Password", font=('arial', 20), width=600)
   lbl_password = Label(pas,text="New Password:", font=('arial', 25))
   lbl_password.pack(fill=X)
   npassword = Entry(pas,textvariable=PASSWORD, font=('arial', 25), width=10, show="*")
   npassword.pack()
   btn_login = Button(pas,text="Change", font=('arial', 18), width=10, command=change)
   btn_login.pack()
   btn_login.bind('<Return>', Login)

def change():
    global nusername
    global npassword
    Database()
    cursor.execute("UPDATE admin SET password='{}' WHERE username='shubh' ".format(npassword.get()))
    conn.commit()
    cursor.close()
    conn.close()
    result = tkMessageBox.showinfo("Username/Password","Password has been changed")
    tkMessageBox.showinfo("Username/Password","Please Open the File again")
    pas.destroy()
    Home.destroy()
    
#================================================================================ LOGOUT ===================================================================================#

def Logout():
    result = tkMessageBox.askquestion('Inventory System', 'Are you sure you want to logout?', icon="warning")
    if result == 'yes': 
        admin_id = ""
        root.deiconify()
        Home.destroy()

#============================================================================== EXIT HOME =======================================================================================#

def Exit2():
    result = tkMessageBox.askquestion('Inventory System', 'Are you sure you want to exit?', icon="warning")
    if result == 'yes':
        Home.destroy()
        exit()
        
#======================================================================== SHOW ADD NEW INVENTORY ================================================================================#

   
def ShowAddNew():
    global addnewform
    addnewform = Toplevel()
    addnewform.title("Inventory System/Add new")
    addnewform.geometry("1366x768+0+0")
    addnewform.config(bg="#FFA07A")
    AddNewForm()

def AddNewForm():
    global productname
    global productqty
    global productcostprice
    global productsellingprice
    global id_e
    TopAddNew = Frame(addnewform, width=600, height=100, bd=1, relief=SOLID)
    TopAddNew.pack(side=TOP, pady=20)
    lbl_text = Label(TopAddNew, text="Add New Product", font=('arial', 18), width=600)
    lbl_text.pack(fill=X)
    MidAddNew = Frame(addnewform, width=100)
    MidAddNew.pack(side=TOP, pady=10)
    lbl_productname = Label(MidAddNew, text="Product Name:", font=('arial', 25), bd=10)
    lbl_productname.grid(row=0, sticky=W)
    lbl_qty = Label(MidAddNew, text="Product Quantity:", font=('arial', 25), bd=10)
    lbl_qty.grid(row=1, sticky=W)
    lbl_price = Label(MidAddNew, text="Product Cost Price:", font=('arial', 25), bd=10)
    lbl_price.grid(row=2, sticky=W)
    lbl_price = Label(MidAddNew, text="Product Selling Price:", font=('arial', 25), bd=10)
    lbl_price.grid(row=3, sticky=W)
    productname = Entry(MidAddNew, textvariable=PRODUCT_NAME, font=('arial', 25), width=15)
    productname.grid(row=0, column=1)
    productqty = Entry(MidAddNew, textvariable=PRODUCT_QTY, font=('arial', 25), width=15)
    productqty.grid(row=1, column=1)
    productcostprice = Entry(MidAddNew, textvariable=PRODUCT_COST_PRICE, font=('arial', 25), width=15)
    productcostprice.grid(row=2, column=1)
    productsellingprice = Entry(MidAddNew, textvariable=PRODUCT_SELLING_PRICE, font=('arial', 25), width=15)
    productsellingprice.grid(row=3, column=1)
    btn_add = Button(MidAddNew, text="Save", font=('arial', 18), width=30, command=AddNew)  
    btn_add.grid(row=4, columnspan=2, pady=20)
    btn_clear=Button(MidAddNew,text="Clear All Fields",width=30,height=2,command=clear_all)
    btn_clear.grid(row=5, columnspan=2, pady=20)

def AddNew():
    global productname
    global productqty
    global productcostprice
    global productsellingprice
    global id_e
    

    name = productname.get()
    costprice=productcostprice.get()
    sellingprice=productsellingprice.get()
    qty = productqty.get()

    # dynamic entries
    totalcp = float(costprice) * float(qty)
    totalsp = float(sellingprice) * float(qty)
    assumed_profit = float(totalsp - totalcp)

    if name == '' or qty == '' or costprice == '' or sellingprice == '':
     tkinter.messagebox.showinfo("Error", "Please Fill all the entries.")
    else:
     Database()
     sql = "INSERT INTO product (product_name, product_qty, product_cost_price, product_selling_price, product_totalcost_price, product_totalselling_price, assumed_profit) VALUES(?,?,?,?,?,?,?)"
     cursor.execute(sql, (name, qty, costprice, sellingprice, totalcp, totalsp, assumed_profit))
     conn.commit()
     cursor.close()
     conn.close()
    

def clear_all():
       global productname
       global productqty
       global productcostprice
       global productsellingprice
       global id_e
       productname.delete(0, END)
       productqty.delete(0, END)
       productcostprice.delete(0, END)
       productsellingprice.delete(0, END)
       



#=============================================================================== SHOW VIEW INVENTORY ================================================================================#


def ShowView():
    global viewform
    viewform = Toplevel()
    viewform.title("Inventory System/View Product")
    viewform.geometry("800x600")
    ViewForm()

def ViewForm():
    global tree
    TopViewForm = Frame(viewform, width=600, bd=1, relief=SOLID)
    TopViewForm.pack(side=TOP, fill=X)
    LeftViewForm = Frame(viewform, width=900)
    LeftViewForm.pack(side=LEFT, fill=Y)
    MidViewForm = Frame(viewform, width=900)
    MidViewForm.pack(side=RIGHT,fill=Y)
    lbl_text = Label(TopViewForm, text="View Products", font=('arial', 18), width=600)
    lbl_text.pack(fill=X)
    lbl_txtproduct_id = Label(LeftViewForm, text="ProductID ", font=('arial 15 bold'))
    lbl_txtproduct_id.pack(side=TOP, anchor=W)
    
    prd_id = Entry(LeftViewForm, textvariable=SEARCH, font=('arial 15 bold'), width=10)
    prd_id.pack(side=TOP,  padx=10, fill=X)
    prd_id.focus()
    prd_id.delete(0,END)
    btn_search = Button(LeftViewForm, text="Search", command=Search)
    btn_search.pack(side=TOP, padx=10, pady=10, fill=X)
    btn_reset = Button(LeftViewForm, text="Reset", command=Reset)
    btn_reset.pack(side=TOP, padx=10, pady=10, fill=X)
    btn_delete = Button(LeftViewForm, text="Delete", command=Delete)
    btn_delete.pack(side=TOP, padx=10, pady=10, fill=X)
    scrollbarx = Scrollbar(MidViewForm, orient=VERTICAL)
    scrollbary = Scrollbar(MidViewForm, orient=HORIZONTAL)
    date_l=Label(MidViewForm,text="Today's Date: "+str(date),font=('arial 16 bold'))
    date_l.pack(side=TOP, fill=Y)
    time_l=Label(MidViewForm, text = "Time : " +str(time),font=('arial 16 bold'))
    time_l.pack(side=TOP, fill=Y)
    tree = ttk.Treeview(MidViewForm, columns=("ProductID", "Product Name", "Product Qty", "Product Selling Price"), selectmode="extended", height=200, yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
    tree.heading('ProductID', text="ProductID",anchor=W)
    tree.heading('Product Name', text="Product Name",anchor=W)
    tree.heading('Product Qty', text="Product Qty",anchor=W)   
    tree.heading('Product Selling Price', text="Product Selling Price",anchor=W)
    tree.column('#0', stretch=NO, minwidth=0, width=0)
    tree.column('#1', stretch=NO, minwidth=0, width=200)
    tree.column('#2', stretch=NO, minwidth=0, width=300)
    tree.column('#3', stretch=NO, minwidth=0, width=300)
    tree.column('#4', stretch=NO, minwidth=0, width=350)
    
    tree.pack()
    DisplayData()

def DisplayData():
    Database()
    cursor.execute("SELECT PRODUCT_ID,PRODUCT_NAME,PRODUCT_QTY,PRODUCT_SELLING_PRICE FROM `product`")
    fetch = cursor.fetchall()
    for data in fetch:
        tree.insert('', 'end', values=(data))
    cursor.close()
    conn.close()
  
def Search():
    if SEARCH.get() != "":
        tree.delete(*tree.get_children())
        Database()
        cursor.execute("SELECT PRODUCT_ID,PRODUCT_NAME,PRODUCT_QTY,PRODUCT_SELLING_PRICE FROM `product` WHERE `product_id` LIKE ?", ('%'+str(SEARCH.get())+'%',))
        fetch = cursor.fetchall()
        for data in fetch:
            tree.insert('', 'end', values=(data))
        cursor.close()
        conn.close()

def Reset():
    tree.delete(*tree.get_children())
    DisplayData()
    SEARCH.set("")

def Delete():
    if not tree.selection():
       print("ERROR")
    else:
        result = tkMessageBox.askquestion('Inventory System', 'Are you sure you want to delete this record?', icon="warning")
        if result == 'yes':
            curItem = tree.focus()
            contents =(tree.item(curItem))
            selecteditem = contents['values']
            tree.delete(curItem)
            Database()
            cursor.execute("DELETE FROM `product` WHERE `product_id` = %d" % selecteditem[0])
            conn.commit()
            cursor.close()
            conn.close()
#================================================================================ SHOW USER INVENTORY ==============================================================================================================

def ShowUserView():
    global showuser
    showuser = Toplevel()
    showuser.title("Inventory System/View Product")
    showuser.geometry("800x600")
    
    ShowUser()



def ShowUser():
    
    
    global tree
    global trpoduct
    global tquantity
    global amount
    global enterid
    global productname
    global pprice
    global enteride
    global left
    global right
    global total_l

    left=Frame(showuser,width=700,height=900)
    left.pack(side=LEFT)

    right = Frame(showuser, width=666, height=900,bg='white')
    right.pack(side=RIGHT)
    
        

    #components
    heading=Label(left,text="VIEW PRODUCT",font=('arial 40 bold'))
    heading.place(x=0,y=0)

    date_l=Label(right,text="Today's Date: "+str(date),font=('arial 16 bold'),bg='white')
    date_l.place(x=0,y=0)
    time_l=Label(right, text = "Time : " +str(time),font=('arial 16 bold'),bg='white')
    time_l.place(x=450,y=0)

    #table invoice=======================================================
    tproduct=Label(right,text="Products",font=('arial 18 bold'),bg='white')
    tproduct.place(x=100,y=60)

    tquantity = Label(right, text="Quantity", font=('arial 18 bold'),bg='white')
    tquantity.place(x=300, y=60)

    tamount = Label(right, text="Amount", font=('arial 18 bold'),bg='white')
    tamount.place(x=500, y=60)

    #enter stuff
    enterid=Label(left,text="Enter Product's ID",font=('arial 18 bold'))
    enterid.place(x=0,y=80)


    enteride=Entry(left,textvariable=SEARCH,width=25,font=('arial 18 bold'))
    enteride.place(x=190,y=80)
    enteride.focus()

    #button
    search_btn=Button(left,text="Search",width=22,height=2,command=ajax)
    search_btn.place(x=350,y=120)
    #fill it later by the fuction ajax

    productname=Label(left,text="",font=('arial 27 bold'))
    productname.place(x=0,y=250)

    pprice = Label(left, text="", font=('arial 27 bold'))
    pprice.place(x=0, y=290)

    clearid_btn=Button(left,text="Clear Field",width=22,height=2,command=lambda:clear_id(enteride))
    clearid_btn.place(x=350,y=180)

    #total label
    total_l=Label(right,text="",font=('arial 40 bold'))
    total_l.place(x=0,y=600)
    
def ajax():
    global trpoduct
    global tquantity
    global amount
    global enterid
    global get_name
    global get_stock
    global get_costprice
    global get_price
    global get_totalcostprice
    global get_totalsellingprice
    global productname
    global pprice
    global quantity_l
    global quantity_e
    global discount_l
    global discount_e
    global add_to_cart_btn
    global change_l
    global change_e
    global left
    global right
    
    
    #get the product info with that id and fill i the labels above
    Database()
    cursor.execute("SELECT * FROM `product` WHERE `product_id` LIKE ?", ('%'+str(SEARCH.get())+'%',))
    fetch = cursor.fetchall()
    for r in fetch:
        temp = list(r)
        enterid=temp[0]
        get_name=temp[1]
        get_stock=temp[2]
        get_costprice=temp[3]
        get_price=temp[4]
        get_totalcostprice=temp[5]
        get_totalsellingprice=temp[6]
    productname.configure(text="Product's Name: " +str(get_name))
    pprice.configure(text="Price:RS. "+str(get_price))
    cursor.close()
    conn.close()
    #craete the quantity and the discount label
    quantity_l=Label(left,text="Enter Quantity",font=('arial 18 bold'))
    quantity_l.place(x=0,y=370)

    quantity_e=Entry(left,textvariable=PRODUCT_QTY,width=25,font=('arial 18 bold'))
    quantity_e.place(x=190,y=370)
    quantity_e.focus()

    #discount
    discount_l = Label(left, text="Enter Discount", font=('arial 18 bold'))
    discount_l.place(x=0, y=410)


    discount_e = Entry(left, width=25, font=('arial 18 bold'))
    discount_e.place(x=190, y=410)
    discount_e.insert(END,0)


    #add to cart button
    add_to_cart_btn = Button(left, text="Add to Cart", width=22, height=2,command=lambda:add_to_cart(enterid,get_name,get_stock,get_price,get_costprice,get_totalcostprice,get_totalsellingprice))
    add_to_cart_btn.place(x=350, y=450)

    #genrate bill and change
    change_l=Label(left,text="Given Amount",font=('arial 18 bold'))
    change_l.place(x=0,y=550)

    change_e=Entry(left,width=25,font=('arial 18 bold'))
    change_e.place(x=190,y=550)

    change_btn= Button(left, text="Calculate Change", width=22, height=2,command=change_func)
    change_btn.place(x=350, y=590)

    
    #geneerate bill button
    bill_btn = Button(left, text="Generate Bill", width=100, height=2,command=lambda:generate_bill(enterid,get_name,get_stock,get_price,get_costprice,get_totalcostprice,get_totalsellingprice,change_e))
    bill_btn.place(x=0, y=640)
   
    

def add_to_cart(enterid,get_name,get_stock,get_price,get_costprice,get_totalcostprice,get_totalsellingprice):

    global trpoduct
    global tquantity
    global amount
    global productname
    global pprice
    global quantity_l
    global quantity_e
    global discount_l
    global discount_e
    global add_to_cart_btn
    global change_l
    global change_e
    global left
    global right
    global total_l
    global tempname
    global tempqt
    global tempprice
    
    quantity_value=int(quantity_e.get())
    if  quantity_value >int(get_stock):
        tkinter.messagebox.showinfo("Error","Not that any products in our stock.")
    else:
        #calculate the price first
        final_price=(float(quantity_value) * float(get_price))-(float(discount_e.get()))
        PRODUCT_LIST.append(get_name)
        PRODUCT_SELLING_PRICE.append(final_price)
        PRODUCT_QTY.append(quantity_value)
        PRODUCT_COST_PRICE.append(get_costprice)
        PRODUCT_TOTALCOST_PRICE.append(get_totalcostprice)
        PRODUCT_TOTALSELLING_PRICE.append(get_totalsellingprice)
        PRODUCT_ID.append(enterid)
        

        x_index=0
        y_index=100
        counter=0
        for p in PRODUCT_LIST:
            tempname=Label(right,text=str(PRODUCT_LIST[counter]),font=('arial 18 bold'),bg='white',anchor='center')
            tempname.place(x=100,y=y_index)
            tempqt = Label(right, text=str(PRODUCT_QTY[counter]), font=('arial 18 bold'),bg='white',anchor='center')
            tempqt.place(x=340, y=y_index)
            tempprice = Label(right, text=str(PRODUCT_SELLING_PRICE[counter]), font=('arial 18 bold'),bg='white',anchor='center')
            tempprice.place(x=520, y=y_index)

            y_index+=40
            counter+=1


            #total confugure
            total_l.configure(text="Total : Rs. "+str(sum(PRODUCT_SELLING_PRICE)))
            #delete
            quantity_l.place_forget()
            quantity_e.place_forget()
            discount_l.place_forget()
            discount_e.place_forget()
            productname.configure(text="")
            pprice.configure(text="")
            add_to_cart_btn.destroy()
            #autofocus to the enter id

            
            

def change_func():
    global change_e
    global c_amount
    amount_given=float(change_e.get())
    our_total=float(sum(PRODUCT_SELLING_PRICE))

    to_give=amount_given-our_total

    #label change
    c_amount=Label(left,text="Change: Rs. "+str(to_give),font=('arial 18 bold'))
    c_amount.place(x=0 ,y=600)

def generate_bill(enterid,get_name,get_stock,get_price,get_costprice,get_totalcostprice,get_totalsellingprice,change_e):
    
    x=0
    Database()
    cursor.execute(" SELECT * FROM product WHERE product_id=?"[x])
    fetch=cursor.fetchall()

    for r in fetch:
        temp = list(r)
        get_stock=temp[2]
        get_costprice=temp[3]
        get_price=temp[4]
        get_totalcostprice=temp[5]
        get_totalsellingprice=temp[6]
    for i in PRODUCT_LIST:
        for r in fetch:
            temp = list(r)
            get_stock=temp[2]
            get_costprice=temp[3]
            get_price=temp[4]
            get_totalcostprice=temp[5]
            get_totalsellingprice=temp[6]
      
        
        new_stock = int(get_stock)-int(PRODUCT_QTY[x])
        new_costprice = int(PRODUCT_TOTALCOST_PRICE[x])-int(get_costprice)*int(PRODUCT_QTY[x])
        new_sellingprice =int(PRODUCT_TOTALSELLING_PRICE[x])-int(get_price)*int(PRODUCT_QTY[x])
        #updating the stock
        Database()
        
        sql = "UPDATE product SET product_qty = ?, product_totalcost_price = ? , product_totalselling_price = ?  WHERE product_id = ? "
        cursor.execute(sql,(new_stock,new_costprice,new_sellingprice,PRODUCT_ID[x]))
   
        conn.commit()
        cursor.close()
        conn.close()

        #inster into transcation
        Database()
        sql2="INSERT INTO transactions (product_name,product_quantity,product_amount,product_date) VALUES(?,?,?,?)"
        cursor.execute(sql2,(PRODUCT_LIST[x],PRODUCT_QTY[x],PRODUCT_SELLING_PRICE[x],date))
        conn.commit()
        print("Decreased")
        x+=1
        Clear_bill()

        

        
        


        

    
    


def Quantity():
    if PRODUCT_QTY.get() != "":
        tree.delete(*tree.get_children())
        Database()
        cursor.execute("SELECT * FROM `product` WHERE `product_qty`=%s", ('%'+str(PRODUCT_QTY.get())+'%',))
        fetch = cursor.fetchall()
        for data in fetch:
            tree.insert('', 'end', values=(data))
        cursor.close()
        conn.close()

def clear_id(enteride):

    enteride.delete(0,END)
    
def Clear_bill():

        global enteride
        global tempname
        global tempqt
        global tempprice
        global c_amount
        global total_l
        global change_l
        global change_e

        tempname.configure(text="")
        tempqt.configure(text="")
        tempprice.configure(text="")
        c_amount.configure(text="")
        total_l.configure(text="")
        change_l.configure(text="")
        change_e.place_forget()
        enteride.delete(0,END)
        
#=============================================================================== MAIN PAGE ================================================================================#

def ShowHome():
    root.withdraw()
    Home()
    loginform.destroy()

menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Account", command=ShowLoginForm)
filemenu.add_command(label="Exit", command=Exit)
menubar.add_cascade(label="File", menu=filemenu)
root.config(menu=menubar)

Title = Frame(root, bd=1, relief=SOLID)
Title.pack(pady=10)

lbl_display = Label(Title, text="Inventory System", font=('arial', 45))
lbl_display.pack(side=TOP, padx=20, pady=20, fill=X)

if __name__ == '__main__':
    root.mainloop()


#================================================================================ THANKYOU  =======================================================================================#


