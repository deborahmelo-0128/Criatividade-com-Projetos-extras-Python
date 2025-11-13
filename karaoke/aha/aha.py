import pygame
import time
import os
from colorama import Fore, Style, init

# Inicializa colorama (para colorir texto no Windows)
init(autoreset=True)

# Caminho do arquivo MP3
ARQUIVO_MUSICA = r"C:\Users\wagner\Desktop\karaoke\aha\09 - A-HA - Stay On These Roads.mp3"

# Velocidade média de digitação (ajuste se quiser mais lento ou rápido)
DIGIT_SPEED = 0.05

# Estrutura sincronizada (tempo em segundos, texto)
# ⏱️ Use os tempos como referência — apenas substitua os textos pelos versos reais.
# A música tem 4:46 = 286 segundos totais.
letra_sincronizada = [
    # --- INTRO ---
    (0.0,  "[Instrumental Intro...]"),
    (15.0, "[Verso 1 - início]"),
    (25.0, "[verso continua]"),
    (35.0, "[mais versos...]"),
    (45.0, "[transição para refrão]"),

    # --- REFRÃO 1 ---
    (55.0, "[Stay on these roads...]"),
    (65.0, "[We shall meet, I know...]"),
    (75.0, "[Stay on...]"),
    (85.0, "[These roads...]"),

    # --- INTERLÚDIO ---
    (95.0, "[Instrumental interlude]"),
    (110.0, "[Verso 2 - início]"),
    (120.0, "[verso continua]"),
    (130.0, "[verso finaliza]"),

    # --- REFRÃO 2 ---
    (140.0, "[Stay on these roads...]"),
    (150.0, "[We shall meet, I know...]"),
    (160.0, "[Stay on these roads...]"),
    (170.0, "[Take care...]"),
    (180.0, "[Take care...]"),

    # --- PONTE ---
    (195.0, "[Bridge instrumental / vocal]"),
    (210.0, "[Final section]"),
    (225.0, "[Refrão final - Stay on these roads...]"),
    (240.0, "[We shall meet, I know...]"),
    (255.0, "[Outro instrumental]"),
    (270.0, "[Fade out...]"),
    (285.0, "[Fim da música 🎶]")
]

def digitar_texto(texto, atraso=DIGIT_SPEED, cor=Fore.CYAN):
    """Imprime texto com efeito de digitação."""
    print(cor, end="")
    for char in texto:
        print(char, end="", flush=True)
        time.sleep(atraso)
    print(Style.RESET_ALL)

def tocar_musica(arquivo):
    """Reproduz o arquivo de música."""
    pygame.mixer.init()
    pygame.mixer.music.load(arquivo)
    pygame.mixer.music.play()
    print(Fore.GREEN + f"\n▶️ Tocando: {os.path.basename(arquivo)}\n" + Style.RESET_ALL)

def exibir_letra(letras):
    """Exibe a letra sincronizada com base no tempo."""
    inicio = time.time()
    for tempo, texto in letras:
        # Espera até o momento certo
        while time.time() - inicio < tempo:
            time.sleep(0.01)
        digitar_texto(texto)

    print(Fore.MAGENTA + "\n🎵 Fim da música 🎵" + Style.RESET_ALL)

if __name__ == "__main__":
    if not os.path.exists(ARQUIVO_MUSICA):
        print(Fore.RED + f"⚠️ Arquivo não encontrado: {ARQUIVO_MUSICA}" + Style.RESET_ALL)
        exit()

    os.system('cls' if os.name == 'nt' else 'clear')
    print(Fore.MAGENTA + "🎤 A-HA — Stay On These Roads 🎶")
    print(Fore.YELLOW + "Versão sincronizada com 4min46s — digitação automática iniciando junto com o áudio.\n")

    tocar_musica(ARQUIVO_MUSICA)
    exibir_letra(letra_sincronizada)
