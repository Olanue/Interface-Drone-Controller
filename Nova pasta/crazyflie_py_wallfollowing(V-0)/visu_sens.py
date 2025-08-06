import tkinter as tk
from tkinter import ttk
import threading
import os

PIPE_NAME = r'\\.\pipe\crazyflie_sensores'

def ler_pipe():
    """Lê continuamente do named pipe e atualiza a interface."""
    while True:
        try:
            with open(PIPE_NAME, 'r') as pipe:
                while True:
                    linha = pipe.readline()
                    if not linha:
                        break
                    atualizar_texto(linha.strip())
        except Exception as e:
            atualizar_texto(f"Esperando dados do drone... ({e})")
            # Espera antes de tentar novamente
            import time
            time.sleep(1)

def atualizar_texto(texto):
    text_widget.config(state=tk.NORMAL)
    text_widget.insert(tk.END, texto + "\n")
    text_widget.see(tk.END)
    text_widget.config(state=tk.DISABLED)

def iniciar_leitura():
    thread = threading.Thread(target=ler_pipe, daemon=True)
    thread.start()

root = tk.Tk()
root.title("Visualização de Sensores - Crazyflie")
root.geometry("400x300")

label = ttk.Label(root, text="Leitura dos Sensores do Drone (Named Pipe):")
label.pack(pady=10)

text_widget = tk.Text(root, height=12, width=45, state=tk.DISABLED)
text_widget.pack(pady=10)

iniciar_leitura()
root.mainloop()