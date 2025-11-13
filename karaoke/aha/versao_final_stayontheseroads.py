import pygame
import time
import os
import sys
from colorama import Fore, Style, init

# Inicializa o colorama (para cores funcionarem no Windows)
init(autoreset=True)

# Caminho do arquivo de áudio
ARQUIVO_MUSICA = r"C:\Users\wagner\Desktop\karaoke\aha\09 - A-HA - Stay On These Roads.mp3"

# Ajuste global inicial (em segundos)
AJUSTE_TEMPO = + 21.5  # Aumente se a letra estiver adiantada, diminua se atrasada

# Letra sincronizada (tempo, texto, velocidade da digitação)
letra_sincronizada = [
    (0.0,  "The cold has a voice", 0.06),
    (5.0,  "It talks to me", 0.07),
    (9.0,  "Stillborn, by choice", 0.065),
    (13.0, "And it airs no need", 0.07),
    (17.0, "To hold...", 0.08),
    (21.0, "Hold me tight, don’t let go", 0.06),
    (27.0, "If you stay, stay", 0.07),
    (32.0, "Don’t ever go away", 0.06),
    (37.0, "Stay on these roads", 0.08),
    (42.0, "We shall meet, I know", 0.07),
    (47.0, "Stay on... these roads", 0.07),
    (52.0, "Oh, these roads...", 0.06),
    (57.0, "Take care", 0.065),
    (61.0, "Take care", 0.065),
    (65.0, "Take care", 0.065)
]

def digitar_texto(texto, atraso_caractere=0.05, cor=Fore.CYAN):
    """Imprime texto com efeito de digitação colorido."""
    print(cor, end="")
    for char in texto:
        print(char, end="", flush=True)
        time.sleep(atraso_caractere)
    print(Style.RESET_ALL)

def animacao_introducao():
    """Mostra uma introdução estilizada antes da música começar."""
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Fore.MAGENTA + "\n\n🎬 Projeto Python Karaoke apresenta...\n")
    time.sleep(2)

    titulo = "🎤 A-HA — Stay on These Roads 🎶"
    for i in range(1, len(titulo) + 1):
        print(Fore.CYAN + titulo[:i], end="\r", flush=True)
        time.sleep(0.08)

    print("\n")
    time.sleep(1.5)

    subtitulo = "Let the music and code flow together..."
    digitar_texto(subtitulo, 0.05, Fore.BLUE)
    time.sleep(2)
    os.system('cls' if os.name == 'nt' else 'clear')

def tocar_musica(arquivo):
    """Inicia o áudio."""
    pygame.mixer.init()
    pygame.mixer.music.load(arquivo)
    pygame.mixer.music.play()
    print(Fore.CYAN + f"\n🎶 Tocando: {os.path.basename(arquivo)}\n" + Style.RESET_ALL)

def exibir_letra(letras, ajuste):
    """Mostra a letra no tempo certo, com cores e digitação suave."""
    inicio = time.time()
    for tempo, texto, atraso_caractere in letras:
        tempo_ajustado = tempo + ajuste
        if tempo_ajustado < 0:
            tempo_ajustado = 0
        while time.time() - inicio < tempo_ajustado:
            time.sleep(0.01)
        digitar_texto(texto, atraso_caractere, Fore.CYAN)
    print(Fore.MAGENTA + "\n🎵 Fim do refrão 🎵" + Style.RESET_ALL)

if __name__ == "__main__":
    if not os.path.exists(ARQUIVO_MUSICA):
        print(Fore.RED + f"⚠️ Arquivo não encontrado: {ARQUIVO_MUSICA}" + Style.RESET_ALL)
        sys.exit(1)

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(Fore.YELLOW + f"🎚️ Ajuste de tempo atual: {AJUSTE_TEMPO:+.2f} segundos" + Style.RESET_ALL)
        print(Fore.CYAN + "Digite um novo valor (ou pressione Enter para manter):" + Style.RESET_ALL)
        novo = input("> ").strip()
        if novo:
            try:
                AJUSTE_TEMPO = float(novo)
            except ValueError:
                print(Fore.RED + "Valor inválido. Use números (ex: 1.5 ou -0.8)" + Style.RESET_ALL)
                time.sleep(2)
                continue

        animacao_introducao()
        tocar_musica(ARQUIVO_MUSICA)
        exibir_letra(letra_sincronizada, AJUSTE_TEMPO)

        while pygame.mixer.music.get_busy():
            time.sleep(0.1)

        print(Fore.GREEN + "\n✅ Música finalizada!" + Style.RESET_ALL)
        print(Fore.CYAN + "Deseja testar outro ajuste? (s/n)" + Style.RESET_ALL)
        resposta = input("> ").strip().lower()
        if resposta != "s":
            break
    print(Fore.MAGENTA + "\nObrigado por usar o Karaoke Python! 🎤🎶\n" + Style.RESET_ALL)