import tkinter as tk
from tkinter import messagebox
import sqlite3 as sq


#----------------------------------------------------------
#GUI: RAIZ
raiz = tk.Tk()
raiz.title("Gestión de Usuarios")
raiz.tk.call('wm', 'iconphoto', raiz._w, tk.PhotoImage(file='res/icono1.png'))
frame = tk.Frame(raiz)
frame.pack()


#----------------------------------------------------------
#Variables y métodos
base_conectada = False
campo_id = tk.StringVar()
campo_nombre = tk.StringVar()
campo_contrasenia = tk.StringVar()
campo_apellido = tk.StringVar()
campo_direccion = tk.StringVar()
cuadro_comentarios = ""
campos = [campo_id,campo_nombre,campo_contrasenia,campo_apellido,campo_direccion]

base_de_datos = ""
puntero = ""

def fmenu_conectar():
	global base_conectada, base_de_datos, puntero
	base_de_datos = sq.connect("Usuarios")
	puntero = base_de_datos.cursor()
	try:
		puntero.execute('''
		CREATE TABLE USUARIOS (ID INTEGER PRIMARY KEY AUTOINCREMENT,NOMBRE VARCHAR(50),CONTRASEÑA VARCHAR(50),
		APELLIDO VARCHAR(50),DIRECCION VARCHAR(100),COMENTARIOS VARCHAR(200))
		''')
		messagebox.showinfo("Conexión exitosa", "La BBDD se ha conectado con éxito!")
		base_conectada = True
	except:
		if base_conectada: messagebox.showinfo("Base conectada", "La BBDD ya está conectada")
		else: messagebox.showinfo("Conexión exitosa", "La BBDD se ha conectado con éxito!")

def fmenu_salir():
	if messagebox.askokcancel("Salir", "¿Está seguro que desea salir?"):
		try: base_de_datos.close()
		except: pass
		raiz.destroy()

def fmenu_borrar_campos():
	global cuadro_comentarios, campos
	for i in campos: i.set("")
	cuadro_comentarios.delete(1.0, tk.END)

def fmenu_licencia(): messagebox.showinfo("Licencia", "Este programa tiene una licencia de código abierto, gratuito y libre")
def fmenu_acercade(): messagebox.showinfo("Acerca de", "Aplicación de prueba para la gestión de usuarios")

def boton_crear():
	global campo_nombre, campo_contrasenia,campo_apellido,campo_direccion,cuadro_comentarios, base_de_datos, puntero
	vals = [
		"" + campo_nombre.get(),
		"" + campo_contrasenia.get(),
		"" + campo_apellido.get(),
		"" + campo_direccion.get(),
		"" + cuadro_comentarios.get(1.0, tk.END)
	]
	try:
		puntero.execute(f"INSERT INTO USUARIOS VALUES ('{int(campo_id.get())}','{vals[0]}','{vals[1]}','{vals[2]}','{vals[3]}','{vals[4]}')")
		base_de_datos.commit()
		messagebox.showinfo("Éxito", "Registro insertado correctamente")
	except AttributeError: messagebox.showwarning("Conéctese a la base", "Debe conectarse a la base antes de operar. [BBDD>Conectar]")

	

def boton_leer():
	global campo_nombre,campo_contrasenia,campo_apellido,campo_direccion, campo_id, cuadro_comentarios, base_de_datos, puntero
	try:
		puntero.execute(f"SELECT * FROM USUARIOS WHERE ID={int(campo_id.get())}")
		valores = puntero.fetchall()
		campo_nombre.set(valores[0][1])
		campo_contrasenia.set(valores[0][2])
		campo_apellido.set(valores[0][3])
		campo_direccion.set(valores[0][4])
		cuadro_comentarios.delete(1.0, tk.END)
		cuadro_comentarios.insert(1.0, valores[0][5])
	except AttributeError: messagebox.showwarning("Conéctese a la base", "Debe conectarse a la base antes de operar. [BBDD>Conectar]")
	except IndexError: messagebox.showwarning("Id incorrecto","El ID que ingresó no existe")

