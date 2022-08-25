from select import select
from tkinter import *
from tkinter import ttk
from tkinter.tix import NoteBook, Select
import sqlite3
from turtle import width

window = Tk()
window.geometry("800x650")

notebook = ttk.Notebook(window)

tab1 = Frame(notebook)
tab2 = Frame(notebook)


notebook.add(tab1, text="Passenger vehicles")
notebook.add(tab2, text="Cargo vehicles")
notebook.pack(expand=True, fill="both")

# -----------------------------------------------
# TAB 1----------------

frame1 = LabelFrame(tab1, text="Search", width=423, height=604, padx=7,)
frame2 = LabelFrame(tab1, text="Assign/Release", width=330, height=200, padx=7,)
frame3 = LabelFrame(tab1, text="Add a new vehicle", width=330, height=200,)
frame4 = LabelFrame(tab1, text="Delete a vehicle", width=330, height=146,)

frame1.grid(row=0, column=0, rowspan=3, padx=10, pady=10)
frame1.grid_propagate(False)
frame2.grid(row=0, column=1,)
frame2.grid_propagate(False)
frame3.grid(row=1, column=1,)
frame3.grid_propagate(False)
frame4.grid(row=2, column=1,)
frame4.grid_propagate(False)


# labals

num_of_passengers_label = Label(frame1, text="Enter number of passengers",)
num_of_passengers_label.grid(row=1, column=0, sticky=W)
ac_condition_label = Label(frame1, text="Ac or no-AC ?",)
ac_condition_label.grid(row=2, column=0, sticky=W)

# input boxes and List
clicked2 = IntVar()
clicked2.set('1')
clicked3 = StringVar()
clicked3.set('yes')
drop = OptionMenu(frame1, clicked2, 1, 2, 3, 4, 5, 6, 7, 8,)
drop.grid(row=1, column=0, sticky=E,)
drop = OptionMenu(frame1, clicked3, 'yes', 'no',)
drop.grid(row=2, column=0, sticky=E,)

def filter():
    conn = sqlite3.connect('cabService.db')
    c = conn.cursor()
    my_tree.delete(*my_tree.get_children())

    clicked_passengers = clicked2.get()
    clicked_ac = clicked3.get()

    if clicked_ac == 'yes':
        sql='''SELECT passengerVehicles.vehicle_Id,vehicle_type,vehicle_modal,max_passengers
                FROM passengerVehicles
                LEFT JOIN job on passengerVehicles.vehicle_Id = job.vehicle_Id
                where job.vehicle_Id is null
                AND max_passengers >=(?) AND AC = (?)'''
        c.execute(sql,(clicked_passengers,clicked_ac))
        items = c.fetchall()
        count = 0
        for item in items:

            my_tree.insert(parent='', index='end', iid=count, text="Parent", values=(
                item[0], item[1], item[2], item[3])),
            count += 1

    else:
        sql= '''SELECT passengerVehicles.vehicle_Id,vehicle_type,vehicle_modal,max_passengers
                FROM passengerVehicles
                LEFT JOIN job on passengerVehicles.vehicle_Id = job.vehicle_Id
                where job.vehicle_Id is null
                AND max_passengers >=(?)'''
        c.execute(sql,(clicked_passengers,))
        items = c.fetchall()
        count = 0
        for item in items:

            my_tree.insert(parent='', index='end', iid=count, text="Parent", values=(
                item[0], item[1], item[2], item[3])),
            count += 1


def showallp():
    conn = sqlite3.connect('cabService.db')
    c = conn.cursor()
    my_tree.delete(*my_tree.get_children())

    sql= '''SELECT passengerVehicles.vehicle_Id,vehicle_type,vehicle_modal,max_passengers
                FROM passengerVehicles
                LEFT JOIN job on passengerVehicles.vehicle_Id = job.vehicle_Id
                where job.vehicle_Id is null'''

    c.execute(sql)
    items = c.fetchall()

    count = 0

    for item in items:
        my_tree.insert(parent='', index='end', iid=count, text="Parent", values=(
        item[0], item[1], item[2], item[3])),
        count += 1



    



