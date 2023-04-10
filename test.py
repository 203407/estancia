import json
import psycopg2

# def createUser():
#         conn = psycopg2.connect(
#                 user="postgres",
#                 password="carrera10",
#                 host="localhost",
#                 port="5432",   
#                 database="estancia"
#             )
#         cursor = conn.cursor()      

#         a = ['']
#         b = ['']
#         c = ['']
#         d = ['']        

#         sql = "INSERT INTO trayectoria (gradoestar,materiasqllevar,materiasaprobadas,materiasrepeticion,nommateriasrepe,cuatrimfalta,materiaqfalta,materiarezagada,nombremateriareza,nommatedeberia,nombrellevaactual,matriculaalumno) VALUES (1,2,3,4,%s,10,%s,2,'as',%s,%s,203407)"           
        
#         valores = (a,b,c,d)

#         cursor.execute(sql,valores)

#         conn.commit()

#         cursor.close()
#         conn.close()

# # createUser()

def selectData():
        conn = psycopg2.connect(
            user="postgres",
            password="carrera10",
            host="localhost",
            port="5432",   
            database="estancia"
        )
        cursor = conn.cursor()

        cursor.execute(f'SELECT * FROM alumnos WHERE matricula = {183392}')
        
        results = cursor.fetchall()

        # print(results[0][-1])
        a = json.dumps(results[0][-1])
        materias = json.loads(a)
        j = json.dumps({"Calidad del Software": "SEPTIEMBRE-DICIEMBRE 2020"})
        mate = json.loads(j)
        print(materias)
        print(mate)

        
        if all(item in materias.items() for item in mate.items()):
                print("El contenido de 'a' está presente en 'materias'")
        else:
                print("El contenido de 'a' no está presente en 'materias'")
        # for t in x:
        #         print(t)
                
        # for x in results[0][-1]:
        #         print(x)
            
        cursor.close()
        conn.close()

# selectData()

def updateusuario():
            conn = psycopg2.connect(
                    user="postgres",
                    password="carrera10",
                    host="localhost",
                    port="5432",   
                    database="estancia"
                )
            cursor = conn.cursor()                    

            a = '{"Calidad del Software": "SEPTIEMBRE-DICIEMBRE 2020"}'
            b = '{"Mantenimiento de Software": "MAYO-AGOSTO 2021"}'

            json_a = json.loads(a)
            json_b = json.loads(b)
            
            json_a.update(json_b)                                
            matricula = 183392
            campo = 'mats'
            valores = (json.dumps(json_a),matricula)
            
            
            sql = "UPDATE alumnos SET {} = %s WHERE matricula = %s".format(campo)
            cursor.execute(sql, valores)

            conn.commit()

            cursor.close()
            conn.close()


# updateusuario()

# updateTrayectoria()

def selectData():
        conn = psycopg2.connect(
            user="postgres",
            password="carrera10",
            host="localhost",
            port="5432",   
            database="estancia"
        )
        cursor = conn.cursor()

        cursor.execute("SELECT notas FROM incidencias where matriculaalumno =191214")
        
        results = cursor.fetchall()


        print(results[0][0])
        if  results[0][0] == None:
                print('no hay ndad')                
        else:
                print('si hayu')
            
        cursor.close()
        conn.close()

# selectData()


def createInci():
        conn = psycopg2.connect(
                user="postgres",
                password="carrera10",
                host="localhost",
                port="5432",   
                database="estancia"
        )
        
        cursor = conn.cursor()      
        matricula= 2034072
        cuatri= 1        
        notas = ['nota1','nota2','nota3']

        sql = "INSERT INTO incidencias (matriculaalumno,cuatri,notas) VALUES (%s,%s,%s)"

        valores = (matricula,cuatri,notas)

        cursor.execute(sql, valores)

        conn.commit()

        cursor.close()
        conn.close()

# createInci()


def updateInciN():
        conn = psycopg2.connect(
                user="postgres",
                password="carrera10",
                host="localhost",
                port="5432",   
                database="estancia"
            )
        cursor = conn.cursor()        
        matricula=183392
        cuatri= 1
        datas= [{'a':'s'}]
        
        sql = "UPDATE incidencias SET notas = %s WHERE matriculaalumno = %s and cuatri = %s;"

        valores = (datas,matricula,cuatri)

        cursor.execute(sql, valores)

        conn.commit()

        cursor.close()
        conn.close()

