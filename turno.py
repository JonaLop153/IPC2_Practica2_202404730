from nodo import InfoNodo

class Turno(InfoNodo):
    def __init__(self, nombre, edad, especialidad, minutoentradaacola):
        self.Nombre = nombre
        self.Edad = edad
        self.Especialidad = especialidad
        self.MinutoEntradaACola = minutoentradaacola
        
        # Tiempos de atención por especialidad
        self.tiempos_atencion = {
            "Medicina General": 10,
            "Pediatría": 15,
            "Ginecología": 20,
            "Dermatología": 25
        }
    
    def obtenerNombre(self):
        return self.Nombre
       
    def asignarNombre(self, nombre):
        self.Nombre = nombre

    def obtenerEdad(self):
        return self.Edad
       
    def asignarEdad(self, edad):
        self.Edad = edad

    def obtenerEspecialidad(self):
        return self.Especialidad
       
    def asignarEspecialidad(self, especialidad):
        self.Especialidad = especialidad

    def obtenerMinutoEntradaACola(self):
        return self.MinutoEntradaACola
       
    def asignarMinutoEntradaACola(self, minutoentradaacola):
        self.MinutoEntradaACola = minutoentradaacola
        
    def obtenerTiempoAtencion(self):
        return self.tiempos_atencion.get(self.Especialidad, 0)

    def desplegar(self):
        print(f"{self.Nombre} - {self.Edad} años - {self.Especialidad} - Minuto entrada: {self.MinutoEntradaACola}")

    def EsIgualALLave(self, nombre):
        return self.Nombre == nombre
    
    def __str__(self):
        return f"{self.Nombre} ({self.Edad} años) - {self.Especialidad} - Tiempo: {self.obtenerTiempoAtencion()} min"