def boton_actualizar():
	global campo_nombre,campo_contrasenia,campo_apellido,campo_direccion,campo_id,cuadro_comentarios, base_de_datos, puntero
	try:
		ide = int(campo_id.get())
		puntero.execute(f"UPDATE USUARIOS SET NOMBRE='{campo_nombre.get()}' WHERE ID={ide}")
		puntero.execute(f"UPDATE USUARIOS SET CONTRASEÑA='{campo_contrasenia.get()}' WHERE ID={ide}")
		puntero.execute(f"UPDATE USUARIOS SET APELLIDO='{campo_apellido.get()}' WHERE ID={ide}")
		puntero.execute(f"UPDATE USUARIOS SET DIRECCION='{campo_direccion.get()}' WHERE ID={ide}")
		puntero.execute(f"UPDATE USUARIOS SET COMENTARIOS='{cuadro_comentarios.get(1.0,tk.END)}' WHERE ID={ide}")
		base_de_datos.commit()
		messagebox.showinfo("Éxito", "Registro actualizado correctamente")
	except AttributeError: messagebox.showwarning("Conéctese a la base", "Debe conectarse a la base antes de operar. [BBDD>Conectar]")


def boton_borrar():
	global campo_id, base_de_datos, puntero
	try:
		puntero.execute(f"DELETE FROM USUARIOS WHERE ID={int(campo_id.get())}")
		base_de_datos.commit()
		messagebox.showinfo("Exito", "Campo borrado correctamente")
	except AttributeError: messagebox.showwarning("Conéctese a la base", "Debe conectarse a la base antes de operar. [BBDD>Conectar]")


#----------------------------------------------------------
#GUI: MENU
barra_menu = tk.Menu()
raiz["menu"] = barra_menu
menu_base = tk.Menu(barra_menu, tearoff=0)
menu_borrar = tk.Menu(barra_menu, tearoff=0)
menu_crud = tk.Menu(barra_menu, tearoff=0)
menu_ayuda = tk.Menu(barra_menu, tearoff=0)

menu_base.add_command(label="Conectar", command=fmenu_conectar)
menu_base.add_command(label="Salir", command=fmenu_salir)
menu_borrar.add_command(label="Borrar campos", command=fmenu_borrar_campos)
menu_crud.add_command(label="Crear", command=boton_crear)
menu_crud.add_command(label="Leer", command=boton_leer)
menu_crud.add_command(label="Actualizar", command=boton_actualizar)
menu_crud.add_command(label="Borrar", command=boton_borrar)
menu_ayuda.add_command(label="Licencia", command=fmenu_licencia)
menu_ayuda.add_command(label="Acerca de", command=fmenu_acercade)

barra_menu.add_cascade(label="BBDD", menu=menu_base)
barra_menu.add_cascade(label="Borrar", menu=menu_borrar)
barra_menu.add_cascade(label="CRUD", menu=menu_crud)
barra_menu.add_cascade(label="Ayuda", menu=menu_ayuda)


#----------------------------------------------------------
#GUI: Dentro del frame
tk.Label(frame,text="Id:", pady=6).grid(row=1,column=1)
tk.Label(frame,text="Nombre:", pady=6).grid(row=2,column=1)
tk.Label(frame,text="Contraseña:", pady=6).grid(row=3,column=1)
tk.Label(frame,text="Apellido:", pady=6).grid(row=4,column=1)
tk.Label(frame,text="Dirección:", pady=6).grid(row=5,column=1)
tk.Label(frame,text="Comentarios:", pady=6).grid(row=6,column=1)

tk.Entry(frame,textvariable=campo_id, width=15).grid(row=1,column=2)
tk.Entry(frame,textvariable=campo_nombre, width=15, justify="right", fg="red").grid(row=2,column=2)
tk.Entry(frame,textvariable=campo_contrasenia, width=15, show="*").grid(row=3,column=2)
tk.Entry(frame,textvariable=campo_apellido, width=15).grid(row=4,column=2)
tk.Entry(frame,textvariable=campo_direccion, width=15).grid(row=5,column=2)
cuadro_comentarios = tk.Text(frame,height=3,width=15)
cuadro_comentarios.grid(row=6,column=2)

tk.Label(raiz,text="").pack()
tk.Button(raiz,text="Crear", width=3, command=boton_crear).pack(side="left")
tk.Button(raiz,text="Leer", width=3, command=boton_leer).pack(side="left")
tk.Button(raiz,text="Actualizar", width=6, command=boton_actualizar).pack(side="right")
tk.Button(raiz,text="Borrar", width=4, command=boton_borrar).pack(side="right")


#-----------------------------------------------------------
#Cierre
raiz.mainloop()