import tkinter as tk
from tkinter import ttk
import metodos
import verificarversao

root = tk.Tk()

def iniciar_janela(version, repo):
    # Variaveis
    largura_entradas = 50

    root.title(f"Compactador {version}")
    root.resizable(False, False)

    label_origem = ttk.Label(root, text="Origem:")
    label_origem.grid(row=0, column=0, padx=(10, 0), pady=(5, 8), sticky="w")

    entrada_origem = ttk.Entry(root, width=largura_entradas)
    entrada_origem.grid(row=0, column=1, padx=(10, 0), pady=(5, 8),sticky="w")

    button_origem = ttk.Button(root, text="...", command=lambda: (entrada_origem.delete(0, "end"),
                                                                  entrada_origem.insert(0, metodos.selecionar_pasta())))
    button_origem.grid(row=0, column=2, padx=(10, 5), pady=(5, 8),sticky="w")

    label_destino = ttk.Label(root, text="Destino:")
    label_destino.grid(row=1, column=0, padx=(10, 0), pady=(5, 8), sticky="w")

    entrada_destino = ttk.Entry(root, width=largura_entradas)
    entrada_destino.grid(row=1, column=1, padx=(10, 0), pady=(5, 8), sticky="w")

    button_destino = ttk.Button(root, text="...", command=lambda: (entrada_destino.delete(0, "end"),
                                                                   entrada_destino.insert(0, metodos.selecionar_pasta())))
    button_destino.grid(row=1, column=2, padx=(10, 5), pady=(5, 8), sticky="w")

    button_compactar = ttk.Button(root, text="Compactar", command=lambda:  metodos.iniciar_compactacao(entrada_origem.get(),
                                                                                                       entrada_destino.get(),
                                                                                                       progress_canvas))
    button_compactar.grid(row=3, column=0, columnspan=3, padx=(10, 5), pady=(5, 8), sticky="we")

    progress_canvas = tk.Canvas(root, height=25, bg="white", highlightthickness=1, highlightbackground="black")
    progress_canvas.grid(row=4, column=0, columnspan=3, padx=(10, 5), pady=(5, 8), sticky="we")

    # verificar versão
    button_update = ttk.Button(root, text="Verificar atualização",
                               command=lambda: verificarversao.consultar_lancamento(repo, version))
    button_update.grid(row=5, column=0, columnspan=3, padx=(10, 5), pady=(5, 8), sticky="we")

    root.mainloop()