import argparse
import janela

VERSION = "2.0.0"
repo= "Compactador"

parser = argparse.ArgumentParser(prog="compactararquivos")
parser.add_argument("-v","--version",action="version", version=f"%(prog)s {VERSION}")
args = parser.parse_args()

janela.iniciar_janela(VERSION, repo)