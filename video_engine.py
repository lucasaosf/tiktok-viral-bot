import os
import subprocess
import random
from typing import Optional

def render_viral_video(
    background_video_path: str,
    voiceover_audio_path: str,
    subtitle_ass_path: str,
    output_video_path: str,
    start_offset: Optional[float] = None
) -> str:
    """
    Renders a vertical 9:16 viral TikTok video with burned-in animated subtitles
    and voiceover overlaid on high-octane Roblox gameplay.
    """
    if not os.path.exists(background_video_path):
        raise FileNotFoundError(f"Background video not found: {background_video_path}")
    if not os.path.exists(voiceover_audio_path):
        raise FileNotFoundError(f"Voiceover audio not found: {voiceover_audio_path}")
    if not os.path.exists(subtitle_ass_path):
        raise FileNotFoundError(f"Subtitle file not found: {subtitle_ass_path}")

    # 1. Determine exact duration of the audio using ffprobe
    probe_cmd = [
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", voiceover_audio_path
    ]
    probe_res = subprocess.run(probe_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
    audio_duration = float(probe_res.stdout.strip())
    total_duration = audio_duration + 0.5  # Add 0.5s padding at the end

    # 2. Randomize start point in the background video if start_offset not specified
    if start_offset is None:
        # Probe background duration
        bg_probe = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", background_video_path],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True
        )
        bg_duration = float(bg_probe.stdout.strip())
        max_start = max(0.0, bg_duration - total_duration - 2.0)
        start_offset = random.uniform(0.0, max_start) if max_start > 5.0 else 0.0

    os.makedirs(os.path.dirname(os.path.abspath(output_video_path)), exist_ok=True)

    # 3. Escape subtitle path for FFmpeg filter on Windows
    # FFmpeg requires forward slashes and escaped colons in filter graph paths
    clean_sub_path = os.path.abspath(subtitle_ass_path).replace("\\", "/").replace(":", "\\:")

    # Build video filter chain:
    # 1. Scale and crop to exact 1080x1920 (9:16 vertical)
    # 2. Burn in ASS stylized subtitles
    vf_filter = f"scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,subtitles='{clean_sub_path}'"

    cmd = [
        "ffmpeg", "-y",
        "-ss", str(round(start_offset, 2)),
        "-i", background_video_path,
        "-i", voiceover_audio_path,
        "-t", str(round(total_duration, 2)),
        "-vf", vf_filter,
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-crf", "22",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-map", "0:v:0",
        "-map", "1:a:0",
        output_video_path
    ]

    print(f"🎬 [Video Engine] Renderizando vídeo final de {total_duration:.1f}s...")
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        print("FFmpeg stderr:", result.stderr[-800:])
        raise RuntimeError(f"FFmpeg render failed with exit code {result.returncode}")

    print(f"✅ [Video Engine] Vídeo renderizado com sucesso: {output_video_path}")
    return output_video_path

if __name__ == "__main__":
    # Test render if assets exist
    bg = "assets/roblox_bg.mp4"
    audio = "test_audio.mp3"
    subs = "test_subs.ass"
    out = "test_output.mp4"
    if os.path.exists(bg) and os.path.exists(audio) and os.path.exists(subs):
        render_viral_video(bg, audio, subs, out)
