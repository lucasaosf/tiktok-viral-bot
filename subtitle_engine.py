from typing import List, Dict, Any

def format_ass_timestamp(seconds: float) -> str:
    """Formats float seconds into ASS timestamp format: H:MM:SS.cs"""
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    cs = int(round((seconds - int(seconds)) * 100))
    if cs >= 100:
        cs = 99
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"

def generate_ass_subtitles(subtitle_cues: List[Dict[str, Any]], output_path: str) -> str:
    """
    Generates a stylized .ass subtitle file with TikTok viral typography:
    - Font: Impact / Arial Black
    - Colors: High-contrast Neon Yellow and Crisp White
    - Thick black outline for 100% legibility over fast gameplay
    - Placed safely in the upper-center safe zone
    """
    header = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: YellowPop,Impact,75,&H0000FFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,1,0,1,6,2,2,40,40,750,1
Style: WhitePop,Impact,75,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,1,0,1,6,2,2,40,40,750,1
Style: GreenPop,Impact,75,&H0039FF14,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,1,0,1,6,2,2,40,40,750,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    dialogues = []
    styles = ["YellowPop", "WhitePop"]
    
    for idx, cue in enumerate(subtitle_cues):
        start_ts = format_ass_timestamp(cue["start"])
        end_ts = format_ass_timestamp(cue["end"])
        
        # Alternates between Yellow and White for dynamic eye tracking
        style = styles[idx % len(styles)]
        
        # Escape ASS special chars if needed
        clean_text = cue["text"].replace("\\", "\\\\").replace("{", "\\{").replace("}", "\\}")
        
        dialogues.append(f"Dialogue: 0,{start_ts},{end_ts},{style},,0,0,0,,{clean_text}")

    full_ass = header + "\n".join(dialogues) + "\n"
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(full_ass)

    return output_path

if __name__ == "__main__":
    sample_cues = [
        {"start": 0.0, "end": 1.2, "text": "MY GRANDFATHER LEFT"},
        {"start": 1.2, "end": 2.4, "text": "A SECRET BOX"},
        {"start": 2.4, "end": 3.8, "text": "AND ONE STRICT RULE"}
    ]
    generate_ass_subtitles(sample_cues, "test_subs.ass")
    print("ASS subtitle generated at test_subs.ass")
