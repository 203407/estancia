
import psycopg2

conn = psycopg2.connect(
            user="postgres",
            password="carrera10",
            host="localhost",
            port="5432",   
            database="estancia"
        )
cursor = conn.cursor()

nomre = 'julia'
id = '12e131d'
matricula=203407


sql = f"INSERT INTO alumnos (id, nombre, matricula) VALUES ('{id}','{nomre}',{matricula})"


cursor.execute(sql);

conn.commit()

print("Record inserted successfully")


        # Obtén los resultados de la consulta
    #results = cursor.fetchall()
#     #print(results)
# try:
        
#     cursor.execute(sql)
#     # Verificar si se insertó correctamente
#     if cursor.rowcount > 0:
#         print("La inserción se realizó correctamente.")
#     else:
#         print("La inserción no se realizó correctamente.")

# except psycopg2.Error as e:
#     print(f"Ocurrió un error: {e}")
#         # Cierra el cursor y la conexión

cursor.close()
conn.close()