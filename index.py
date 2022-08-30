from tkinter import ttk
from tkinter import *

import sqlite3
from unittest import result

class Payroll:
    db_name = 'database.db'

    def __init__(self, window):
        self.wind = window
        self.wind.title('Nomina')

        frame = LabelFrame(self.wind, text = 'registre su informacion de nomina')
        frame.grid(row = 0, column = 0, columnspan = 5, pady = 20)

        Label(frame, text = 'name: ').grid(row=1, column=0)
        self.name = Entry(frame)

        self.name.grid(row=1, column=1)

        Label(frame, text = 'last name: ').grid(row=2, column=0)
        self.lastName = Entry(frame)
        self.lastName.grid(row=2, column=1)

        Label(frame, text = 'IdDocument: ').grid(row=3, column=0)
        self.idDocument = Entry(frame)
        self.idDocument.grid(row=3, column=1)

        Label(frame, text = 'Salary ').grid(row=4, column=0)
        self.salary = Entry(frame)
        self.salary.grid(row=4, column=1)

        Label(frame, text = 'Worked days ').grid(row=5, column=0)
        self.WorkedDays = Entry(frame)
        self.WorkedDays.grid(row=5, column=1)

        #boton
        ttk.Button(frame, text= 'ENVIAR INFORMACION', command= self.add_information).grid(row=6, columnspan=5, sticky= W + E)
        
        # salida mensajes

        self.message = Label(text= '', fg = 'red')
        self.message.grid(row=3, column=0, columnspan=2, sticky= W + E)

        self.tree =ttk.Treeview(height=10, columns= ('#1','#2','#3','#4','#5'))
        self.tree.grid(row=10, column=0, columnspan=10)
        self.tree.heading('#1', text='name', anchor= CENTER)
        self.tree.heading('#2', text='last name', anchor= CENTER)
        self.tree.heading('#3', text='IdDocument', anchor= CENTER)
        self.tree.heading('#4', text='Salary', anchor= CENTER)
        self.tree.heading('#5', text='Worked Days', anchor= CENTER)

        #botones
        ttk.Button(text = 'DELETE', command= self.delete_information).grid(row = 5, column = 0, sticky= W + E)
        ttk.Button(text = 'UPDATE', command= self.edit_information).grid(row = 5, column = 1, sticky= W + E)

        self.get_information()

    def run_query(self, query, parameters = ()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result

    def get_information(self):
        #limpiar tabla
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        #consultar datos
        query ='SELECT * FROM Payroll ORDER BY name DESC'
        db_rows = self.run_query(query)
        for row in db_rows:
           self.tree.insert('', 0, text = row[1], values=row[5] ) 

    def validation(self):
        return len(self.name.get()) != 0 and len(self.lastName.get()) != 0 and len(self.idDocument.get()) != 0 and len(self.salary.get()) != 0 and len(self.WorkedDays.get()) != 0

    def add_information(self):
        if self.validation():
            query = 'INSERT INTO Payroll VALUES(NULL, ?, ?, ?, ?, ?)'
            parameters = (self.name.get(), self.lastName.get(), self.idDocument.get(), self.salary.get(), self.WorkedDays.get())
            self.run_query(query, parameters)
            self.message['text'] = 'Product {} added succesfully'.format(self.name.get())
            self.name.delete(0, END)
            self.lastName.delete(0, END)
            self.idDocument.delete(0, END)
            self.salary.delete(0, END)
            self.WorkedDays.delete(0, END)
        else:
            self.message['text'] = 'Name and last name are required'
        self.get_information()

    def delete_information(self):
        self.message['text'] = 'please select a record'
        try:
            self.tree.item(self.tree.selection())['text']
        except IndexError as e:
            self.message['text'] = 'please select a record'
            return
        self.message['text'] = ''
        name = self.tree.item(self.tree.selection()) ['text'][0]
        query = 'DELETE FROM Payroll WHERE name = ?'
        self.run_query(query, (name,))
        self.message['text'] = 'record {} deleted succesfully'.format(format(name))
        self.get_information()

    def edit_information(self):
        self.message['text'] = 'please select a record'
        try:
            self.tree.item(self.tree.selection())['text']
        except IndexError as e:
            self.message['text'] = 'please select a record'
            return
        name = self.tree.item (self.tree.selection())['text']
        lastName = self.tree.item (self.tree.selection())['values'][0]
        self.edit_wind = Toplevel()
        self.edit_wind.title = 'edit information'

    #datos antiguos
        Label (self.edit_wind, text = 'old name: ').grid(row = 0, column = 1)
        Entry (self.edit_wind, textvariable = StringVar(self.edit_wind, value = name), state='readonly').grid(row = 0, column=2)
    # datos nuevos
        Label (self.edit_wind, text = 'New name: ').grid(row = 1, column = 1)
        new_name = Entry (self.edit_wind)
        new_name.grid(row= 1, column=2)

        Label (self.edit_wind, text = 'Old last name: ').grid(row = 2, column = 1)
        Entry (self.edit_wind, textvariable = StringVar(self.edit_wind, value = lastName), state='readonly').grid(row = 2, column=2)

        Label (self.edit_wind, text = 'New last name: ').grid(row = 3, column = 1)
        new_last_name = Entry (self.edit_wind)
        new_last_name.grid(row= 3, column=2)
if __name__ == '__main__':
    window = Tk()
    application = Payroll(window)
    window.mainloop()
