import re
import time
import pygame
from rich.panel import Panel
from rich.live import Live
from rich.console import Console

console = Console()


def progresso_com_lrc(caminho_lrc: str, isArquivo: bool = True):
    """
    Exibe texto sincronizado com base em um arquivo .lrc (letra com tempos).
    Usa pygame para tocar a música e rich para exibir as falas no terminal.

    Parâmetros:
        caminho_lrc (str): Caminho para o arquivo .lrc ou texto bruto.
        isArquivo (bool): Se True, lê o arquivo; caso contrário, trata como string.
    """
    # 🔹 Lê o conteúdo do arquivo .lrc
    if isArquivo:
        with open(caminho_lrc, "r", encoding="utf-8") as f:
            conteudo = f.readlines()
    else:
        conteudo = caminho_lrc.splitlines()

    # 🔹 Extrai tempos e versos com regex
    padrao = re.compile(r"\[(\d+):(\d+\.\d+)\]\s*(.*)")
    linhas = []

    for linha in conteudo:
        m = padrao.match(linha)
        if m:
            minutos, segundos, texto = m.groups()
            tempo_total = float(minutos) * 60 + float(segundos)
            linhas.append((tempo_total, texto.strip()))

    if not linhas:
        console.print("[red]Nenhuma linha válida encontrada no arquivo LRC.[/red]")
        return

    # 🔹 Solicita o caminho da música
    caminho_musica = input("🎵 Caminho do arquivo MP3: ").strip()

    # 🔹 Inicializa pygame e toca o áudio
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(caminho_musica)
        pygame.mixer.music.play()
    except Exception as e:
        console.print(f"[red]Erro ao carregar música:[/red] {e}")
        return

    # 🔹 Exibe a letra sincronizada
    inicio = time.time()
    with Live(refresh_per_second=10) as live:
        for tempo, verso in linhas:
            while time.time() - inicio < tempo:
                time.sleep(0.01)
            painel = Panel(
                verso,
                title="[bold magenta]Letra Sincronizada[/bold magenta]",
                border_style="cyan",
                subtitle=f"[italic]{tempo:.2f}s[/italic]",
                expand=False,
            )
            live.update(painel)

    pygame.mixer.music.stop()
    console.print("\n[bold green]✔ Exibição concluída![/bold green]")
