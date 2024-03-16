import tkinter as tk
from tkinter import ttk

# Estilos generales
COLOR_FONDO = "#f0f0f0"
COLOR_BOTON = "#d9d9d9"
FUENTE = ("Arial", 10)

class AplicacionGestionReservas:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Gestión de Reservas con Algoritmos Genéticos")
        self.ventana.configure(bg=COLOR_FONDO)

        # Configuración del layout
        self.configurar_ui()

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
        # Sección de entrada para los detalles de las reservas
        frame_reservas = tk.LabelFrame(self.ventana, text="Detalles de las Reservas", bg=COLOR_FONDO, font=FUENTE)
        frame_reservas.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        tk.Label(frame_reservas, text="Número de Noches:", bg=COLOR_FONDO, font=FUENTE).grid(row=0, column=0, sticky="w")
        tk.Entry(frame_reservas, font=FUENTE).grid(row=0, column=1, sticky="ew")

        tk.Label(frame_reservas, text="Número de Huéspedes:", bg=COLOR_FONDO, font=FUENTE).grid(row=1, column=0, sticky="w")
        self.num_huespedes = tk.Spinbox(frame_reservas, from_=1, to=5, font=FUENTE, width=5)
        self.num_huespedes.grid(row=1, column=1, sticky="ew")

        tk.Label(frame_reservas, text="Preferencias Especiales:", bg=COLOR_FONDO, font=FUENTE).grid(row=2, column=0, sticky="w")
        preferencias = ttk.Combobox(frame_reservas, values=["Sin preferencias", "Proximidad a instalaciones", "Preferencia por vista", "Accesibilidad"], font=FUENTE, state="readonly")
        preferencias.grid(row=2, column=1, sticky="ew")
        preferencias.current(0)

        # Sección para las características de las habitaciones
        frame_habitaciones = tk.LabelFrame(self.ventana, text="Características de las Habitaciones", bg=COLOR_FONDO, font=FUENTE)
        frame_habitaciones.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        tk.Label(frame_habitaciones, text="Tamaño:", bg=COLOR_FONDO, font=FUENTE).grid(row=0, column=0, sticky="w")
        self.tamano_habitacion = ttk.Combobox(frame_habitaciones, values=["Estándar", "Suite"], font=FUENTE, state="readonly")
        self.tamano_habitacion.grid(row=0, column=1, sticky="ew")
        self.tamano_habitacion.current(0)
        self.tamano_habitacion.bind("<<ComboboxSelected>>", self.actualizar_limite_huespedes)

        # Comodidades como casillas de verificación
        tk.Label(frame_habitaciones, text="Comodidades:", bg=COLOR_FONDO, font=FUENTE).grid(row=1, column=0, sticky="w", pady=5)
        comodidades = ["WiFi", "Aire acondicionado", "Minibar", "TV", "Caja fuerte"]
        self.comodidades_vars = []
        for i, comodidad in enumerate(comodidades, start=1):
            var = tk.BooleanVar()
            chk = tk.Checkbutton(frame_habitaciones, text=comodidad, var=var, bg=COLOR_FONDO, font=FUENTE)
            chk.grid(row=2, column=i, sticky="w")
            self.comodidades_vars.append(var)

        # Sección para la información contextual
        frame_contexto = tk.LabelFrame(self.ventana, text="Información Contextual", bg=COLOR_FONDO, font=FUENTE)
        frame_contexto.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        tk.Label(frame_contexto, text="Eventos Locales:", bg=COLOR_FONDO, font=FUENTE).grid(row=0, column=0, sticky="w")
        eventos = ttk.Combobox(frame_contexto, values=["Ninguno", "Evento local pequeño", "Evento importante"], font=FUENTE, state="readonly")
        eventos.grid(row=0, column=1, sticky="ew")
        eventos.current(0)

        tk.Label(frame_contexto, text="Temporada:", bg=COLOR_FONDO, font=FUENTE).grid(row=1, column=0, sticky="w")
        temporada = ttk.Combobox(frame_contexto, values=["Baja", "Media", "Alta"], font=FUENTE, state="readonly")
        temporada.grid(row=1, column=1, sticky="ew")
        temporada.current(0)

# Crear y ejecutar la aplicación
ventana_principal = tk.Tk()
app = AplicacionGestionReservas(ventana_principal)
ventana_principal.mainloop()
