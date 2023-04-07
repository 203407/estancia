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

        # Convertimos los dos JSON en objetos Python
        # json_obj1 = json.loads(json_string1)        

        # Combinamos los dos objetos Python en uno solo
        # new_json_obj = {**json_obj1, **json_obj2}

        # Convertimos el objeto Python resultante en un nuevo JSON
        new_json_string = json.dumps(json_string1)
        
        sql = "INSERT INTO tes (testd,dds) VALUES (%s,%s)"
        valores = (new_json_string,'l')       

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

selectDataTraByM(183392)