import pygame
import time
import re
import os
import sys
import sys

# === CONFIGURAÇÕES ===
ARQUIVO_MUSICA = r"C:\Users\wagner\Desktop\karaoke\Ellie_Goulding_B_-_Love_Me_Like_You_Do_DJ_Noiz_Remix_(mp3.pm).mp3"
ARQUIVO_LRC = r"C:\Users\wagner\Desktop\karaoke\love_like.lrc"
VELOCIDADE_DIGITACAO = 0.04  # segundos entre cada letra

# === FUNÇÕES ===

def tocar_musica(arquivo):
    """Inicia reprodução da música."""
    pygame.mixer.init()
    pygame.mixer.music.load(arquivo)
    pygame.mixer.music.play()
    print("\n🎧 Música iniciada...\n")

def ler_lrc(caminho):
    """Lê e interpreta o arquivo .lrc, retornando lista [(tempo, texto)]."""
    linhas_sincronizadas = []
    padrao_tempo = re.compile(r"\[(\d+):(\d+).(\d+)\](.*)")
    with open(caminho, "r", encoding="utf-8") as f:
        for linha in f:
            linha = linha.strip()
            if not linha:
                continue
            m = padrao_tempo.match(linha)
            if m:
                minutos, segundos, milesimos, texto = m.groups()
                tempo_total = int(minutos) * 60 + int(segundos) + int(milesimos) / 100
                linhas_sincronizadas.append((tempo_total, texto.strip()))
    return linhas_sincronizadas

def efeito_digitacao(texto):
    """Mostra o texto com efeito de digitação."""
    for caractere in texto:
        print(caractere, end='', flush=True)
        time.sleep(VELOCIDADE_DIGITACAO)
    print()  # quebra de linha no final

def exibir_karaoke(letra):
    """Mostra a letra com sincronização e efeito de digitação."""
    inicio = time.time()
    for tempo, linha in letra:
        # Espera até o momento certo da letra
        while time.time() - inicio < tempo:
            time.sleep(0.01)
        # Mostra a linha atual
        print("\n\033[1;33m", end='')  # texto amarelo
        efeito_digitacao(linha)
        print("\033[0m", end='')  # reset cor
    print("\n🎤 Fim da música! 🎶")

# === EXECUÇÃO PRINCIPAL ===
if __name__ == "__main__":
    if not os.path.exists(ARQUIVO_MUSICA):
        print("❌ Arquivo de música não encontrado.")
        sys.exit()
    if not os.path.exists(ARQUIVO_LRC):
        print("❌ Arquivo LRC não encontrado.")
        sys.exit()

    print("🎶 Iniciando karaokê com efeito de digitação...\n")
    letra = ler_lrc(ARQUIVO_LRC)
    tocar_musica(ARQUIVO_MUSICA)
    exibir_karaoke(letra)