# updateInciN()

def intertUser():
        conn = psycopg2.connect(
                user="postgres",
                password="carrera10",
                host="localhost",
                port="5432",   
                database="estancia"
            )
        cursor = conn.cursor()        
        
                
        n = {{"a":1,"b":2}}
        
        a = json.dumps(n)
        
        sql = "INSERT INTO tes (testd) VALUES (%s)"
        valores = (a)

        cursor.execute(sql, (valores,))

        conn.commit()

        cursor.close()
        conn.close()

def intertUser2():
        conn = psycopg2.connect(
                user="postgres",
                password="carrera10",
                host="localhost",
                port="5432",   
                database="estancia"
            )
        cursor = conn.cursor()        
        
                
       # Definimos los dos JSON
        json_string1 = '{"as2":"perido 202--20", "dddds ":"perido 10023"}'        

        data = {
                "Periodo academico":["","",""],
                "Cantidad alumnos" : [0,0,0],
                "Reprobacion":[0,0,0],
                "Rezago":[0,0,0],
                "Retencion":[0,0,0],
                "Abandono escolar":[0,0,0],
                "Desercion":[0,0,0],
                "Terminacion": [0,0,0],
                "Eficiencia Terminal":[0,0,0],
                "Titulados":[0,0,0]            
        } 
   
        # Convertimos el objeto Python resultante en un nuevo JSON
        new_json_string = json.dumps(data)
        matricula = 183
        sql = "INSERT INTO tes (data,mat) VALUES (%s,%s)"
        valores = (new_json_string)       

        cursor.execute(sql, (valores,))

        conn.commit()

        cursor.close()
        conn.close()
        
# intertUser2()


def intertUser2():
        conn = psycopg2.connect(
                user="postgres",
                password="carrera10",
                host="localhost",
                port="5432",   
                database="estancia"
            )
        cursor = conn.cursor()        
                        
        periodo_academico= ["","",""]
        cantidad_alumnos = [0,0,0]
        reprobacion=[0,0,0]
        rezago=[0,0,0]
        retencion=[0,0,0]
        abandono_escolar=[0,0,0]
        desercion=[0,0,0]
        terminaron = [0,0,0]
        eficiencia_terminal= [0,0,0]
        titulados= [0,0,0]            
                    
        matricula = 183
        
        periodosAca = {

            "183": ["SEPTIEMBRE-DICIEMBRE 2018","ENERO-ABRIL 2019","MAYO-AGOSTO 2019","SEPTIEMBRE-DICIEMBRE 2019","ENERO-ABRIL 2020","MAYO-AGOSTO 2020","SEPTIEMBRE-DICIEMBRE 2020","ENERO-ABRIL 2021","MAYO-AGOSTO 2021","SEPTIEMBRE-DICIEMBRE 2021","ENERO-ABRIL 2022","MAYO-AGOSTO 2022","SEPTIEMBRE-DICIEMBRE 2022","ENERO-ABRIL 2023","MAYO-AGOSTO 2023"],

            "191": ["ENERO-ABRIL 2019","MAYO-AGOSTO 2019","SEPTIEMBRE-DICIEMBRE 2019","ENERO-ABRIL 2020","MAYO-AGOSTO 2020","SEPTIEMBRE-DICIEMBRE 2020","ENERO-ABRIL 2021","MAYO-AGOSTO 2021","SEPTIEMBRE-DICIEMBRE 2021","ENERO-ABRIL 2022","MAYO-AGOSTO 2022","SEPTIEMBRE-DICIEMBRE 2022","ENERO-ABRIL 2023","MAYO-AGOSTO 2023","SEPTIEMBRE-DICIEMBRE 2023"],        
        
        }

        sql = "INSERT INTO trayectoriageneral (mat,cantidad_alumnos,reprobacion,rezago,retencion,abandono_escolar,desercion,terminaron,eficiencia_terminal,titulados,periodo_academico) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        # sql = "INSERT INTO trayectoriageneral (mat,periodo_academico) VALUES (%s,%s)"
        
        valores = (matricula,cantidad_alumnos,reprobacion,rezago,retencion,abandono_escolar,desercion,terminaron,eficiencia_terminal,titulados,periodosAca["183"])       

        cursor.execute(sql, valores)

        conn.commit()

        cursor.close()
        conn.close()
        
# intertUser2()


