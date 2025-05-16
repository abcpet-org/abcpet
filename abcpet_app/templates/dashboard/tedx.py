from youtube_transcript_api import YouTubeTranscriptApi

def obtener_transcripcion(video_id):
    try:
        transcripcion = YouTubeTranscriptApi.get_transcript(video_id)
        texto = ''
        for linea in transcripcion:
            texto += linea['text'] + ' '
        return texto
    except Exception as e:
        print("Error al obtener la transcripción:", e)
        return None

if __name__ == "__main__":
    video_id = 'TU_VIDEO_ID_AQUI'  # Reemplaza esto con el ID de tu video
    texto_transcripcion = obtener_transcripcion(video_id)
    if texto_transcripcion:
        print("Transcripción del video:")
        print(texto_transcripcion)