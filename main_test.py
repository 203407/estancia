import tkinter as tk
import customtkinter as ctk 
from tkinter import filedialog
from interfaz_test import Window

import PyPDF2, re
import uuid
import psycopg2



from alumno import Alumno



def get_reprobados(pdf_reader, asignatura, periodo):
    cont = 0
   
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text = page.extract_text()
        lines = text.split('\n')
        for line in lines:
            if cont > 5:
                match = re.match(r'(\b\w+\b.*?)(\d+\s+\d+)', line)
                if match != None:
                    part1 = match.group(1)
                    part2 = match.group(2)
                    calificaciones = part2.split(" ")
                    for c in calificaciones:
                        if int(c) < 70:
                            id_unico = uuid.uuid4()
                            x = ''+  str(id_unico) 
                            a = Alumno(x,part1, asignatura, periodo, calificaciones)
                            
                            
                            insertarData(a.id,a.nombre,a.m,asignatura,periodo)
                            createInci(a.m)

                            #win.alumnos.append(a)
                            break

            cont += 1
                
def insertarData(id,nombre,matricula,materiaR,periodo):
    conn = psycopg2.connect(
            user="postgres",
            password="carrera10",
            host="localhost",
            port="5432",   
            database="estancia"
        )
    cursor = conn.cursor()

    sql = f"INSERT INTO alumnos (id, nombre, matricula,materiar,periodo) VALUES ('{id}','{nombre}',{matricula},'{materiaR}','{periodo}')"

    cursor.execute(sql);

    conn.commit()

    cursor.close()
    conn.close()
    

def get_periodo(pdf_reader):
    search = "PERIODO"
    rule = "\d\s[A-Z]{2}"
    found = False
    periodo = None

    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text = page.extract_text()
        lines = text.split('\n')
        profesor = lines[len(lines)-1]
        profesor = profesor.replace(" SERVICIOS ESCOLARES", "")
        for line in lines:
            if search in line:
                found = True
                match = re.search(rule, line)
                pos = match.start() + 1
                lineFormat = line[:pos]
                periodo = lineFormat.replace("PERIODO: ", "")
                break
        if found:
            break
    return periodo, profesor


def get_asignatura(pdf_reader):
    search = "ASIGNATURA"
    rule = '\s[A-Z]{2}'
    found = False
    value = None

    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text = page.extract_text()
        lines = text.split('\n')
        for line in lines:
            if search in line:
                found = True
                lineFormat = re.split(rule, line)
                value = lineFormat[0].replace("ASIGNATURA: ", "")
                win.show_message("Mensaje", "Se actualizaron los datos")
                break
        if found:
            break
    return value

   
def get_data():
    print(FILEPATH)
    pdf_file = open(FILEPATH, 'rb')
    pdf_reader = PyPDF2.PdfReader(pdf_file)

    page = pdf_reader.pages[0]
    text = page.extract_text()
    lines = text.split('\n')
    
    #LECTURA DE PDF ACTA DE CALIFICACIONES
    if "ACTA DE CALIFICACIONES" in lines[1]:
        asignatura = get_asignatura(pdf_reader)
        periodo, profesor = get_periodo(pdf_reader)
        # print(asignatura +" "+ periodo +" "+ profesor)
        get_reprobados(pdf_reader, asignatura, periodo)

        if asignatura not in win.asignaturas and asignatura != None:
            #win.asignaturas.append(asignatura)
            print(asignatura)
            insertarDataA(asignatura)
            print(win.asignaturas)

    pdf_file.close()


def createInci(idAlumno):
    conn = psycopg2.connect(
            user="postgres",
            password="carrera10",
            host="localhost",
            port="5432",   
            database="estancia"
        )
    cursor = conn.cursor()
    data = [[''],[''],[''],[''],[''],[''],[''],[''],[''],[''],[''],[''],[''],[''],['']]
    sql = "INSERT INTO incidencias (matriculaalumno, uplo) VALUES (%s, %s)"

    valores = (idAlumno, data)

    cursor.execute(sql, valores)

    conn.commit()

    cursor.close()
    conn.close()
             
def insertarDataA(asignatura):
    conn = psycopg2.connect(
            user="postgres",
            password="carrera10",
            host="localhost",
            port="5432",   
            database="estancia"
        )
    cursor = conn.cursor()

    sql = f"INSERT INTO materias (materiass) VALUES ('{asignatura}')"

    cursor.execute(sql);

    conn.commit()

    cursor.close()
    conn.close()
   

def select_file():
    global FILEPATH
    FILEPATH = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    label = ctk.CTkLabel(master=win.bottom_frame, text=FILEPATH)
    label.place(relx= 0.5, rely=0.45, anchor=tk.CENTER)

     
if __name__ == "__main__":
    win = Window(select_file, get_data)
    win.mainloop()
    
    