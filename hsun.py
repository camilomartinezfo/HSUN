#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 23 12:10:07 2021

@author: Juan
"""

from tkinter import *
from tkinter import ttk
from ttkthemes import ThemedTk
import sqlite3
import platform
import os
from PIL import Image
from PIL import ImageTk

bd = sqlite3.connect('bd.db')
cursor = bd.cursor()
tablas = cursor.execute('SELECT name from sqlite_master where type= "table"').fetchall()
tab = []
for tabla in tablas:
    tab.append(tabla[0])

def guardar():
    nombre = usuario.get()
    programa = carrera.get()
    cantidad = creditos.get()
    cursor.execute("INSERT INTO registro (Nombre, Carrera, Creditos) values(?,?,?)",(nombre, programa, cantidad))
    bd.commit()
    registro.destroy()

if 'registro' not in tab:
    cursor.execute("CREATE TABLE registro (Nombre TEXT, Carrera TEXT, Creditos INTEGER)")
    registro = ThemedTk(theme = 'plastik')
    if platform.system() == "Windows":
        registro.iconbitmap(os.getcwd() + '\\avance.ico')
    registro.title('HSUN')
    ventana = Frame(registro)
    ventana.config(width = '430', height = '170', bg = '#F8F9FB')
    ventana.pack()
        
    # Título
    etiqueta = Label(registro, text="Por favor complete la siguiente información: ", font=("Calibri", 13, "bold"))
    etiqueta.place(x=220, y=20, anchor = 'center')
    etiqueta.config(bg = '#F8F9FB')
        
    #Entradas
    nombre = Label(registro, text="Nombre: ", font=("Arial", 11))
    nombre.place(x=20, y=50)
    nombre.config(bg = '#F8F9FB')
    usuario = ttk.Entry(registro, width = 25)
    usuario.place(x = 100, y = 50)
            
    programa = Label(registro, text="Carrera: ", font=("Arial", 11))
    programa.place(x=20, y=80)
    programa.config(bg = '#F8F9FB')
    carrera = ttk.Entry(registro, width = 25)
    carrera.place(x = 100, y = 80)
            
    cantidad = Label(registro, text="Total \nCréditos: ", font=("Arial", 11))
    cantidad.place(x=20, y=110)
    cantidad.config(bg = '#F8F9FB')
    creditos = ttk.Entry(registro, width = 25)
    creditos.place(x = 100, y = 120)
        
    #Guardar inforamción
    guardar = ttk.Button(registro, text='Guardar', command = guardar)
    if platform.system() == "Windows":
        guardar.place(x = 280, y = 80)
    else:
        guardar.place(x = 320, y = 80)
    
    registro.mainloop()
            

class inf():
    bd = sqlite3.connect('bd.db')
    cursor = bd.cursor()
    cursor.execute("create table if not exists historia (id INTEGER PRIMARY KEY AUTOINCREMENT, Nombre TEXT, Creditos INTEGER, Calificacion REAL)")
    def nuevo(item, posx, posy):
        nombre = inf.cursor.execute("SELECT " + item + " FROM registro").fetchall()[0][0]
        estudiante = Label(informacion, text = "{}: {}".format(item, nombre)) 
        estudiante.place(x = posx, y = posy)
        estudiante.config(bg = 'snow')
    
    def progreso():
        total = inf.cursor.execute("SELECT Creditos FROM registro").fetchall()[0][0]
        prog = inf.cursor.execute("SELECT Creditos FROM historia  WHERE Calificacion >= 3.0").fetchall()
        suma = 0
        for credito in prog:
            suma += credito[0]
        prog = round(suma/total*100,2)
        return prog
        
    def boton(texto, posx, posy, comando = 0):
        boton = ttk.Button(principal, text=texto, command = comando)
        boton.place(x = posx, y = posy)
            
    def etiqueta(ventana, texto, posx, posy, fondo = 'dark slate gray', letra = 'floral white'):
        titulo = Label(ventana, text = texto, font = ("Arial", 11)) 
        titulo.place(x = posx, y = posy, anchor = 'center')
        titulo.config(bg = fondo, fg = letra)
                
    def promedio():
        resultado = inf.cursor.execute("SELECT Creditos, Calificacion FROM historia WHERE Calificacion >= 3.0").fetchall()
        suma = 0
        total = 0
        for materia in resultado:
            suma += materia[0] * materia[1]
            total += materia[0]
        if total != 0:
            prom = round(suma/total,1)
        else:
            prom = "N.A"
        return prom
        
    def papa():
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
        return prom

def tramosImg(x):
    im_logo = Image.open("1-256x256.png") 
    im_fin = Image.open("2-256x256.png")
    imgorro = Image.open("gorroesc.png")
    img = Image.open("New.png")
    if x < 20:
        img.paste(im_logo,(20, 335))
    elif x < 100:
        img.paste(im_logo,(x,round(385 - (0.4375*x + 41.25))))
    elif x < 185:
        img.paste(im_logo,(x,round(385 - (1.058823*x - 20.88))))        
    elif x < 255:
        img.paste(im_logo,(x,round(385 - (0.7857*x + 29.6429))))        
    elif x < 405:
        img.paste(im_logo,(x,round(385 - (0.3667*x + 136.5))))        
    elif x < 449:
        img.paste(im_logo,(x,round(385 - (1.55*x - 342.75))))        
    elif x < 480:      
        img.paste(im_fin,(470, 25))
        img.paste(imgorro,(470,12))
    img.save('image.png')                           

def Rescala(x):
    return round(4.293*x + 20)

def logoGrafico(x):
    xvalue = Rescala(x)
    tramosImg(xvalue)
    Img = Image.open("image.png")
    ImgMod = Img.resize((190,150))
    ImgMod.save("image.png","png")

def agregar():
    clase = materia.get()
    cal = nota.get()
    cred = creditos.get()
    cursor.execute("INSERT INTO historia (Nombre, Creditos, Calificacion) values(?,?,?)",(clase, cred, cal))
    bd.commit()
    nota.delete(0, END)
    creditos.delete(0, END)
    materia.delete(0, END)
    materia.focus()
    avance['text'] = "Progreso: {}%".format(inf.progreso())
    promedio['text'] = "Promedio Académico: {}".format(inf.promedio())
    papa['text'] = "P.A.P.A: {}".format(inf.papa())
    logoGrafico(inf.progreso())
    im = ImageTk.PhotoImage(Image.open(ruta))
    panel.configure(image = im)
    panel.image = im

def borrar():
    id = eliminar.get()
    cursor.execute("DELETE FROM historia WHERE id = ?", (id,))
    bd.commit()
    eliminar.delete(0, END)
    avance['text'] = "Progreso: {}%".format(inf.progreso()) 
    promedio['text'] = "Promedio Académico: {}".format(inf.promedio())
    papa['text'] = "P.A.P.A: {}".format(inf.papa())
    eliminar.focus()
    logoGrafico(inf.progreso())
    im = ImageTk.PhotoImage(Image.open(ruta))
    panel.configure(image = im)
    panel.image = im

def historial():
    tabla = ThemedTk(theme = 'plastik')
    if platform.system() == "Windows":
        tabla.iconbitmap(os.getcwd() + '\\avance.ico')
    tabla.title('Historial Académico')
    ventana = Frame(tabla)
    ventana.config(width = '390', height = '80')
    scrollbar = Scrollbar(tabla)
    scrollbar.pack(side = RIGHT, fill = Y) 
    resumen = ttk.Treeview(tabla, yscrollcommand = scrollbar.set)
    resumen.pack(fill = 'both', expand = True)
    scrollbar.config(command = resumen.yview )
    resumen["columns"] = ("uno", "dos", "tres")
    resumen.column("#0", width=10, minwidth=20)
    resumen.column("uno", width=50, minwidth=50)
    resumen.column("dos", width=230, minwidth=80)
    resumen.column("tres", width=120, minwidth=50)
    resumen.heading("uno", text="ID")
    resumen.heading("dos", text="MATERIA")
    resumen.heading("tres", text="CALIFICACIÓN")
    materias = cursor.execute("SELECT id, Nombre, Calificacion FROM historia").fetchall()
    for materia in materias:
        resumen.insert("", END, values=(materia))
    tabla.mainloop()

#Escogiendo Tema de la app
principal = ThemedTk(theme = 'plastik')
if platform.system() == "Windows":
    principal.iconbitmap(os.getcwd() + '\\avance.ico')

#Configurando ventana principal
ventana = Frame(principal)
principal.title('HSUN')
ventana.pack(fill = 'both', expand = True)
if platform.system() == "Windows":
    ventana.config(width = '540', height = '340', relief = 'ridge', bg = "dark slate gray") 
else:
    ventana.config(width = '585', height = '340', relief = 'ridge', bg = "dark slate gray")

#Configurando el título de la herramienta 
titulo = Frame(principal)
titulo.place(x = 0, y = 0)
if platform.system() == "Windows":
    titulo.config(bg='floral white', width = '540', height = '45', relief = 'ridge', bd = 1.3)
else:
    titulo.config(bg='floral white', width = '585', height = '45', relief = 'ridge', bd = 1.3)
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

avance = Label(informacion, text = "Progreso: {}%".format(inf.progreso())) 
avance.place(x = 8, y = 60)
avance.config(bg = 'snow')

promedio = Label(informacion, text = "Promedio Académico: {}".format(inf.promedio())) 
promedio.place(x = 8, y = 80)
promedio.config(bg = 'snow')

papa = Label(informacion, text = "P.A.P.A: {}".format(inf.papa())) 
papa.place(x = 8, y = 100)
papa.config(bg = 'snow')

#Grafico
logoGrafico(inf.progreso())

if platform.system() == 'Windows':
    ruta = os.getcwd() + '\\image.png'
else:
    ruta = os.getcwd() + '/image.png'
im = ImageTk.PhotoImage(file = ruta)
panel = Label(informacion, image = im)
panel.pack()
panel.config(relief = 'flat', bd = 0)
panel.place(x = 3, y = 130)

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
if platform.system() == "Windows":
    inf.boton("Eliminar", 302, 276, comando = borrar)
else:
    inf.boton("Eliminar", 320, 276, comando = borrar)

#Historial Académico
if platform.system() == "Windows":
    inf.boton("Historial Académico", 400, 300, historial)
else:
    inf.boton("Historial Académico", 425, 300, historial)

principal.resizable(0,0) #No permite que se maximice la ventana
principal.mainloop()