# Filter button
myButton = Button(frame1, text="Filter", command=filter,
                  justify=LEFT, anchor="w",bg='light blue',width=7)
myButton.grid(row=3, column=0, sticky=W, pady=1)

showallButton = Button(frame1, text="Show all",
                       command=showallp, justify=LEFT, anchor="w",bg="#f05b6a")
showallButton.grid(row=3, column=0, sticky=E, pady=10)


# Tree viwe
my_tree = ttk.Treeview(frame1)


# define colomns
my_tree['columns'] = ("Vehicle Id", "Vehicle type",
                      "Vehicle model", "Max passengers")

# format colomns
my_tree.column("#0", width=0, stretch=NO)
my_tree.column("Vehicle Id", anchor=W, width=100)
my_tree.column("Vehicle type", anchor=CENTER, width=100)
my_tree.column("Vehicle model", anchor=W, width=100)
my_tree.column("Max passengers", anchor=W, width=100)


# Create Headings
my_tree.heading("#0", text="Label", anchor=W)
my_tree.heading("Vehicle Id", text="Vehicle Id", anchor=W)
my_tree.heading("Vehicle type", text="Vehicle type", anchor=CENTER)
my_tree.heading("Vehicle model", text="Vehicle model", anchor=W)
my_tree.heading("Max passengers", text="Max passengers", anchor=W)

my_tree.grid(row=4, column=0, sticky=W)


# frame2---------------

enter_vehicle_id = Label(frame2, text="Enter vehicle id",)
enter_vehicle_id.grid(row=0, column=0, sticky=W)
enter_customer_id = Label(frame2, text="Enter customer id")
enter_customer_id.grid(row=1, column=0,)

input_vehicle_id = Entry(frame2, width=20,)
input_vehicle_id.grid(row=0, column=1, padx=40)

input_customer_id = Entry(frame2, width=20)
input_customer_id.grid(row=1, column=1, padx=40)

def assign():
    conn = sqlite3.connect('cabService.db')
    c = conn.cursor()
    select_job = conn.cursor()
    get_vehicle_id = int(input_vehicle_id.get())
    

    sql = 'INSERT INTO job VALUES (:vehicle_id,:customer_id)'
    sql_get_vehical_id = '''SELECT job.vehicle_Id,vehicle_modal,customer_Id
                                FROM passengerVehicles
                                INNER JOIN job ON passengerVehicles.vehicle_Id=job.vehicle_Id
                                WHERE job.vehicle_Id = (?)'''

    c.execute(sql,{'vehicle_id':int(input_vehicle_id.get()),'customer_id':int(input_customer_id.get())})
    select_job.execute(sql_get_vehical_id,(get_vehicle_id,))
    
    items = select_job.fetchall()
    print(items)


    

    conn.commit()
    conn.close()


    enter_vehicle_id = Label(frame2, text="successfully assigned",fg='blue')
    enter_vehicle_id.grid(row=4, column=0)

    enter_vehicle_id = Label(frame2, text="**-details-**",fg='red')
    enter_vehicle_id.grid(row=5, column=0)

    labal_vehicle_id = Label(frame2, text="vehicle id: ",fg='red')
    labal_vehicle_id.grid(row=6, column=0)
    labal_vehicle_modal = Label(frame2, text="vehicle_model: ",fg='red')
    labal_vehicle_modal.grid(row=7, column=0)
    labal_customer_id = Label(frame2, text="customer_id: ",fg='red')
    labal_customer_id.grid(row=8, column=0)

    show_vehicle_id = Label(frame2, text=items[0][0],fg='green')
    show_vehicle_id.grid(row=6, column=1,padx=4)
    show_vehicle_modal = Label(frame2, text=items[0][1],fg='green')
    show_vehicle_modal.grid(row=7, column=1,padx=4)
    show_customer_id = Label(frame2, text=items[0][2],fg='green')
    show_customer_id.grid(row=8, column=1,padx=4)

