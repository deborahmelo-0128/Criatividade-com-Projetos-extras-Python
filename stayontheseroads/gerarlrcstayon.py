import whisper

ARQUIVO_MUSICA = r"C:\Users\wagner\Desktop\stayontheseroads\09 - A-HA - Stay On These Roads.mp3"
ARQUIVO_SAIDA = r"C:\Users\wagner\Desktop\stayontheseroads\stay_on.lrc"

print("🎧 Gerando legenda sincronizada com Whisper...")
modelo = whisper.load_model("base")  # ou "small", "medium"
resultado = modelo.transcribe(ARQUIVO_MUSICA)

with open(ARQUIVO_SAIDA, "w", encoding="utf-8") as f:
    for seg in resultado["segments"]:
        inicio = seg["start"]
        minutos = int(inicio // 60)
        segundos = int(inicio % 60)
        centesimos = int((inicio - int(inicio)) * 100)
        texto = seg["text"].strip()
        if texto:
            f.write(f"[{minutos:02d}:{segundos:02d}.{centesimos:02d}] {texto}\n")

print(f"✅ LRC salvo em {ARQUIVO_SAIDA}")
