import os
import sys
import time
import json
import argparse
from datetime import datetime, timedelta

from story_generator import VIRAL_STORIES
from voice_engine import generate_voice
from subtitle_engine import generate_ass_subtitles
from video_engine import render_viral_video

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
ASSETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
TEMP_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "temp")
ROBLOX_VIDEO = os.path.join(ASSETS_DIR, "roblox_bg.mp4")

DEFAULT_HASHTAGS = "#fyp #foryou #viral #storytime #redditstories #mystery #roblox #satisfying #creepypasta #trending #usa"

SLOT_HOURS = ["14:00", "17:00", "21:00"]

def produce_batch(start_day_offset: int = 1, total_days: int = 9, story_start_index: int = 3):
    """
    Produz em lote os vídeos para os próximos dias (3 por dia),
    gerando nomes organizados por Dia e Horário de agendamento:
    Ex: D02_14h_story_id.mp4
    """
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(TEMP_DIR, exist_ok=True)

    base_date = datetime.now()
    schedule_records = []

    print("\n" + "=" * 65)
    print("🏭 [BATCH PRODUCER] INICIANDO PRODUÇÃO EM MASSA DO LOTE 1")
    print(f"   Dias a cobrir: {total_days} dias (3 vídeos por dia)")
    print(f"   Total de vídeos: {total_days * 3}")
    print(f"   Horários por dia: {', '.join(SLOT_HOURS)} (Horário Nobre EUA)")
    print("=" * 65 + "\n")

    current_story_idx = story_start_index
    total_produced = 0

    for d in range(total_days):
        target_day = base_date + timedelta(days=(start_day_offset + d))
        date_str = target_day.strftime("%Y-%m-%d")
        day_num = start_day_offset + d + 1  # Ex: D02, D03...

        for slot_idx, slot_time in enumerate(SLOT_HOURS):
            hour_str = slot_time.split(":")[0] + "h"
            story = VIRAL_STORIES[current_story_idx % len(VIRAL_STORIES)]
            story_id = story.get("id", f"story_{current_story_idx}")

            prefix = f"D{day_num:02d}_{hour_str}_{story_id}"
            audio_path = os.path.join(TEMP_DIR, f"{prefix}.mp3")
            subs_path = os.path.join(TEMP_DIR, f"{prefix}.ass")
            video_path = os.path.join(OUTPUT_DIR, f"{prefix}.mp4")
            caption_path = os.path.join(OUTPUT_DIR, f"{prefix}_caption.txt")

            # Se o vídeo já foi renderizado anteriormente, pula
            if os.path.exists(video_path) and os.path.getsize(video_path) > 10 * 1024 * 1024:
                print(f"⏩ [Vídeo já existe] {prefix}.mp4 (pulando renderização)")
            else:
                print("\n" + "-" * 60)
                print(f"🎬 Renderizando [{total_produced + 1}/{total_days * 3}]: Dia {day_num:02d} ({date_str} às {slot_time})")
                print(f"   Título: {story['title']}")
                print(f"   Hook: \"{story['hook']}\"")
                print("-" * 60)

                # 1. Narração
                duration, cues = generate_voice(story["text"], audio_path, voice="en-US-ChristopherNeural")
                # 2. Legendas dinâmicas
                generate_ass_subtitles(cues, subs_path)
                # 3. Renderização FFmpeg
                render_viral_video(ROBLOX_VIDEO, audio_path, subs_path, video_path)

            caption = (
                f"{story['hook']}\n\n"
                f"What would you do? Comment below! 👇\n\n"
                f"{DEFAULT_HASHTAGS}"
            )
            with open(caption_path, "w", encoding="utf-8") as f:
                f.write(caption)

            schedule_records.append({
                "day_number": day_num,
                "scheduled_date": date_str,
                "scheduled_time": slot_time,
                "schedule_iso": f"{date_str}T{slot_time}:00",
                "video_path": video_path,
                "caption_path": caption_path,
                "title": story["title"],
                "hook": story["hook"],
                "caption": caption
            })

            current_story_idx += 1
            total_produced += 1

    # Salva o plano completo de agendamento em JSON
    plan_path = os.path.join(OUTPUT_DIR, "lote_1_schedule_plan.json")
    with open(plan_path, "w", encoding="utf-8") as f:
        json.dump(schedule_records, f, indent=2, ensure_ascii=False)

    print("\n" + "=" * 65)
    print("🎉 [LOTE 1 CONCLUÍDO COM SUCESSO]")
    print(f"   Total de vídeos prontos: {len(schedule_records)}")
    print(f"   Plano de agendamento salvo em: {plan_path}")
    print("=" * 65 + "\n")

    return schedule_records

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Produtor em lote do Lote 1 (TikTok US)")
    parser.add_argument("--days", type=int, default=3, help="Quantidade de dias a produzir agora (3 vídeos/dia)")
    parser.add_argument("--offset", type=int, default=1, help="Dia inicial (1 = amanhã)")
    args = parser.parse_args()

    produce_batch(start_day_offset=args.offset, total_days=args.days)