def release():
    conn = sqlite3.connect('cabService.db')
    c = conn.cursor()
    select_job = conn.cursor()
    get_vehicle_id = int(input_vehicle_id.get())
    

    sql = 'DELETE FROM job WHERE vehicle_Id=(?)'
    sql_get_vehical_id = '''SELECT vehicle_Id,vehicle_modal
                                FROM passengerVehicles
                                WHERE vehicle_Id = (?)'''

    c.execute(sql,(get_vehicle_id,))
    select_job.execute(sql_get_vehical_id,(get_vehicle_id,))
    
    items = select_job.fetchall()
    print(items)


    

    conn.commit()
    conn.close()


    enter_vehicle_id = Label(frame2, text="successfully relesed ",fg='red')
    enter_vehicle_id.grid(row=4, column=0)

    enter_vehicle_id = Label(frame2, text="**-details-**",fg='red')
    enter_vehicle_id.grid(row=5, column=0)

    labal_vehicle_id = Label(frame2, text="vehicle id: ",fg='green')
    labal_vehicle_id.grid(row=6, column=0)
    labal_vehicle_modal = Label(frame2, text="vehicle_model: ",fg='green')
    labal_vehicle_modal.grid(row=7, column=0)
    labal_customer_id = Label(frame2, text="**************",fg='green')
    labal_customer_id.grid(row=8, column=0)

    show_vehicle_id = Label(frame2, text=items[0][0],fg='green')
    show_vehicle_id.grid(row=6, column=1,padx=4)
    show_vehicle_modal = Label(frame2, text=items[0][1],fg='green')
    show_vehicle_modal.grid(row=7, column=1,padx=4)
    show_customer_id = Label(frame2, text="*******",fg='green')
    show_customer_id.grid(row=8, column=1,padx=4)





# Hire buttons
assign_Button = Button(frame2, text="Assign", width=10,command=assign,bg='light blue',)
assign_Button.grid(row=3, column=0, sticky=W,pady=2)
release_Button = Button(frame2, text="Release", width=10,command=release,bg="#f05b6a",)
release_Button.grid(row=3, column=1, )



# frame3---------------

select_vehicle_type = Label(frame3, text="Select vehicle type",)
select_vehicle_type.grid(row=0, column=0, sticky=W)
enter_vehicle_model = Label(frame3, text="Enter vehicle model",)
enter_vehicle_model.grid(row=1, column=0, sticky=W)
select_ac_condition = Label(frame3, text="Ac condition type",)
select_ac_condition.grid(row=2, column=0, sticky=W)
select_ac_no_of = Label(frame3, text="Maximum number of passengers",)
select_ac_no_of.grid(row=3, column=0, sticky=W)

clickedCarType = StringVar()
clickedCarType.set('car')
clickedac = StringVar()
clickedac.set('yes')

drop_car_type = OptionMenu(frame3,clickedCarType,'car','van','three wheel')
drop_car_type.grid(row=0, column=1)

input_new_vehicle_modal = Entry(frame3, width=15)
input_new_vehicle_modal.grid(row=1, column=1,)

drop_ac = OptionMenu(frame3,clickedac,'yes','no',)
drop_ac.grid(row=2, column=1,)

input_new_max_pass = Entry(frame3, width=15)
input_new_max_pass.grid(row=3, column=1,)


def enter():
    conn = sqlite3.connect('cabService.db')
    c = conn.cursor()

    modal = input_new_vehicle_modal.get()
    max_pass = input_new_max_pass.get()

    print(clickedCarType)
    print(modal)
    print(clickedac)
    print(max_pass)

    sql = ''' INSERT INTO passengerVehicles (vehicle_type, vehicle_modal, AC, max_passengers)
            VALUES ((?),(?),(?),(?))'''

    c.execute(sql,(clickedCarType.get(),modal,clickedac.get(),max_pass))
    conn.commit()
    conn.close()

    select_vehicle_type = Label(frame3, text="Succsessfully added a new vehicle",)
    select_vehicle_type.grid(row=5, column=0,)




submit_Button = Button(frame3, text="Submit", width=10,command=enter,bg='#90fcad')
submit_Button.grid(row=4, column=0, sticky=W)


# frame 4








