import time
import tkinter as tk
from tkinter import messagebox
from playsound import playsound

class PomodoroTimer:
    def __init__(self, master):
        self.master = master
        self.master.title("Pomodoro")
        self.master.geometry("400x350")

        self.timer_label = tk.Label(master, font=("Arial", 24), text="00:00")
        self.timer_label.pack(pady=20)

        self.work_button = tk.Button(master, text="Iniciar Expediente", command=self.start_pomodoro_work)
        self.work_button.pack(pady=10)

        self.lunch_button = tk.Button(master, text="Iniciar Intervalo de Almoço", command=self.start_lunch_break)
        self.lunch_button.pack(pady=10)

        self.break_button = tk.Button(master, text="Iniciar Pausa Curta", command=self.start_short_break)
        self.break_button.pack(pady=10)

        self.is_paused = False
        self.remaining_time = 0
        self.start_time = 0

    def start_pomodoro_work(self):
        work_time = 25 * 60  # 25 minutos em segundos
        self.countdown(work_time)

    def start_lunch_break(self):
        lunch_break_time = 60 * 60  # 1 hora em segundos
        self.countdown(lunch_break_time)

    def start_short_break(self):
        short_break_time = 15 * 60  # 15 minutos em segundos
        self.countdown(short_break_time)

    def countdown(self, seconds):
        self.start_time = time.time()
        self.remaining_time = seconds

        while self.remaining_time >= 0 and not self.is_paused:
            minutes, secs = divmod(self.remaining_time, 60)
            timer = f"{minutes:02d}:{secs:02d}"
            self.timer_label.config(text=timer)
            self.master.update()
            time.sleep(1)
            self.remaining_time -= 1

        if self.remaining_time < 0:
            self.timer_label.config(text="00:00")
            self.play_sound()

            messagebox.showinfo("Pomodoro", "Tempo esgotado!")

    def play_sound(self):
        playsound("alarm.wav")  # Substitua "alarm.wav" pelo caminho para o seu arquivo de som

root = tk.Tk()
app = PomodoroTimer(root)
root.mainloop()