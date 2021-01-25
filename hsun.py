# -*- coding: utf-8 -*-
"""
Created on Sat Jan 23 12:10:07 2021

@author: Juan
"""

from tkinter import *
from tkinter import ttk
from ttkthemes import ThemedTk
import os
import sqlite3

class inf():
    bd = sqlite3.connect('bd.db')
    cursor = bd.cursor()
    cursor.execute("create table if not exists historia (id INTEGER PRIMARY KEY AUTOINCREMENT, Nombre TEXT, Creditos INTEGER, Calificacion REAL)")
    def nuevo(item, posx, posy):
        nombre = inf.cursor.execute("SELECT " + item + " FROM registro").fetchall()[0][0]
        estudiante = Label(informacion, text = "{}: {}".format(item, nombre)) 
        estudiante.place(x = posx, y = posy)
        estudiante.config(bg = 'snow')
    
    def progreso(posx, posy):
        total = inf.cursor.execute("SELECT Creditos FROM registro").fetchall()[0][0]
        prog = inf.cursor.execute("SELECT Creditos FROM historia WHERE Calificacion >= 3.0").fetchall()
        suma = 0
        for credito in prog:
            suma += credito[0]
        progreso = round(suma/total*100,2)
        avance = Label(informacion, text = "Progreso: {}%".format(progreso)) 
        avance.place(x = posx, y = posy)
        avance.config(bg = 'snow')
        
    def boton(texto, posx, posy, comando = 0):
        boton = ttk.Button(principal, text=texto, command = comando)
        boton.place(x = posx, y = posy)
    
    def etiqueta(ventana, texto, posx, posy, fondo = 'dark slate gray', letra = 'floral white'):
        titulo = Label(ventana, text = texto, font = ("Arial", 11)) 
        titulo.place(x = posx, y = posy, anchor = 'center')
        titulo.config(bg = fondo, fg = letra)
        
    def promedio(posx, posy):
        resultado = inf.cursor.execute("SELECT Creditos, Calificacion FROM historia WHERE Calificacion > 3.0").fetchall()
        suma = 0
        total = 0
        for materia in resultado:
            suma += materia[0] * materia[1]
            total += materia[0]
        if total != 0:
            prom = round(suma/total,2)
        else:
            prom = "N.A"
        pa = Label(informacion, text = "Promedio Académico: {}".format(prom))
        pa.place(x = posx, y = posy)
        pa.config(bg = 'snow')

    def papa(posx, posy):
        resultado = inf.cursor.execute("SELECT Creditos, Calificacion FROM historia").fetchall()
        suma = 0
        total = 0
        for materia in resultado:
            suma += materia[0] * materia[1]
            total += materia[0]
        if total != 0:
            prom = round(suma/total,1)
        else:
            prom = "N.A"
        pa = Label(informacion, text = "P.A.P.A: {}".format(prom))
        pa.place(x = posx, y = posy)
        pa.config(bg = 'snow')
        
def agregar():
    clase = materia.get()
    cal = nota.get()
    cred = creditos.get()
    bd = sqlite3.connect('bd.db')
    cursor = bd.cursor()
    cursor.execute("INSERT INTO historia (Nombre, Creditos, Calificacion) values(?,?,?)",(clase, cred, cal))
    bd.commit()
    nota.delete(0, END)
    creditos.delete(0, END)
    materia.delete(0, END)
    materia.focus()
    inf.progreso(8, 60)
    inf.promedio(8, 80)
    inf.papa(8, 100)
    
def borrar():
    id = eliminar.get()
    bd = sqlite3.connect('bd.db')
    cursor = bd.cursor()
    cursor.execute("DELETE FROM historia WHERE id = ?", (id,))
    bd.commit()
    eliminar.delete(0, END)
    inf.progreso(8, 60)
    inf.promedio(8, 80)
    inf.papa(8, 100)  
    eliminar.focus()

def historial():
    bd = sqlite3.connect('bd.db')
    cursor = bd.cursor()
    materias = cursor.execute("SELECT id, Nombre, Calificacion FROM historia").fetchall()
    resultado = ''
    for materia in materias:
        resultado += 'id: ' +  str(materia[0]) + ' | Nombre: ' + materia[1] + ' | Calificación: ' + str(materia[2]) +'\n'
    messagebox.showinfo('Historial Académico', resultado)

#Escogiendo Tema de la app
principal = ThemedTk(theme = 'plastik')
principal.iconbitmap(os.getcwd() + '/avance.ico')

#Configurando ventana principal
ventana = Frame(principal)
principal.title('HSUN')
ventana.pack(fill = 'both', expand = "yes")
ventana.config(width = '540', height = '340', relief = 'ridge', bg = "dark slate gray") 

#Configurando el título de la herramienta 
titulo = Frame(principal)
titulo.place(x = 0, y = 0)
titulo.config(bg='floral white', width = '540', height = '45', relief = 'ridge', bd = 1.3)
etiqueta = Label(titulo, text="Herramienta de Seguimiento Universitario", font=("Calibri", 13, "bold"))
etiqueta.place(x=290, y=20, anchor = 'center')
etiqueta.config(bg='snow')

##Cuadro de resumen
#Configuración
informacion = Frame(principal)
informacion.config(bg = 'snow', width = '200', height = '285', relief = 'ridge', bd = 1)
informacion.place(x = 5, y = 50)

#Información 
inf.nuevo('Nombre', 8, 20)
inf.nuevo('Carrera', 8, 40)
inf.progreso(8, 60)
inf.promedio(8, 80)
inf.papa(8, 100)

##Acciones del usario
inf.etiqueta(principal, "Ingrese la información para agregar \nuna nueva materia a su historia académica", 370, 75)

#Agregar Materias
inf.etiqueta(principal, 'Nombre Asigunatura:', 285, 125)
materia = ttk.Entry(principal, width=25)
materia.place(x = 360, y = 115)
materia.focus()
        
inf.etiqueta(principal, 'Número de créditos: ', 285, 155)
creditos = ttk.Entry(principal, width=25)
creditos.place(x = 360, y = 145)

inf.etiqueta(principal, 'Calificación: ', 260, 185)    
nota = ttk.Entry(principal, width=25)
nota.place(x = 360, y = 175)

inf.boton("Agregar Materia", 337, 212, comando = agregar)

#Eliminar Materias
inf.etiqueta(principal, "Ingrese el id de la materia que desea eliminar", 370, 260)
eliminar = ttk.Entry(principal, width = 10)
eliminar.place(x = 224, y = 277)
inf.boton("Eliminar", 302, 276, comando = borrar)

#Historial Académico
inf.boton("Historial Académico", 400, 300, historial)

principal.mainloop()