detele_id = Label(frame4, text="Enter Vehicle Id",)
detele_id.grid(row=0, column=0, sticky=W)



Enter_dele_vehi_id = Entry(frame4, width=15)
Enter_dele_vehi_id.grid(row=0, column=1,)

def deleteq():
    conn = sqlite3.connect('cabService.db')
    c = conn.cursor()

    sql = '''DELETE FROM passengerVehicles WHERE vehicle_Id = (?)'''
    c.execute(sql,(Enter_dele_vehi_id.get(),))

    detele_id = Label(frame4, text="Succsessfully deleted: vehicle id : " + str(Enter_dele_vehi_id.get()),fg='red')
    detele_id.grid(row=2, column=0, sticky=W)

    
    conn.commit()
    conn.close()



delete_Button = Button(frame4, text="Delete", width=10,command=deleteq,bg='red')
delete_Button.grid(row=1, column=0, sticky=W)



# Tab 2 ----------------------------------------------------------------------
frame11 = LabelFrame(tab2, text="Search", width=423, height=604, padx=7,)
frame22 = LabelFrame(tab2, text="Assign/Release", width=330, height=195, padx=7,)
frame33 = LabelFrame(tab2, text="Add a new vehicle", width=330, height=200,)
frame44 = LabelFrame(tab2, text="Delete a vehicle", width=330, height=146,)

frame11.grid(row=0, column=0, rowspan=3, padx=10, pady=10)
frame11.grid_propagate(False)
frame22.grid(row=0, column=1,)
frame22.grid_propagate(False)
frame33.grid(row=1, column=1,)
frame33.grid_propagate(False)
frame44.grid(row=2, column=1,)
frame44.grid_propagate(False)

# labals

select_cargo_type = Label(frame11, text="Select vehicle type (cargo)",)
select_cargo_type.grid(row=1, column=0, sticky=W)
vr_label1 = Label(frame11, text="Enter maximum size(ft)",)
vr_label1.grid(row=2, column=0, sticky=W)
vr_label2 = Label(frame11, text="Enter load size(kg)",)
vr_label2.grid(row=3, column=0, sticky=W)

# input boxes and List

clicked33 = StringVar()
clicked33.set('lorry')
display1 = "disabled"
display2 = "normal"

def change_state_size(state='disabled'):
    enter_load.config(state=state)
    
def change_state_load(state='disabled'):
    enter_size.config(state=state)

def abc(*args):
    if clicked33.get() == 'lorry':
        change_state_size(state='normal')
        change_state_load(state='disabled')
    elif clicked33.get() == 'truck':
        change_state_size(state='disabled')
        change_state_load(state='normal')
        
   


drop = OptionMenu(frame11, clicked33,'truck', 'lorry',command=abc)
drop.grid(row=1, column=0,)





enter_size = Entry(frame11, width=15,state= display1)
enter_size.grid(row=2, column=0,)

enter_load = Entry(frame11, width=15,state= display2)
enter_load.grid(row=3, column=0,)


def filterCargo():
    if clicked33.get() == 'truck':

        conn = sqlite3.connect('cabService.db')
        c = conn.cursor()
        my_tree11.delete(*my_tree11.get_children())

        sql1truck = ''' SELECT cargoVehicles.vehicle_Id,vehicle_type,vehicle_modal,max_size 
                        FROM cargoVehicles
                        LEFT JOIN cargoJob on cargoVehicles.vehicle_Id = cargoJob.vehicle_Id
                        where cargoJob.vehicle_Id is null 
                        and max_size >=(?) '''

        c.execute(sql1truck,(enter_size.get(),))
        items = c.fetchall()
        count = 0

        for item in items:
            my_tree11.insert(parent='', index='end', iid=count, text="Parent", values=(
            item[0], item[1], item[2], str(item[3]) + " ft")),
            count += 1
    elif clicked33.get() == 'lorry': 

        conn = sqlite3.connect('cabService.db')
        c = conn.cursor()
        my_tree11.delete(*my_tree11.get_children())

        sql1truck = '''SELECT cargoVehicles.vehicle_Id,vehicle_type,vehicle_modal,max_load
                        FROM cargoVehicles
                        LEFT JOIN cargoJob on cargoVehicles.vehicle_Id = cargoJob.vehicle_Id
                        where cargoJob.vehicle_Id is null 
                        and max_load >=(?) '''

        c.execute(sql1truck,(enter_load.get(),))
        items = c.fetchall()
        count = 0

        for item in items:
            my_tree11.insert(parent='', index='end', iid=count, text="Parent", values=(
            item[0], item[1], item[2], str(item[3]) + " kg")),
            count += 1

