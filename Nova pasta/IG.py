import tkinter as tk
from tkinter import ttk, messagebox
import multiprocessing
from calculo import processa  # Importa do outro arquivo

def calcular():
    entrada = entry.get().strip()
    if not entrada.isdigit():
        messagebox.showerror("Erro", "Digite um número inteiro positivo.")
        return
    valor = int(entrada)
    button.config(state=tk.DISABLED)
    text.delete(1.0, tk.END)
    text.insert(tk.END, "Calculando...\n")
    root.update()

    global parent_conn, proc
    parent_conn, child_conn = multiprocessing.Pipe()
    proc = multiprocessing.Process(target=processa, args=(valor, child_conn))
    proc.start()
    text.delete(1.0, tk.END)
    root.after(50, atualizar_texto)

def atualizar_texto():
    global parent_conn, proc
    try:
        while parent_conn.poll():
            resultado = parent_conn.recv()
            if "parcial" in resultado:
                text.insert(tk.END, resultado["parcial"])
                text.see(tk.END)
            elif "fim" in resultado:
                resumo = resultado["relatorio"].split("\n\n")[-1]
                text.insert(tk.END, "\n" + resumo)
                with open("relatorio.txt", "w", encoding="utf-8") as f:
                    f.write(resultado["relatorio"])
                button.config(state=tk.NORMAL)
                proc.join()
                return
    except EOFError:
        pass
    root.after(50, atualizar_texto)

if __name__ == "__main__":
    multiprocessing.freeze_support()
    root = tk.Tk()
    root.title("Sequências Numéricas")
    root.geometry("500x400")

    label = ttk.Label(root, text="Digite um número inteiro:")
    label.pack(pady=10)

    entry = ttk.Entry(root)
    entry.pack(pady=5)
    entry.bind("<Return>", lambda e: calcular())

    button = ttk.Button(root, text="Calcular", command=calcular)
    button.pack(pady=10)

    text = tk.Text(root, height=15, width=60)
    text.pack(pady=10)

    parent_conn = None
    proc = None

    root.mainloop()