class InfoNodo():
    def desplegar():
        pass
    
    def EsIgualALLave():
        pass

class Nodo:
    def __init__(self, info):
        self.info = info
        self.siguiente = None

    def obtenerInfo(self):
        return self.info

    def obtenerSiguiente(self):
        return self.siguiente

    def asignarInfo(self, info):
        self.info = info

    def asignarSiguiente(self, nuevosiguiente):
        self.siguiente = nuevosiguiente