import os
import sys
import time
import argparse
from datetime import datetime

from story_generator import get_random_story, VIRAL_STORIES
from voice_engine import generate_voice
from subtitle_engine import generate_ass_subtitles
from video_engine import render_viral_video

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
ASSETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
TEMP_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "temp")

ROBLOX_VIDEO = os.path.join(ASSETS_DIR, "roblox_bg.mp4")

# Viral hashtags optimized for US & European algorithmic distribution
DEFAULT_HASHTAGS = "#fyp #foryou #viral #storytime #redditstories #mystery #roblox #satisfying #creepypasta #trending"

def create_viral_video(story: dict = None, voice: str = "en-US-ChristopherNeural") -> dict:
    """
    Creates a full 60s+ viral TikTok video in English:
    1. Selects an engaging viral story.
    2. Generates ultra-realistic American neural voiceover.
    3. Builds eye-tracking, high-contrast dynamic captions.
    4. Renders 1080x1920 vertical video with Roblox parkour background.
    """
    if story is None:
        story = get_random_story()

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(TEMP_DIR, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    story_id = story.get("id", "viral_story")
    
    audio_path = os.path.join(TEMP_DIR, f"{story_id}_{timestamp}.mp3")
    subs_path = os.path.join(TEMP_DIR, f"{story_id}_{timestamp}.ass")
    final_video_path = os.path.join(OUTPUT_DIR, f"{story_id}_{timestamp}.mp4")

    print("\n" + "=" * 65)
    print(f"🚀 [CRIADOR DE VÍDEO VIRAL] INICIANDO PRODUÇÃO")
    print(f"   Título: {story['title']}")
    print(f"   Hook: \"{story['hook']}\"")
    print(f"   Voz: {voice} (Padrão TikTok US)")
    print("=" * 65)

    # 1. Generate Voice and Subtitle Cues
    print("🎙️ 1. Gerando narração neural americana com Edge-TTS...")
    duration, subtitle_cues = generate_voice(story["text"], audio_path, voice=voice)
    print(f"   -> Áudio gerado com sucesso: {duration:.1f} segundos ({len(subtitle_cues)} blocos de fala)")

    # 2. Generate Stylized ASS Subtitles
    print("📝 2. Criando legendas dinâmicas coloridas (formato TikTok)...")
    generate_ass_subtitles(subtitle_cues, subs_path)
    print(f"   -> Legendas compiladas em: {subs_path}")

    # 3. Render Final Video
    print("🎬 3. Montando vídeo com gameplay vertical de Roblox (1080x1920)...")
    render_viral_video(
        background_video_path=ROBLOX_VIDEO,
        voiceover_audio_path=audio_path,
        subtitle_ass_path=subs_path,
        output_video_path=final_video_path
    )

    caption = f"{story['hook']}\n\nWhat would you do? Comment below! 👇\n\n{DEFAULT_HASHTAGS}"
    
    meta_path = os.path.join(OUTPUT_DIR, f"{story_id}_{timestamp}_caption.txt")
    with open(meta_path, "w", encoding="utf-8") as f:
        f.write(caption)

    print("\n" + "=" * 65)
    print("🎉 [SUCESSO] VÍDEO VIRAL PRONTO PARA O TIKTOK!")
    print(f"   Arquivo Final: {final_video_path}")
    print(f"   Duração: {duration:.1f}s (> 60s qualificado para monetizar em dólar)")
    print(f"   Legenda / Hashtags salvas em: {meta_path}")
    print("=" * 65 + "\n")

    return {
        "video_path": final_video_path,
        "audio_path": audio_path,
        "duration": duration,
        "caption": caption
    }

def main():
    parser = argparse.ArgumentParser(description="Automação TikTok US/Europa: Gerador de Vídeos e Lives 24/7")
    parser.add_argument("--generate", action="store_true", help="Gera 1 vídeo viral completo em inglês")
    parser.add_argument("--count", type=int, default=1, help="Quantidade de vídeos a gerar em lote")
    parser.add_argument("--live", action="store_true", help="Inicia a live 24/7 de Roblox para o TikTok")

    args = parser.parse_args()

    if args.live:
        from live_streamer import stream_to_tiktok_live
        stream_to_tiktok_live(video_path=ROBLOX_VIDEO)
    else:
        # Padrão: gerar vídeos
        count = max(1, args.count)
        print(f"Iniciando geração de {count} vídeo(s) viral(is)...")
        for i in range(count):
            story = VIRAL_STORIES[i % len(VIRAL_STORIES)]
            create_viral_video(story=story)
            if i < count - 1:
                time.sleep(2)

if __name__ == "__main__":
    main()
