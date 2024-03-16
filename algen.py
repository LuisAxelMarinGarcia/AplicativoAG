import tkinter as tk
from tkinter import ttk
import random
import itertools

# Estilos generales
COLOR_FONDO = "#f0f0f0"
COLOR_BOTON = "#d9d9d9"
FUENTE = ("Arial", 10)


class AplicacionGestionReservas:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Gestión de Reservas con Algoritmos Genéticos")
        self.ventana.configure(bg=COLOR_FONDO)
        self.configurar_ui()

    def generar_poblacion_inicial(self, tamano_poblacion, num_habitaciones):
        return [[random.randint(1, num_habitaciones) for _ in range(tamano_poblacion)] for _ in range(tamano_poblacion)]

    def formar_parejas(self, poblacion):
        return list(itertools.combinations(poblacion, 2))

    def cruzar_en_punto_fijo(self, individuo1, individuo2):
        """
        Realiza un cruzamiento en un solo punto fijo entre dos individuos.
        """
        punto_cruza = len(individuo1) // 2  # Punto fijo en la mitad del individuo
        nuevo_individuo1 = individuo1[:punto_cruza] + individuo2[punto_cruza:]
        nuevo_individuo2 = individuo2[:punto_cruza] + individuo1[punto_cruza:]
        return nuevo_individuo1, nuevo_individuo2

    def iniciar_optimizacion(self):
        noches = int(self.entradas_reservas['Número de Noches'].get())
        huespedes = int(self.num_huespedes.get())
        preferencias = self.preferencias.get()
        tamaño = self.tamano_habitacion.get()
        comodidades_seleccionadas = [var.get() for var in self.comodidades_vars]
        eventos = self.eventos.get()
        temporada = self.temporada.get()

        # Asumir que el número de habitaciones varía con el tamaño seleccionado
        num_habitaciones = 20 if tamaño == "Suite" else 10
        tamano_poblacion = 10  # Asumiendo un tamaño fijo para el ejemplo

        poblacion = self.generar_poblacion_inicial(tamano_poblacion, num_habitaciones)
        parejas = self.formar_parejas(poblacion)

        print(f"Parejas formadas: {len(parejas)}")
        # Aquí continuaría la lógica para el cruzamiento, mutación, etc.

    def actualizar_limite_huespedes(self, event):
        # Actualizar el límite de huéspedes basado en el tamaño de la habitación
        tamano = self.tamano_habitacion.get()
        if tamano == "Estándar":
            self.num_huespedes.config(to=5)
        elif tamano == "Suite":
            self.num_huespedes.config(to=10)
        else:
            self.num_huespedes.config(to=5)

        # Resetea el valor cuando se cambia el tamaño de habitación
        self.num_huespedes.delete(0, 'end')
        self.num_huespedes.insert(0, "1")


    def configurar_ui(self):
        frame_reservas = tk.LabelFrame(self.ventana, text="Detalles de las Reservas", bg="#f0f0f0", font=("Arial", 10))
        frame_reservas.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        tk.Label(frame_reservas, text="Número de Noches:", bg="#f0f0f0", font=("Arial", 10)).grid(row=0, column=0, sticky="w")
        tk.Entry(frame_reservas, font=("Arial", 10)).grid(row=0, column=1, sticky="ew")

        tk.Label(frame_reservas, text="Número de Huéspedes:", bg="#f0f0f0", font=("Arial", 10)).grid(row=1, column=0, sticky="w")
        self.num_huespedes = tk.Spinbox(frame_reservas, from_=1, to=5, font=("Arial", 10), width=5)
        self.num_huespedes.grid(row=1, column=1, sticky="ew")

        tk.Label(frame_reservas, text="Preferencias Especiales:", bg="#f0f0f0", font=("Arial", 10)).grid(row=2, column=0, sticky="w")
        self.preferencias = ttk.Combobox(frame_reservas, values=["Sin preferencias", "Proximidad a instalaciones", "Preferencia por vista", "Accesibilidad"], font=("Arial", 10), state="readonly")
        self.preferencias.grid(row=2, column=1, sticky="ew")
        self.preferencias.current(0)

        frame_habitaciones = tk.LabelFrame(self.ventana, text="Características de las Habitaciones", bg="#f0f0f0", font=("Arial", 10))
        frame_habitaciones.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        tk.Label(frame_habitaciones, text="Tamaño:", bg="#f0f0f0", font=("Arial", 10)).grid(row=0, column=0, sticky="w")
        self.tamano_habitacion = ttk.Combobox(frame_habitaciones, values=["Estándar", "Suite"], font=("Arial", 10), state="readonly")
        self.tamano_habitacion.grid(row=0, column=1, sticky="ew")
        self.tamano_habitacion.current(0)
        self.tamano_habitacion.bind("<<ComboboxSelected>>", self.actualizar_limite_huespedes)

        tk.Label(frame_habitaciones, text="Comodidades:", bg="#f0f0f0", font=("Arial", 10)).grid(row=1, column=0, sticky="w", pady=5)
        comodidades = ["WiFi", "Aire acondicionado", "Minibar", "TV", "Caja fuerte"]
        self.comodidades_vars = []
        for i, comodidad in enumerate(comodidades, start=1):
            var = tk.BooleanVar()
            chk = tk.Checkbutton(frame_habitaciones, text=comodidad, var=var, bg="#f0f0f0", font=("Arial", 10))
            chk.grid(row=2, column=i, sticky="w")
            self.comodidades_vars.append(var)

        frame_contexto = tk.LabelFrame(self.ventana, text="Información Contextual", bg="#f0f0f0", font=("Arial", 10))
        frame_contexto.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        tk.Label(frame_contexto, text="Eventos Locales:", bg="#f0f0f0", font=("Arial", 10)).grid(row=0, column=0, sticky="w")
        self.eventos = ttk.Combobox(frame_contexto, values=["Ninguno", "Evento local pequeño", "Evento importante"], font=("Arial", 10), state="readonly")
        self.eventos.grid(row=0, column=1, sticky="ew")
        self.eventos.current(0)

        tk.Label(frame_contexto, text="Temporada:", bg="#f0f0f0", font=("Arial", 10)).grid(row=1, column=0, sticky="w")
        self.temporada = ttk.Combobox(frame_contexto, values=["Baja", "Media", "Alta"], font=("Arial", 10), state="readonly")
        self.temporada.grid(row=1, column=1, sticky="ew")
        self.temporada.current(0)
# Crear y ejecutar la aplicación
ventana_principal = tk.Tk()
app = AplicacionGestionReservas(ventana_principal)
ventana_principal.mainloop()
