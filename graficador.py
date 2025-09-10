import graphviz
import tempfile
import os
from PIL import Image, ImageTk

class Graficador:
    @staticmethod
    def generar_grafico_cola(turnos, nombre_archivo="cola_turnos"):
        if not turnos:
            return None, "No hay turnos para graficar"
            
        dot = graphviz.Digraph(comment='Cola de Turnos Médicos')
        dot.attr(rankdir='LR')
        dot.attr('node', shape='box', style='filled', fillcolor='lightblue')

        # Crear nodos
        for i, turno in enumerate(turnos):
            label = (f"{turno.obtenerNombre()}\\n"
                    f"Edad: {turno.obtenerEdad()}\\n"
                    f"Especialidad: {turno.obtenerEspecialidad()}\\n"
                    f"Tiempo: {turno.obtenerTiempoAtencion()} min")
            dot.node(f'node{i}', label)

        # Conexiones entre nodos
        for i in range(len(turnos) - 1):
            dot.edge(f'node{i}', f'node{i+1}')

        # Guardar y devolver
        dot.render(nombre_archivo, format='png', cleanup=True)
        return dot, f"{nombre_archivo}.png"

    @staticmethod
    def generar_imagen_tkinter(turnos):
        """Genera una imagen de la cola y devuelve un PhotoImage para Tkinter"""
        if not turnos:
            return None

        # Crear gráfico con Graphviz
        dot = graphviz.Digraph()
        dot.attr(rankdir='LR')
        dot.attr('node', shape='box', style='filled', fillcolor='lightblue')
        dot.attr(size='6,4')  # Tamaño del gráfico

        # Nodos
        for i, turno in enumerate(turnos):
            label = (f"{turno.obtenerNombre()}\\n"
                    f"Edad: {turno.obtenerEdad()}\\n"
                    f"Especialidad: {turno.obtenerEspecialidad()}\\n"
                    f"Tiempo: {turno.obtenerTiempoAtencion()} min")
            dot.node(f'node{i}', label)

        # Aristas
        for i in range(len(turnos) - 1):
            dot.edge(f'node{i}', f'node{i+1}')

        # Guardar en archivo temporal
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
            filename = tmp.name

        try:
            # Renderizar y guardar
            dot.render(filename, format='png', cleanup=True)
            # Abrir la imagen
            img = Image.open(filename + '.png')
            # Convertir a PhotoImage
            photo = ImageTk.PhotoImage(img)
            return photo
        except Exception as e:
            print(f"Error generando imagen: {e}")
            return None
        finally:
            # Eliminar el archivo temporal
            temp_png = filename + '.png'
            if os.path.exists(temp_png):
                os.unlink(temp_png)