from cola import Cola
from turno import Turno

class GestorTurnos:
    def __init__(self):
        self.cola_turnos = Cola()
        self.contador_turnos = 0
        self.tiempo_total_espera = 0
    
    def registrar_turno(self, nombre, edad, especialidad, minuto_entrada=0):
        self.contador_turnos += 1
        turno = Turno(nombre, edad, especialidad, minuto_entrada)
        self.cola_turnos.Push(turno)
        return turno
    
    def atender_turno(self):
        if self.cola_turnos.estaVacia():
            return None
        
        turno_atendido = self.cola_turnos.Pop()
        return turno_atendido
    
    def obtener_tiempo_espera_estimado(self):
        tiempo_total = 0
        actual = self.cola_turnos.primero
        
        while actual != None:
            turno = actual.obtenerInfo()
            tiempo_total += turno.obtenerTiempoAtencion()
            actual = actual.obtenerSiguiente()
        
        return tiempo_total
    
    def obtener_cantidad_turnos(self):
        return self.cola_turnos.tamanio
    
    def obtener_turnos_pendientes(self):
        return self.cola_turnos.obtenerElementos()
    
    def hay_turnos_pendientes(self):
        return not self.cola_turnos.estaVacia()
    
    def ver_proximo_turno(self):
        return self.cola_turnos.verFrente()