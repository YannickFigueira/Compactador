import tkinter as tk
from tkinter import ttk

# Variáveis de estilo locais do layout
LARGURA_ENTRADAS = 50
ESPACO = 5


class Compactador:
    def __init__(self, janela_principal, repo, version):
        self.janela_principal = janela_principal
        self.janela_principal.title(f"Compactador {version}")
        self.janela_principal.resizable(False, False)

        self.nome_janela = "compactador"  # Identificador para o seu controlador
        self.controles = {}

        self._criar_layout(repo, version)
        self._criar_barra_menu()

    def _criar_layout(self, repo, version):
        # --- Variáveis ---
        self.controles['var_repo'] = tk.StringVar(value=repo)
        self.controles['var_version'] = tk.StringVar(value=version)

        # --- Controles ---
        self.label_origem = ttk.Label(self.janela_principal, text="Origem:")
        self.label_origem.grid(row=0, column=0, padx=ESPACO, pady=ESPACO)

        self.entrada_origem = ttk.Entry(self.janela_principal, width=LARGURA_ENTRADAS)
        self.entrada_origem.grid(row=0, column=1, padx=ESPACO, pady=ESPACO)
        self.controles['entrada_origem'] = self.entrada_origem

        self.button_origem = ttk.Button(self.janela_principal, text="...")
        self.button_origem.grid(row=0, column=2, padx=ESPACO, pady=ESPACO)
        self.controles['button_origem'] = self.button_origem

        self.label_destino = ttk.Label(self.janela_principal, text="Destino:")
        self.label_destino.grid(row=1, column=0, padx=ESPACO, pady=ESPACO)

        self.entrada_destino = ttk.Entry(self.janela_principal, width=LARGURA_ENTRADAS)
        self.entrada_destino.grid(row=1, column=1, padx=ESPACO, pady=ESPACO)
        self.controles['entrada_destino'] = self.entrada_destino

        self.button_destino = ttk.Button(self.janela_principal, text="...")
        self.button_destino.grid(row=1, column=2, padx=ESPACO, pady=ESPACO)
        self.controles['button_destino'] = self.button_destino

        self.button_compactar = ttk.Button(self.janela_principal, text="Compactar")
        self.button_compactar.grid(row=3, column=0, columnspan=3, padx=ESPACO, pady=ESPACO, sticky="ew")
        self.controles['button_compactar'] = self.button_compactar

        self.progress_canvas = tk.Canvas(self.janela_principal, height=25, bg="white", highlightthickness=1, highlightbackground="black")
        self.progress_canvas.grid(row=4, column=0, columnspan=3, padx=ESPACO, pady=ESPACO, sticky="ew")
        self.controles['progress_canvas'] = self.progress_canvas

    def _criar_barra_menu(self):
        # Cria a barra principal
        barra_menu = tk.Menu(self.janela_principal)
        self.janela_principal.config(menu=barra_menu)

        # Menu Ajuda
        menu_ajuda = tk.Menu(barra_menu, tearoff=0)
        barra_menu.add_cascade(label="Ajuda", menu=menu_ajuda)

        # Salvamos a referência do menu "Sobre" para o controlador colocar a ação nele depois
        self.controles['var_title'] = tk.StringVar(value="Compactador")
        self.controles['menu_ajuda'] = menu_ajuda
