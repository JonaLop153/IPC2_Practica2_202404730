import tkinter as tk
from tkinter import ttk, messagebox
from gestor_turnos import GestorTurnos
from graficador import Graficador
import os

try:
    import graphviz
except ImportError:
    messagebox.showerror("Error", "Graphviz no está instalado. Ejecuta: pip install graphviz")
    exit()

class AplicacionTurnos:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gestión de Turnos Médicos")
        self.root.geometry("1000x700")
        
        self.gestor = GestorTurnos()
        self.especialidades = ["Medicina General", "Pediatría", "Ginecología", "Dermatología"]
        self.graph_image = None  # Para mantener referencia a la imagen actual
        
        self.configurar_interfaz()
        self.actualizar_interfaz()
    
    def configurar_interfaz(self):
        # Frame principal con paned window para dividir la interfaz
        main_paned = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        main_paned.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Frame izquierdo para controles
        left_frame = ttk.Frame(main_paned, padding="10")
        right_frame = ttk.Frame(main_paned, padding="10")
        
        main_paned.add(left_frame, weight=1)
        main_paned.add(right_frame, weight=2)
        
        # ===== LEFT FRAME - CONTROLES =====
        ttk.Label(left_frame, text="Registrar Nuevo Turno", font=("Times New Roman", 15, "bold")).grid(row=0, column=0, columnspan=2, pady=10, sticky=tk.W)
        
        ttk.Label(left_frame, text="Nombre:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.nombre_entry = ttk.Entry(left_frame, width=25)
        self.nombre_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(left_frame, text="Edad:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.edad_entry = ttk.Entry(left_frame, width=10)
        self.edad_entry.grid(row=2, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(left_frame, text="Especialidad:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.especialidad_combo = ttk.Combobox(left_frame, values=self.especialidades, state="readonly", width=22)
        self.especialidad_combo.grid(row=3, column=1, sticky=tk.W, pady=5)
        
        ttk.Button(left_frame, text="Registrar Turno", command=self.registrar_turno).grid(row=4, column=0, columnspan=2, pady=10)
        
        # Separador
        ttk.Separator(left_frame, orient=tk.HORIZONTAL).grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        # Sección de atención
        ttk.Label(left_frame, text="Atención de Turnos", font=("Times New Roman", 15, "bold")).grid(row=6, column=0, columnspan=2, pady=10, sticky=tk.W)
        
        ttk.Button(left_frame, text="Atender Siguiente Turno", command=self.atender_turno).grid(row=7, column=0, columnspan=2, pady=5)
        
        # Información de turno actual
        self.info_label = ttk.Label(left_frame, text="No hay turnos en atención", wraplength=250)
        self.info_label.grid(row=8, column=0, columnspan=2, pady=10)
        
        # Tiempo estimado de espera
        self.tiempo_label = ttk.Label(left_frame, text="Tiempo estimado de espera: 0 minutos")
        self.tiempo_label.grid(row=9, column=0, columnspan=2, pady=5)
        
        # Separador
        ttk.Separator(left_frame, orient=tk.HORIZONTAL).grid(row=10, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        # Botones adicionales
        button_frame = ttk.Frame(left_frame)
        button_frame.grid(row=11, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="Generar Gráfico", command=self.generar_grafico).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Actualizar Vista", command=self.actualizar_vista_graphviz).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Limpiar Campos", command=self.limpiar_campos).pack(side=tk.LEFT, padx=5)
        
        # Configurar expansión left frame
        left_frame.columnconfigure(1, weight=1)
        
        # ===== RIGHT FRAME - VISUALIZACIÓN GRAPHVIZ =====
        ttk.Label(right_frame, text="Visualización de la Cola", font=("Times New Roman", 15, "bold")).grid(row=0, column=0, pady=5, sticky=tk.W)
        
        # Frame para la imagen Graphviz
        graph_frame = ttk.Frame(right_frame, relief=tk.SUNKEN, borderwidth=2)
        graph_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        graph_frame.columnconfigure(0, weight=1)
        graph_frame.rowconfigure(0, weight=1)
        
        # Label para mostrar la imagen
        self.graph_label = ttk.Label(graph_frame, text="No hay turnos para mostrar", background="#beeacc")
        self.graph_label.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Configurar expansión right frame
        right_frame.columnconfigure(0, weight=1)
        right_frame.rowconfigure(1, weight=1)

    def actualizar_vista_graphviz(self):
        """Actualiza la visualización Graphviz de la cola"""
        if not self.gestor.hay_turnos_pendientes():
            self.graph_label.config(text="No hay turnos para mostrar", image='')
            return
        
        turnos = self.gestor.obtener_turnos_pendientes()
        new_image = Graficador.generar_imagen_tkinter(turnos)
        
        if new_image:
            # Liberar referencia anterior para evitar memory leak
            self.graph_image = None
            self.graph_image = new_image
            self.graph_label.config(image=self.graph_image, text='')
        else:
            self.graph_label.config(text="Error al generar visualización", image='')

    def registrar_turno(self):
        nombre = self.nombre_entry.get().strip()
        edad = self.edad_entry.get().strip()
        especialidad = self.especialidad_combo.get()
        
        if not nombre or not edad or not especialidad:
            messagebox.showerror("Error", "Por favor, complete todos los campos.")
            return
        
        try:
            edad = int(edad)
            if edad <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese una edad válida.")
            return
        
        turno = self.gestor.registrar_turno(nombre, edad, especialidad)
        messagebox.showinfo("Éxito", f"Turno registrado para {nombre}.\nTiempo estimado de espera: {self.gestor.obtener_tiempo_espera_estimado()} minutos")
        
        self.limpiar_campos()
        self.actualizar_interfaz()
        self.actualizar_vista_graphviz()
    
    def atender_turno(self):
        if not self.gestor.hay_turnos_pendientes():
            messagebox.showinfo("Información", "No hay turnos pendientes para atender.")
            self.info_label.config(text="No hay turnos en atención")
            return
        
        turno_atendido = self.gestor.atender_turno()
        self.info_label.config(text=f"Atendiendo: {turno_atendido}\nTiempo de atención: {turno_atendido.obtenerTiempoAtencion()} minutos")
        
        messagebox.showinfo("Turno Atendido", f"Se atendió a: {turno_atendido}")
        self.actualizar_interfaz()
        self.actualizar_vista_graphviz()
    
    def generar_grafico(self):
        if not self.gestor.hay_turnos_pendientes():
            messagebox.showinfo("Información", "No hay turnos para generar gráfico.")
            return
        
        turnos = self.gestor.obtener_turnos_pendientes()
        dot, archivo = Graficador.generar_grafico_cola(turnos)
        
        if dot:
            messagebox.showinfo("Gráfico Generado", f"Se ha generado el archivo '{archivo}'")
        else:
            messagebox.showerror("Error", "No se pudo generar el gráfico")
    
    def actualizar_interfaz(self):
        # Actualizar tiempo estimado
        tiempo_espera = self.gestor.obtener_tiempo_espera_estimado()
        self.tiempo_label.config(text=f"Tiempo estimado de espera: {tiempo_espera} minutos")
        
        # Actualizar información del próximo turno
        proximo = self.gestor.ver_proximo_turno()
        if proximo:
            self.info_label.config(text=f"Próximo: {proximo}")
        else:
            self.info_label.config(text="No hay turnos en atención")
    
    def limpiar_campos(self):
        self.nombre_entry.delete(0, tk.END)
        self.edad_entry.delete(0, tk.END)
        self.especialidad_combo.set('')

if __name__ == "__main__":
    root = tk.Tk()
    app = AplicacionTurnos(root)
    root.mainloop()