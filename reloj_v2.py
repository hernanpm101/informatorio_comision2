import tkinter as tk
from datetime import datetime
from tkinter import messagebox

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
        
        self.title("Proyecto Tkinter Reloj con alarma para la clase del INFORMATORIO 2025")
        self.geometry("600x400") 
        self.resizable(False, False)
        self.configure(bg="black")

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
            text="Alarma para la clase del INFO (HH:MM):",
            font=("Arial", 14),
            bg="black",
            fg="white"
        )
        alarm_label.pack(side="left", padx=10)
        
        # Campo de entrada para la hora de la alarma
        self.alarm_entry = tk.Entry(
            alarm_frame,
            font=("Arial", 14),
            width=8,
            bg="gray20",
            fg="white",
            insertbackground="white" # Color del cursor
        )
        self.alarm_entry.pack(side="left", padx=5)
        
        # Botón para activar la alarma
        set_alarm_button = tk.Button(
            alarm_frame,
            text="Activar Alarma",
            font=("Arial", 12, "bold"),
            bg="lime green",
            fg="black",
            command=self.set_alarm
        )
        set_alarm_button.pack(side="left", padx=10)
        
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
        
        # Formato de la fecha: Día, DD de Mes de YYYY tipo Argentina
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
        
        # Validamos el formato de la entrada (HH:MM)
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
            
    def trigger_alarm(self):
        """
        Muestra la notificación cuando la alarma suena.
        """
        # Detenemos la alarma para que no siga sonando en cada segundo
        self.alarm_time = None
        self.alarm_status_label.config(text="Alarma: Desactivada", fg="red")
        
        # Muestra un cuadro de mensaje
        messagebox.showinfo("¡ALARMA!", "¡Es hora de la clase del INFORMATORIO!")
               
if __name__ == "__main__":
    app = RelojApp()
    app.mainloop()