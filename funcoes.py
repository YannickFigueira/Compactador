import os
import threading
import webbrowser
import zipfile
from pathlib import Path
from platform import system
from tkinter import messagebox, filedialog
import logging

import estilo
import verificarversao

home_dir = os.path.expanduser('~')
if system == 'Linux':

    if not os.path.exists(f"{home_dir}/log"):
        os.mkdir(f"{home_dir}/log")

    logging.basicConfig(
        filename=f"{home_dir}/log/{estilo.ARQUIVO_ERRO}",        # nome do arquivo
        level=logging.ERROR,         # nível de log
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
elif system == 'Windows':

    if not os.path.exists(f"c:/temp"):
        os.mkdir(f"c:/temp")

    logging.basicConfig(
        filename=f"c:/temp/{estilo.ARQUIVO_ERRO}",  # nome do arquivo
        level=logging.ERROR,  # nível de log
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

# --- Comandos gerais ---
def selecionar_pasta():
    pasta = filedialog.askdirectory(title="Selecione uma pasta")
    if pasta:  # se o usuário não cancelar
        return pasta
    else:
        return ""

class Controles:
    def __init__(self, view):
        self.view = view

        # O controlador se adapta automaticamente baseando-se em qual janela o chamou
        if hasattr(view, 'nome_janela'):
            if view.nome_janela == "compactador":
                self._vincular_compactador()

    def _vincular_compactador(self):
        self.view.controles['button_origem'].config(command=lambda: self.selecionar_origem())
        self.view.controles['button_destino'].config(command=lambda: self.selecionar_destino())
        self.view.controles['button_compactar'].config(command=lambda: self.iniciar_compactacao(
            self.view.controles['entrada_origem'].get().strip(), self.view.controles['entrada_destino'].get().strip()))

        # Vincula a ação ao menu "Sobre" que foi criado no layout
        self.view.controles['menu_ajuda'].add_command(label="Verificar atualização",
                                                      command=lambda: verificarversao.consultar_lancamento(estilo.REPO, estilo.VERSION))
        self.view.controles['menu_ajuda'].add_command(label="Sobre", command=lambda: self.visitar_site())

    def selecionar_origem(self):
        self.view.controles['entrada_origem'].delete(0, 'end')
        self.view.controles['entrada_origem'].insert(0, selecionar_pasta())

    def selecionar_destino(self):
        self.view.controles['entrada_destino'].delete(0, 'end')
        self.view.controles['entrada_destino'].insert(0, selecionar_pasta())

    # --- Comandos com controles ---
    # --- Funcionalidades ---

    # --- Inicia a compactação --- #
    def iniciar_compactacao(self, origem,
                            destino_zip):
        t = threading.Thread(
            target=self.compactar,
            args=(origem,
                  destino_zip),
            daemon=True
        )
        t.start()

    def compactar(self, origem, destino_zip):
        if not origem == "":
            pasta_origem = Path(origem)
            if pasta_origem.is_dir() or pasta_origem.is_file():
                # pasta_destino = Path(destino_zip)
                if not destino_zip == "":
                    pasta_matriz = str(origem).split("/")
                    destino_zip = f"{destino_zip}/{pasta_matriz[len(pasta_matriz) - 1]}.zip"
                    # Cria o arquivo ZIP no destino

                    with zipfile.ZipFile(destino_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
                        # Percorre todos os arquivos da pasta de origem
                        contador = 0
                        # Conta todos os arquivos dentro da pasta origem
                        total = sum(len(arquivos) for _, _, arquivos in os.walk(origem))

                        for raiz, _, arquivos in os.walk(origem):
                            for arquivo in arquivos:

                                try:
                                    caminho_completo = Path(raiz) / arquivo
                                    caminho_relativo = caminho_completo.relative_to(origem)
                                    zipf.write(caminho_completo, caminho_relativo)

                                    self.atualizar_barra(contador, total)
                                    print(f"{contador} / {total}")
                                    contador += 1
                                except Exception as e:
                                    logging.error(f"Erro ao compactar {caminho_completo}: {e}")
                            # print(f"{contador} / {len(arquivos)}")

                        if not total == 0:
                            self.atualizar_barra(total, total)
                        else:
                            self.atualizar_barra(1, 1)
                        messagebox.showinfo("Completo", "Finalizado com exito.")
                        self.view.controles['entrada_destino'].focus_set()
                else:
                    messagebox.showinfo("Verificar", "Digite algo ou selecione uma pasta.")
                    self.view.controles['entrada_destino'].focus_set()
            else:
                messagebox.showinfo("Verificar", "Arquivo ou pasta inexistente")
                self.view.controles['entrada_origem'].focus_set()
        else:
            messagebox.showinfo("Verificar", "Digite algo ou selecione uma pasta")
            self.view.controles['entrada_origem'].focus_set()

    ### Atualiza a barra de progresso ###
    def atualizar_barra(self, valor, total):
        self.view.controles['progress_canvas'].delete("all")
        largura = int((valor / total) * self.view.controles['progress_canvas'].winfo_width())
        # desenha a barra preenchida
        self.view.controles['progress_canvas'].create_rectangle(0, 0, largura, 25, fill="green")
        # escreve a porcentagem dentro da barra
        porcentagem = (valor / total) * 100
        x = self.view.controles['progress_canvas'].winfo_width() // 2
        self.view.controles['progress_canvas'].create_text(x, 12, text=f"{porcentagem:.3f}%", fill="black", font=("Arial", 10, "bold"),
                                    anchor="center")

    # --- Menus ---

    def visitar_site(self):
        pagina = "https://github.com/YannickFigueira"
        resposta = messagebox.askyesno(
            "Sobre",
            f"{estilo.NOME_PROGRAMA} {estilo.VERSION}\n"
            f"Desenvolvedor YannickFigueira\n"
            f"chronostimeinchain@gmail.com\n\n"
            f"Deseja visitar a página?"
        )
        if resposta:
            webbrowser.open(pagina)
