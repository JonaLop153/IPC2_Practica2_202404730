from nodo import Nodo

class Cola:
    def __init__(self):
        self.primero = None
        self.ultimo = None
        self.tamanio = 0

    def estaVacia(self):
        return self.primero == None

    def Push(self, item):
        nuevo = Nodo(item)
        
        if self.primero != None: 
            self.ultimo.asignarSiguiente(nuevo)
        else:
            self.primero = nuevo
            
        self.ultimo = nuevo
        self.tamanio += 1
            
    def tamano(self):
        return self.tamanio

    def desplegar(self):
        actual = self.primero
        while actual != None:
            actual.obtenerInfo().desplegar()
            actual = actual.obtenerSiguiente()

    def buscar(self, item):
        actual = self.primero
        encontrado = False
        while actual != None and not encontrado:
            if actual.obtenerInfo().EsIgualALLave(item):
                encontrado = True
            else:
                actual = actual.obtenerSiguiente()

        return encontrado

    def Pop(self):
        if self.primero == None:
            print("Cola esta vacia")
            return None
        
        primerotemp = self.primero
        self.primero = self.primero.obtenerSiguiente()
        
        if self.primero == None:
            self.ultimo = None
            
        self.tamanio -= 1
        return primerotemp.obtenerInfo()
    
    def obtenerElementos(self):
        elementos = []
        actual = self.primero
        while actual != None:
            elementos.append(actual.obtenerInfo())
            actual = actual.obtenerSiguiente()
        return elementos
    
    def verFrente(self):
        if self.primero == None:
            return None
        return self.primero.obtenerInfo()