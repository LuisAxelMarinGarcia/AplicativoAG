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

    def seleccionar_para_cruza(self, poblacion_con_aptitud):
        total_aptitud = sum([aptitud for _, aptitud in poblacion_con_aptitud])
        probabilidades = [aptitud / total_aptitud for _, aptitud in poblacion_con_aptitud]
        return random.choices(poblacion_con_aptitud, weights=probabilidades, k=2)

    def cruzar_en_punto_fijo(self, individuo1, individuo2):
        punto_cruza = len(individuo1) // 2
        return (individuo1[:punto_cruza] + individuo2[punto_cruza:], individuo2[:punto_cruza] + individuo1[punto_cruza:])

    def mutar_individuo(self, individuo, num_habitaciones):
        for i in range(len(individuo)):
            if random.random() < 0.05:  # Una tasa de mutación más razonable
                individuo[i] = random.randint(1, num_habitaciones)
        return individuo

    def evaluar_aptitud(self, individuo, preferencias, comodidades_seleccionadas, eventos, temporada, noches, huespedes, tamaño):
        # Inicializa el puntaje de aptitud total
        score_total = 0

        # Ponderaciones para las preferencias de los huéspedes
        preferencias_ponderaciones = {
            "Sin preferencias": 1.0,
            "Proximidad a instalaciones": 1.1,
            "Preferencia por vista": 1.2,
            "Accesibilidad": 1.15
        }

        # Ponderaciones para las comodidades seleccionadas
        comodidades_ponderaciones = {
            "WiFi": 1.2,
            "Aire acondicionado": 1.1,
            "Minibar": 1.15,
            "TV": 1.05,
            "Caja fuerte": 1.03
        }

        # Ponderaciones para los eventos locales
        evento_ponderaciones = {
            "Ninguno": 1.0,
            "Evento local pequeño": 1.05,
            "Evento importante": 1.1
        }

        # Ponderaciones para las temporadas
        temporada_ponderaciones = {
            "Baja": 1.0,
            "Media": 1.1,
            "Alta": 1.2
        }

        # Máximo de huéspedes permitidos por tipo de habitación
        max_huespedes_permitidos = {
            "Estándar": 2,
            "Suite": 4  # Ajusta estos valores según las capacidades reales
        }

        max_huespedes = max_huespedes_permitidos[tamaño]

        # Evalúa cada habitación asignada en el individuo
        for habitacion in individuo:
            habitacion_score = 10  # Puntuación base para cada habitación
            
            # Ajustar la puntuación en base a las preferencias
            habitacion_score *= preferencias_ponderaciones[preferencias]

            # Penalización por exceder el límite de huéspedes
            if huespedes > max_huespedes:
                habitacion_score *= 0.5

            # Ajuste por comodidades seleccionadas
            for comodidad in comodidades_seleccionadas:
                if comodidad in comodidades_ponderaciones:
                    habitacion_score *= comodidades_ponderaciones[comodidad]

            # Ajustes por eventos y temporada
            habitacion_score *= evento_ponderaciones[eventos]
            habitacion_score *= temporada_ponderaciones[temporada]

            # Agrega la puntuación de esta habitación al puntaje total
            score_total += habitacion_score

        # Retorna el puntaje total de aptitud para este individuo
        return score_total


    def iniciar_optimizacion(self):
        # Recogida de datos de la interfaz
        noches = int(self.entradas_noche.get())
        huespedes = int(self.num_huespedes.get())
        preferencias = self.preferencias.get()
        tamaño = self.tamano_habitacion.get()
        comodidades_seleccionadas = [comodidad for var, comodidad in zip(self.comodidades_vars, ["WiFi", "Aire acondicionado", "Minibar", "TV", "Caja fuerte"]) if var.get()]
        eventos = self.eventos.get()
        temporada = self.temporada.get()

        # Configuración inicial del algoritmo
        num_habitaciones = 20 if tamaño == "Suite" else 10
        tamano_poblacion = 10
        generaciones = 20

        # Proceso de optimización
        poblacion = self.generar_poblacion_inicial(tamano_poblacion, num_habitaciones)
        for _ in range(generaciones):
            poblacion_con_aptitud = [(ind, self.evaluar_aptitud(ind, preferencias, comodidades_seleccionadas, eventos, temporada, noches, huespedes, tamaño)) for ind in poblacion]
            nueva_poblacion = []
            while len(nueva_poblacion) < tamano_poblacion:
                padre1, padre2 = [p[0] for p in self.seleccionar_para_cruza(poblacion_con_aptitud)]
                hijo1, hijo2 = self.cruzar_en_punto_fijo(padre1, padre2)
                nueva_poblacion.extend([self.mutar_individuo(hijo1, num_habitaciones), self.mutar_individuo(hijo2, num_habitaciones)])

            poblacion = nueva_poblacion[:tamano_poblacion]

        # Evaluación final y selección de la mejor solución...
        poblacion_final_con_aptitud = [(ind, self.evaluar_aptitud(ind, preferencias, comodidades_seleccionadas, eventos, temporada, noches, huespedes, tamaño)) for ind in poblacion]
        mejor_solucion, mejor_aptitud = max(poblacion_final_con_aptitud, key=lambda x: x[1])

        # Mostrar la mejor solución en la interfaz y luego en la ventana de resultados
        resultado_str = f"Mejor solución encontrada con aptitud {mejor_aptitud}: {mejor_solucion}"
        self.resultado_label.config(text=resultado_str)
        
        # Mostrar la ventana de resultados detallados basados en la mejor solución
        self.mostrar_resultados(noches, huespedes, tamaño, preferencias, comodidades_seleccionadas, eventos, temporada)

                
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
        
    
    def mostrar_resultados(self, noches, huespedes, tamaño, preferencias, comodidades_seleccionadas, eventos, temporada):
        # Crear una nueva ventana para mostrar los resultados
        ventana_resultados = tk.Toplevel(self.ventana)
        ventana_resultados.title("Resultados de la Optimización")
        ventana_resultados.configure(bg=COLOR_FONDO)

        # Mostrar los detalles de la reserva
        detalles_reserva = (f"Número de noches: {noches}\n"
                            f"Número de huéspedes: {huespedes}\n"
                            f"Tamaño de habitación: {tamaño}\n"
                            f"Preferencias especiales: {preferencias}\n"
                            f"Comodidades seleccionadas: {', '.join(comodidades_seleccionadas) if comodidades_seleccionadas else 'Ninguna'}\n"
                            f"Evento local durante la estancia: {eventos}\n"
                            f"Temporada de la reserva: {temporada}\n")

        tk.Label(ventana_resultados, text="Detalles de la reserva:\n" + detalles_reserva, bg=COLOR_FONDO, font=FUENTE, wraplength=500).pack(pady=10)

        # Simulación de la ocupación del hotel y recomendaciones
        ocupacion_estimada = self.calcular_ocupacion_hotel(noches, temporada)
        recomendacion_precio = self.generar_recomendacion_precio(ocupacion_estimada)

        tk.Label(ventana_resultados, text=f"Ocupación del hotel estimada para el período de la reserva: {ocupacion_estimada:.2f}%", bg=COLOR_FONDO, font=FUENTE).pack(pady=10)
        tk.Label(ventana_resultados, text=f"Recomendación: {recomendacion_precio}", bg=COLOR_FONDO, font=FUENTE).pack(pady=10)
        
    def calcular_ocupacion_hotel(self, noches, temporada):
        # Suponemos que tenemos una ocupación base que varía según la temporada
        base_ocupacion_temporada = {
            'Baja': 50,  # 50% de ocupación base en temporada baja
            'Media': 70,  # 70% de ocupación base en temporada media
            'Alta': 90,  # 90% de ocupación base en temporada alta
        }
        
        # Asumimos que la ocupación puede variar en un 10% diario debido a factores no controlables (azar)
        variacion_aleatoria = sum(random.uniform(-0.1, 0.1) for _ in range(noches))
        ocupacion_estimada = base_ocupacion_temporada[temporada] + (variacion_aleatoria * 100)
        
        # Asegurarnos de que la ocupación esté entre 0% y 100%
        ocupacion_estimada = max(0, min(100, ocupacion_estimada))
        
        return ocupacion_estimada

    def generar_recomendacion_precio(self, ocupacion_hotel):
        # Definimos umbrales de ocupación para nuestras recomendaciones de precios
        if ocupacion_hotel > 85:
            return "Considerar aumento de precios por alta demanda"
        elif ocupacion_hotel < 40:
            return "Evaluar promociones para incrementar la ocupación"
        else:
            return "Mantener precios actuales"

    def configurar_ui(self):
        frame_reservas = tk.LabelFrame(self.ventana, text="Detalles de las Reservas", bg=COLOR_FONDO, font=FUENTE)
        frame_reservas.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        tk.Label(frame_reservas, text="Número de Noches:", bg=COLOR_FONDO, font=FUENTE).grid(row=0, column=0, sticky="w")
        self.entradas_noche = tk.Entry(frame_reservas, font=FUENTE)
        self.entradas_noche.grid(row=0, column=1, sticky="ew")

        tk.Label(frame_reservas, text="Número de Huéspedes:", bg=COLOR_FONDO, font=FUENTE).grid(row=1, column=0, sticky="w")
        self.num_huespedes = tk.Spinbox(frame_reservas, from_=1, to=5, font=FUENTE, width=5)
        self.num_huespedes.grid(row=1, column=1, sticky="ew")

        tk.Label(frame_reservas, text="Preferencias Especiales:", bg=COLOR_FONDO, font=FUENTE).grid(row=2, column=0, sticky="w")
        self.preferencias = ttk.Combobox(frame_reservas, values=["Sin preferencias", "Proximidad a instalaciones", "Preferencia por vista", "Accesibilidad"], font=FUENTE, state="readonly")
        self.preferencias.grid(row=2, column=1, sticky="ew")
        self.preferencias.current(0)

        frame_habitaciones = tk.LabelFrame(self.ventana, text="Características de las Habitaciones", bg=COLOR_FONDO, font=FUENTE)
        frame_habitaciones.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        tk.Label(frame_habitaciones, text="Tamaño:", bg=COLOR_FONDO, font=FUENTE).grid(row=0, column=0, sticky="w")
        self.tamano_habitacion = ttk.Combobox(frame_habitaciones, values=["Estándar", "Suite"], font=FUENTE, state="readonly")
        self.tamano_habitacion.grid(row=0, column=1, sticky="ew")
        self.tamano_habitacion.current(0)
        self.tamano_habitacion.bind("<<ComboboxSelected>>", self.actualizar_limite_huespedes)

        tk.Label(frame_habitaciones, text="Comodidades:", bg=COLOR_FONDO, font=FUENTE).grid(row=1, column=0, sticky="w", pady=5)
        comodidades = ["WiFi", "Aire acondicionado", "Minibar", "TV", "Caja fuerte"]
        self.comodidades_vars = []
        for i, comodidad in enumerate(comodidades):
            var = tk.BooleanVar()
            chk = tk.Checkbutton(frame_habitaciones, text=comodidad, var=var, bg=COLOR_FONDO, font=FUENTE)
            chk.grid(row=2, column=i, sticky="w")
            self.comodidades_vars.append(var)

        frame_contexto = tk.LabelFrame(self.ventana, text="Información Contextual", bg=COLOR_FONDO, font=FUENTE)
        frame_contexto.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        tk.Label(frame_contexto, text="Eventos Locales:", bg=COLOR_FONDO, font=FUENTE).grid(row=0, column=0, sticky="w")
        self.eventos = ttk.Combobox(frame_contexto, values=["Ninguno", "Evento local pequeño", "Evento importante"], font=FUENTE, state="readonly")
        self.eventos.grid(row=0, column=1, sticky="ew")
        self.eventos.current(0)

        tk.Label(frame_contexto, text="Temporada:", bg=COLOR_FONDO, font=FUENTE).grid(row=1, column=0, sticky="w")
        self.temporada = ttk.Combobox(frame_contexto, values=["Baja", "Media", "Alta"], font=FUENTE, state="readonly")
        self.temporada.grid(row=1, column=1, sticky="ew")
        self.temporada.current(0)

        # Botón para iniciar la optimización
        boton_optimizar = tk.Button(self.ventana, text="Iniciar Optimización", bg=COLOR_BOTON, font=FUENTE, command=self.iniciar_optimizacion)
        boton_optimizar.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

        # Etiqueta para mostrar el resultado de la optimización
        self.resultado_label = tk.Label(self.ventana, text="", bg=COLOR_FONDO, font=FUENTE)
        self.resultado_label.grid(row=4, column=0, padx=10, pady=10, sticky="ew")

# Crear y ejecutar la aplicación
ventana_principal = tk.Tk()
app = AplicacionGestionReservas(ventana_principal)
ventana_principal.mainloop()