def show():
    if clicked33.get() == 'truck':

        conn = sqlite3.connect('cabService.db')
        c = conn.cursor()
        my_tree11.delete(*my_tree11.get_children())

        sql1truck = '''SELECT cargoVehicles.vehicle_Id,vehicle_type,vehicle_modal,max_size 
                        FROM cargoVehicles
                        LEFT JOIN cargoJob on cargoVehicles.vehicle_Id = cargoJob.vehicle_Id
                        where cargoJob.vehicle_Id is null 
                        and max_size >=1 '''

        c.execute(sql1truck)
        items = c.fetchall()
        count = 0

        for item in items:
            my_tree11.insert(parent='', index='end', iid=count, text="Parent", values=(
            item[0], item[1], item[2], str(item[3]) + " ft")),
            count += 1
    elif clicked33.get() == 'lorry': 

        conn = sqlite3.connect('cabService.db')
        c = conn.cursor()
        my_tree11.delete(*my_tree11.get_children())

        sql1truck = '''SELECT cargoVehicles.vehicle_Id,vehicle_type,vehicle_modal,max_load
                        FROM cargoVehicles
                        LEFT JOIN cargoJob on cargoVehicles.vehicle_Id = cargoJob.vehicle_Id
                        where cargoJob.vehicle_Id is null 
                        and max_load >=1 '''

        c.execute(sql1truck)
        items = c.fetchall()
        count = 0

        for item in items:
            my_tree11.insert(parent='', index='end', iid=count, text="Parent", values=(
            item[0], item[1], item[2], str(item[3]) + " kg")),
            count += 1
    
   










filter_button11= Button(frame11, text="Filter", width=10,command=filterCargo,bg='light blue')
filter_button11.grid(row=4, column=0, sticky=W)
filter_button111= Button(frame11, text="Show all", width=10, command=show,bg='#f05b6a')
filter_button111.grid(row=4, column=0,sticky=E, pady=10)

# Tree viwe 2
my_tree11 = ttk.Treeview(frame11)

# define colomns
my_tree11['columns'] = ("Vehicle Id", "Vehicle type",
                      "Vehicle model", "Max passengers")

# format colomns
my_tree11.column("#0", width=0, stretch=NO)
my_tree11.column("Vehicle Id", anchor=W, width=100)
my_tree11.column("Vehicle type", anchor=CENTER, width=100)
my_tree11.column("Vehicle model", anchor=W, width=100)
my_tree11.column("Max passengers", anchor=W, width=100)


# Create Headings
my_tree11.heading("#0", text="Label", anchor=W)
my_tree11.heading("Vehicle Id", text="Vehicle Id", anchor=W)
my_tree11.heading("Vehicle type", text="Vehicle type", anchor=CENTER)
my_tree11.heading("Vehicle model", text="Vehicle model", anchor=W)
my_tree11.heading("Max passengers", text="Max load/size", anchor=W)

my_tree11.grid(row=5, column=0, sticky=W,pady=10)

#frame 22



enter_cargo_id = Label(frame22, text="Enter vehicle id",)
enter_cargo_id.grid(row=0, column=0, sticky=W)
enter_customer_id_cargo = Label(frame22, text="Enter customer id")
enter_customer_id_cargo.grid(row=1, column=0,)

input_vehicle_id_cargo = Entry(frame22, width=20,)
input_vehicle_id_cargo.grid(row=0, column=1, padx=40)
input_customer_id_cargo = Entry(frame22, width=20)
input_customer_id_cargo.grid(row=1, column=1, padx=40)