def selectdatas():
        conn = psycopg2.connect(
            user="postgres",
            password="carrera10",
            host="localhost",
            port="5432",   
            database="estancia"
        )
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM materias")
        
        results = cursor.fetchall()
        

        for x in results:                
                if x[0] == "Calidad del Software":
                        print("si esta")
                        

        # for x in results:
        #         print(x[0])
        #         print(x[0])
        # print(results[0][0])

        # if  results[0][0] == None:
        #         print('no hay ndad')                
        # else:
        #         print('si hayu')
            
        cursor.close()
        conn.close()

# intertUser()
# selectdatas()

def getByMatricula():
        conn = psycopg2.connect(
            user="postgres",
            password="carrera10",
            host="localhost",
            port="5432",   
            database="estancia"
        )
        cursor = conn.cursor()        
        # Ejecuta una consulta SQL
        
        matricula = 183392
        
        a = {"base de datos":"Periodo abril-marzo"}

        materias = {"base de datos":"Periodo abril-marzo",
                    "IA":"Periodo mayo-diciemre"}

        cursor.execute(f"SELECT * FROM alumnos WHERE matricula={matricula}" )

        # Obtén los resultados de la consulta
        results = cursor.fetchall()
        # print(results)
        
        if results!= []:                
                print(results)
        else:
                print("no hay alumno con esa matricula")

        cursor.close()
        conn.close()

        return results

# getByMatricula()
# a = {"nombre":"jose","edad":1,"nombre":"jose","edad":1}
# for x in a:
#         print(x)

# a = {"base de datos":"Periodo abril-marzo"}
# materias = {"base de datos":"Periodo abril-marzo", "IA":"Periodo mayo-diciembre"}

# if all(item in materias.items() for item in a.items()):
#     print("El contenido de 'a' está presente en 'materias'")
# else:
#     print("El contenido de 'a' no está presente en 'materias'")

# print(a[0])


def selectDataTraByM(matricula):
        conn = psycopg2.connect(
            user="postgres",
            password="carrera10",
            host="localhost",
            port="5432",   
            database="estancia"
        )
        cursor = conn.cursor()

        cursor.execute(f'SELECT * FROM trayectoria Where matriculaalumno = {matricula}')
        
        results = cursor.fetchall()

        print(results[0])
            
        cursor.close()
        conn.close()

        # return results

# selectDataTraByM(183392)


def selectTrayByGeneraciones(matricula):
        conn = psycopg2.connect(
            user="postgres",
            password="carrera10",
            host="localhost",
            port="5432",   
            database="estancia"
        )
        cursor = conn.cursor()        

        cursor.execute(f'SELECT * FROM trayectoriageneral where mat = {matricula}')
        
        results = cursor.fetchall()
        
        print(results[0][-1])
            
        cursor.close()
        conn.close()
        
        return results



# selectTrayByGeneraciones(183)




def intertGeneracion(matricula):
        
        conn = psycopg2.connect(
                user="postgres",
                password="carrera10",
                host="localhost",
                port="5432",   
                database="estancia"
        )

        cursor = conn.cursor()        
                                
        
        sql = "INSERT INTO generaciones (matri) VALUES (%s)"
        valores = (matricula,)

        cursor.execute(sql, valores)

        conn.commit()

        cursor.close()
        conn.close()

# intertGeneracion(203)


def selectGeneraciones(matricula):
        conn = psycopg2.connect(
            user="postgres",
            password="carrera10",
            host="localhost",
            port="5432",   
            database="estancia"
        )
        cursor = conn.cursor()        

        cursor.execute(f'SELECT * FROM generaciones where matri = {matricula}')
        
        results = cursor.fetchall()
        
        response = 0
        if results != []:
                print(results)
                response = 1
        else:
                print("no hya nada")
            
        cursor.close()
        conn.close()
        
        return response

# selectGeneraciones(2203)


def selectdatas():
        conn = psycopg2.connect(
            user="postgres",
            password="carrera10",
            host="localhost",
            port="5432",   
            database="estancia"
        )
        cursor = conn.cursor()

        prefijo = 183

        cursor.execute(f"SELECT * FROM alumnos WHERE CAST(matricula AS TEXT) LIKE '{prefijo}%'")

        resultado = cursor.fetchall()
        


        print(resultado)
                        
            
        cursor.close()
        conn.close()

        return resultado

selectdatas()