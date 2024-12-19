import whisper

model = whisper.load_model("turbo")

result = model.transcribe("audio.mp3")

transcription_text = result["text"]

with open("transcription.txt", "w") as file:
    file.write(transcription_text)

print("La transcripción se ha guardado en 'transcription.txt'")