def assignCargo():
    conn = sqlite3.connect('cabService.db')
    c = conn.cursor()
    select_job = conn.cursor()
    get_vehicle_id = int(input_vehicle_id_cargo.get())
    

    sql = 'INSERT INTO cargoJob VALUES (:vehicle_id,:customer_id)'
    sql_get_vehical_id = '''SELECT cargoJob.vehicle_Id,vehicle_modal,customer_Id
                                FROM cargoVehicles
                                INNER JOIN cargoJob ON cargoVehicles.vehicle_Id=cargoJob.vehicle_Id
                                WHERE cargoJob.vehicle_Id = (?)'''

    c.execute(sql,{'vehicle_id':int(input_vehicle_id_cargo.get()),'customer_id':int(input_customer_id_cargo.get())})
    
    select_job.execute(sql_get_vehical_id,(get_vehicle_id,))
    
    items = select_job.fetchall()
    print(items)


    

    conn.commit()
    conn.close()


    enter_vehicle_id = Label(frame22, text="successfully assigned",fg='red')
    enter_vehicle_id.grid(row=4, column=0)

    enter_vehicle_id = Label(frame22, text="**-details-**",fg='blue')
    enter_vehicle_id.grid(row=5, column=0)

    labal_vehicle_id = Label(frame22, text="vehicle id: ",fg='#02c45a')
    labal_vehicle_id.grid(row=6, column=0)
    labal_vehicle_modal = Label(frame22, text="vehicle_model: ",fg='#02c45a')
    labal_vehicle_modal.grid(row=7, column=0)
    labal_customer_id = Label(frame22, text="customer_id: ",fg='#02c45a')
    labal_customer_id.grid(row=8, column=0)

    show_vehicle_id = Label(frame22, text=items[0][0],fg='#02c45a')
    show_vehicle_id.grid(row=6, column=1,padx=4)
    show_vehicle_modal = Label(frame22, text=items[0][1],fg='#02c45a')
    show_vehicle_modal.grid(row=7, column=1,padx=4)
    show_customer_id = Label(frame22, text=items[0][2],fg='#02c45a')
    show_customer_id.grid(row=8, column=1,padx=4)

def realseCargo():
    conn = sqlite3.connect('cabService.db')
    c = conn.cursor()
    select_job = conn.cursor()
    get_vehicle_id = int(input_vehicle_id_cargo.get())
    

    sql = 'DELETE FROM cargoJob WHERE vehicle_Id=(?)'
    sql_get_vehical_id = '''SELECT vehicle_Id,vehicle_modal
                                FROM cargoVehicles
                                WHERE vehicle_Id = (?)'''

    c.execute(sql,(get_vehicle_id,))
    
    select_job.execute(sql_get_vehical_id,(get_vehicle_id,))
    
    items = select_job.fetchall()
    print(items)


    

    conn.commit()
    conn.close()


    enter_vehicle_id = Label(frame22, text="successfully relaesed",fg='red')
    enter_vehicle_id.grid(row=4, column=0)

    enter_vehicle_id = Label(frame22, text="**-details-**",fg='blue')
    enter_vehicle_id.grid(row=5, column=0)

    labal_vehicle_id = Label(frame22, text="vehicle id: ",fg='#02c45a')
    labal_vehicle_id.grid(row=6, column=0)
    labal_vehicle_modal = Label(frame22, text="vehicle_model: ",fg='#02c45a')
    labal_vehicle_modal.grid(row=7, column=0)
    labal_customer_id = Label(frame22, text="**************",fg='#02c45a')
    labal_customer_id.grid(row=8, column=0)

    show_vehicle_id = Label(frame22, text=items[0][0],fg='#02c45a')
    show_vehicle_id.grid(row=6, column=1,padx=4)
    show_vehicle_modal = Label(frame22, text=items[0][1],fg='#02c45a')
    show_vehicle_modal.grid(row=7, column=1,padx=4)
    
    
# Hire buttons
assign_Button_cargo = Button(frame22, text="Assign", width=10,command=assignCargo,bg='light blue')
assign_Button_cargo.grid(row=3, column=0, sticky=W,)
release_Button_cargo = Button(frame22, text="Release", width=10,command=realseCargo,bg='#f05b6a')
release_Button_cargo.grid(row=3, column=1, )

