
class Alumno():
    def __init__(self,id,datos, asignatura, periodo, calificaciones ):
        self.id = id
        self.datos = datos
        self.calificaciones  = [calificaciones, asignatura, periodo]
        self.n = ""
        self.m = 0
        self.set_datos(datos)
      
        

    def set_datos(self, datos):
        self.nombre = ""
        valores = datos.split(" ")

        self.matricula = valores[1]
        self.m = int(valores[1])
        for i in range(2, len(valores)):
            self.nombre += valores[i] + " "
            self.n = valores[i]

    
    def tostring(self):
        return {self.datos}


