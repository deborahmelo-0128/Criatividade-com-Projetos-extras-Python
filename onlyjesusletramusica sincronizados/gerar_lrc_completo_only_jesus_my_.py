# -*- coding: utf-8 -*-
import sys
import os
import time
import pygame
from colorama import Fore, Style, init
import re

# --- CONFIGURAÇÕES ---
ARQUIVO_MUSICA = r"C:\Users\wagner\Desktop\letrasincronizadamp3\only-jesus-my-savior-354984.mp3"
ARQUIVO_LRC = r"C:\Users\wagner\Desktop\letrasincronizadamp3\onlyjesus_completo.lrc"

# Habilita cores ANSI no Windows CMD
os.system("")

# Força saída UTF-8 no terminal
sys.stdout.reconfigure(encoding='utf-8')
init(autoreset=True)


# --- Função: carregar letras com timestamps ---
def carregar_lrc(caminho):
    padrao = re.compile(r"\[(\d+):(\d+\.\d+)\](.*)")
    linhas = []
    with open(caminho, "r", encoding="utf-8") as f:
        for linha in f:
            linha = linha.strip()
            match = padrao.match(linha)
            if match:
                minutos, segundos, texto = match.groups()
                tempo = int(minutos) * 60 + float(segundos)
                linhas.append((tempo, texto.strip()))
    linhas.sort(key=lambda x: x[0])
    return linhas


# --- Função: mostrar texto com efeito de digitação ---
def digitar_texto(texto, cor=Fore.CYAN, atraso=0.05):
    for letra in texto:
        sys.stdout.write(cor + letra + Style.RESET_ALL)
        sys.stdout.flush()
        time.sleep(atraso)
    print()


# --- Função: tocar música e mostrar letra sincronizada ---
def tocar_com_letra(arquivo_musica, arquivo_lrc):
    linhas = carregar_lrc(arquivo_lrc)
    if not linhas:
        print(Fore.RED + "❌ Nenhuma linha válida encontrada no arquivo LRC.")
        return

    pygame.mixer.init()
    pygame.mixer.music.load(arquivo_musica)
    pygame.mixer.music.play()

    inicio = time.time()
    i = 0
    print(Fore.YELLOW + "\n🎧 Iniciando reprodução...\n")

    while i < len(linhas) and pygame.mixer.music.get_busy():
        tempo_atual = time.time() - inicio
        if tempo_atual >= linhas[i][0]:
            digitar_texto(linhas[i][1])
            i += 1
        time.sleep(0.05)

    pygame.mixer.music.stop()
    print(Fore.GREEN + "\n🎵 Fim da música!")


# --- EXECUÇÃO ---
if __name__ == "__main__":
    tocar_com_letra(ARQUIVO_MUSICA, ARQUIVO_LRC)
