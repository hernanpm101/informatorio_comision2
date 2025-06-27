import tkinter as tk
from datetime import datetime
from tkinter import messagebox
import pygame.mixer   #alarma.mp3
import os

class RelojApp(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # Diccionarios para la traducción manual de días y meses
        self.dias_semana = {
            "Monday": "Lunes", "Tuesday": "Martes", "Wednesday": "Miércoles",
            "Thursday": "Jueves", "Friday": "Viernes", "Saturday": "Sábado", "Sunday": "Domingo"
        }
        self.meses_anio = {
            "January": "Enero", "February": "Febrero", "March": "Marzo",
            "April": "Abril", "May": "Mayo", "June": "Junio", "July": "Julio",
            "August": "Agosto", "September": "Septiembre", "October": "Octubre",
            "November": "Noviembre", "December": "Diciembre"
        }
        
        self.title("Alumnos: Roma, Delgado Labrovich y Perez Melgar. Grupo 12-TKinder RelojApp")
        self.geometry("600x460") 
        self.resizable(False, False)
        self.configure(bg="black")

        # Inicializar el mezclador de Pygame para el sonido
        try:
            pygame.mixer.init()
        except Exception as e:
            messagebox.showerror("Error de Inicialización de Audio", f"No se pudo inicializar el sistema de audio de Pygame: {e}")
            print(f"Error al inicializar pygame.mixer: {e}")

        # Variable para almacenar la hora de la alarma
        self.alarm_time = None
        
        self.create_widgets()
        self.update_datetime()

    def create_widgets(self):
        """Crea y empaqueta los widgets de la interfaz."""
        # Etiqueta para la fecha
        self.date_label = tk.Label(
            self,
            font=("Arial", 25, "bold"),
            bg="black",
            fg="cyan"
        )
        self.date_label.pack(pady=10)

        # Etiqueta para la hora
        self.time_label = tk.Label(
            self,
            font=("Arial", 70, "bold"),
            bg="black",
            fg="lime green"
        )
        self.time_label.pack(expand=True)
        
        # Alarma
        alarm_frame = tk.Frame(self, bg="black")
        alarm_frame.pack(pady=20)
        
        # Etiqueta para el campo de entrada
        alarm_label = tk.Label(
            alarm_frame,
            text="⏰ Alarma para la clase del INFO. Comisión 2 (HH:MM):",
            font=("Arial", 14),
            bg="black",
            fg="white"
        )
        alarm_label.pack(pady=5) # Lo empaquetamos arriba de todo en el frame
        
        # Campo de entrada para la hora de la alarma
        self.alarm_entry = tk.Entry(
            alarm_frame,
            font=("Arial", 14),
            width=8,
            bg="gray20",
            fg="white",
            insertbackground="white" # Color del cursor
        )
        self.alarm_entry.pack(pady=5) # Lo empaquetamos después de la etiqueta
        
        # Botón para activar la alarma
        set_alarm_button = tk.Button(
            alarm_frame,
            text="Activar Alarma",
            font=("Arial", 12, "bold"),
            bg="lime green",
            fg="black",
            command=self.set_alarm
        )
        set_alarm_button.pack(pady=5) # Empaquetado verticalmente
        
        # Botón para apagar la alarma manualmente
        stop_alarm_button = tk.Button(
            alarm_frame,
            text="Apagar Alarma",
            font=("Arial", 12, "bold"),
            bg="red",
            fg="white",
            command=self.stop_alarm
        )
        stop_alarm_button.pack(pady=5) # Empaquetado debajo del botón de activar

        # Etiqueta para mostrar el estado de la alarma
        self.alarm_status_label = tk.Label(
            self,
            text="Alarma: Desactivada",
            font=("Arial", 12),
            bg="black",
            fg="red"
        )
        self.alarm_status_label.pack(pady=5)

    def update_datetime(self):
        """
        Actualiza la fecha y la hora, y verifica la alarma.
        """
        now = datetime.now()
        
        # Hora y fecha formateadas
        current_time_str = now.strftime("%H:%M:%S")
        
        # Formato de la fecha: Día, DD de Mes de AAAA tipo Argentina
        current_date_str = now.strftime("%A, %d de %B de %Y")
        
        # Reemplazo los nombres en inglés por sus equivalentes en español
        for en, es in self.dias_semana.items():
            current_date_str = current_date_str.replace(en, es)
        for en, es in self.meses_anio.items():
            current_date_str = current_date_str.replace(en, es)

        self.time_label.config(text=current_time_str)
        self.date_label.config(text=current_date_str)
        
        # Verificación de la Alarma
        if self.alarm_time and now.strftime("%H:%M") == self.alarm_time:
            self.trigger_alarm()
        
        # Llama a esta función cada 1 segundo (1000 milisegundos)
        self.after(1000, self.update_datetime)

    def set_alarm(self):
        """
        Guarda la hora de la alarma ingresada por el usuario.
        """
        alarm_input = self.alarm_entry.get()
        
        # Validacion el formato de la entrada (HH:MM)
        try:
            # parsear la hora para ver si tiene el formato correcto
            datetime.strptime(alarm_input, "%H:%M")
            self.alarm_time = alarm_input
            self.alarm_entry.delete(0, tk.END) # Limpiamos el campo
            self.alarm_status_label.config(text=f"Alarma activa para las {self.alarm_time}", fg="lime green")
            messagebox.showinfo("Alarma", f"¡Alarma configurada para las {self.alarm_time}!")
            
        except ValueError:
            messagebox.showerror("Error", "Formato de hora inválido. Usa HH:MM (ej. 14:30)")
            self.alarm_status_label.config(text="Alarma: Desactivada (Error en formato)", fg="red")
            self.alarm_time = None
            
    def play_alarm_sound(self):
        """
        Reproduce un archivo de sonido para la alarma usando pygame.mixer.
        Asegúrate de tener un archivo de sonido (ej. 'alarma.mp3' o 'alarma.wav') en el mismo directorio.
        """
        try:
            # Obtiene la ruta absoluta del directorio donde se encuentra este script
            script_dir = os.path.dirname(__file__)
            # Construye la ruta completa al archivo de sonido
            sound_file_path = os.path.join(script_dir, 'alarma.mp3') 
            
            # Carga el archivo de sonido
            pygame.mixer.music.load(sound_file_path)
            # Reproduce el sonido en un bucle continuo hasta que se detenga
            pygame.mixer.music.play(-1) 
        except pygame.error as e:
            messagebox.showerror("Error de Sonido", f"No se pudo reproducir el sonido: {e}\nAsegúrate de que 'alarma.mp3' existe en la misma carpeta que el script y es compatible con Pygame.")
            print(f"Error al reproducir sonido con pygame.mixer: {e}")

    def trigger_alarm(self):
        """
        Muestra la notificación y reproduce el sonido cuando la alarma suena.
        La alarma se desactiva inmediatamente después de activarse para evitar bucles.
        """
        if self.alarm_time is not None:
            self.play_alarm_sound()
            messagebox.showinfo("¡ALARMA!", "¡Es hora de la clase del INFORMATORIO, PRENDE LA COMPU!")
            # El sonido seguirá sonando hasta que el usuario lo detenga manualmente.
            self.alarm_time = None
            self.alarm_status_label.config(text="Alarma: Sonando...", fg="orange")
            
    def stop_alarm(self):
        """
        Detiene la reproducción del sonido de la alarma y la desactiva.
        """
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
            messagebox.showinfo("Alarma", "Alarma detenida manualmente, gracias ya me dolia la cabeza!.")
        
        self.alarm_time = None
        self.alarm_status_label.config(text="Alarma: Desactivada", fg="red")
                
if __name__ == "__main__":
    app = RelojApp()
    app.mainloop()