# frame 33------------------------



select_vehicle_type_cargo = Label(frame33, text="Select vehicle type",)
select_vehicle_type_cargo.grid(row=0, column=0, sticky=W)
enter_vehicle_model_cargo = Label(frame33, text="Enter vehicle model",)
enter_vehicle_model_cargo.grid(row=1, column=0, sticky=W)

select_ac_no_of_cargo1 = Label(frame33, text="Enter maximum size(ft)",)
select_ac_no_of_cargo1.grid(row=3, column=0, sticky=W)

select_ac_no_of_cargo2 = Label(frame33, text="Enter maximum load(kg)",)
select_ac_no_of_cargo2.grid(row=4, column=0, sticky=W)

clickedCarType_c = StringVar()
clickedCarType_c.set('truck')
display11 = "normal"
display22 = "disabled"



def change_state_size_cargo(state='disabled'):
    cargo_size.config(state=state)
    
def change_state_load_cargo(state='disabled'):
    load_cargo_size.config(state=state)

def abc_cargo(*args):
    if clickedCarType_c.get() == 'truck':
        change_state_size_cargo(state='normal')
        change_state_load_cargo(state='disabled')
    elif clickedCarType_c.get() == 'lorry':
        change_state_size_cargo(state='disabled')
        change_state_load_cargo(state='normal')



drop_car_type = OptionMenu(frame33,clickedCarType_c,'truck','lorry',command=abc_cargo)
drop_car_type.grid(row=0, column=1)

input_new_vehicle_modal_cargo = Entry(frame33, width=15)
input_new_vehicle_modal_cargo.grid(row=1, column=1,)

cargo_size = Entry(frame33, width=15,state=display11)
cargo_size.grid(row=3, column=1,)
load_cargo_size = Entry(frame33, width=15,state=display22)
load_cargo_size.grid(row=4, column=1,)



def enterc():
    conn = sqlite3.connect('cabService.db')
    c = conn.cursor()

    get_modal = input_new_vehicle_modal_cargo.get()
    get_cargo_size = cargo_size.get()
    get_load = load_cargo_size.get()


    if clickedCarType_c.get() == 'truck':
        sql = ''' INSERT INTO cargoVehicles (vehicle_type, vehicle_modal, max_size)
            VALUES ((?),(?),(?))'''
        c.execute(sql,(clickedCarType_c.get(),get_modal,get_cargo_size,))



    elif clickedCarType_c.get() == 'lorry':
        sql = ''' INSERT INTO cargoVehicles (vehicle_type, vehicle_modal, max_load)
            VALUES ((?),(?),(?))'''
        c.execute(sql,(clickedCarType_c.get(),get_modal,get_load,))
    


    conn.commit()
    conn.close()

    
    l= Label(frame33, text="succsessfully Enterd new vehicle",fg='green')
    l.grid(row=6, column=0)



enterrcargo = Button(frame33, text="Submit", width=10,command=enterc,bg='#42f593')
enterrcargo.grid(row=5, column=0,)


# frame 44






detele_id_cargo = Label(frame44, text="Enter Vehicle Id",)
detele_id_cargo.grid(row=0, column=0, sticky=W)

Enter_dele_vehi_id_cargo = Entry(frame44, width=15)
Enter_dele_vehi_id_cargo.grid(row=0, column=1,)

def delete():

    conn = sqlite3.connect('cabService.db')
    c = conn.cursor()

    sql="DELETE FROM cargoVehicles WHERE vehicle_Id = (?)"
    c.execute(sql,(Enter_dele_vehi_id_cargo.get(),))

    conn.commit()
    conn.close()

    
    l=Label(frame44, text="successfully removed vehicle id : " + Enter_dele_vehi_id_cargo.get(),fg='red')
    l.grid(row=2, column=0, sticky=W)









delete_Button_cargo = Button(frame44, text="Delete", width=10,command=delete,bg='red')
delete_Button_cargo.grid(row=1, column=0, sticky=W)









window.mainloop()
