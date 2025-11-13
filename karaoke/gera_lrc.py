import whisper

ARQUIVO = r"C:\Users\wagner\Desktop\karaoke\09 - A-HA - Stay On These Roads.mp3"

modelo = whisper.load_model("base")
resultado = modelo.transcribe(ARQUIVO, task="transcribe")

with open("stay_on_these_roads.lrc", "w", encoding="utf-8") as f:
    for segmento in resultado["segments"]:
        tempo = segmento["start"]
        minutos = int(tempo // 60)
        segundos = int(tempo % 60)
        milesimos = int((tempo - int(tempo)) * 100)
        f.write(f"[{minutos:02d}:{segundos:02d}.{milesimos:02d}]{segmento['text'].strip()}\n")

print("✅ Arquivo stay_on_these_roads.lrc gerado com sucesso!")

