# visu_sens.py
import tkinter as tk
from tkinter import ttk
import threading
import time
import win32file

PIPE_NAME = r'\\.\pipe\crazyflie_sensores'

def ler_pipe():
    """Cliente: conecta ao pipe criado pelo controlador e lê dados."""
    while True:
        try:
            handle = win32file.CreateFile(
                PIPE_NAME,
                win32file.GENERIC_READ,
                0, None,
                win32file.OPEN_EXISTING,
                0, None
            )
            print("Conectado ao pipe, aguardando dados...")

            while True:
                hr, data = win32file.ReadFile(handle, 64*1024)
                atualizar_texto(data.decode().strip())
        except Exception as e:
            atualizar_texto(f"Esperando controlador... ({e})")
            time.sleep(1)

def atualizar_texto(texto):
    text_widget.config(state=tk.NORMAL)
    text_widget.insert(tk.END, texto + "\n")
    text_widget.see(tk.END)
    text_widget.config(state=tk.DISABLED)

def iniciar_leitura():
    thread = threading.Thread(target=ler_pipe, daemon=True)
    thread.start()

# -------------------
# Interface gráfica
# -------------------
root = tk.Tk()
root.title("Visualização de Sensores - Crazyflie")
root.geometry("500x350")

label = ttk.Label(root, text="Leitura dos Sensores do Drone (Named Pipe):")
label.pack(pady=10)

text_widget = tk.Text(root, height=15, width=60, state=tk.DISABLED)
text_widget.pack(pady=10)

iniciar_leitura()
root.mainloop()