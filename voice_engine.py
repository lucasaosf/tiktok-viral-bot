import asyncio
import os
import re
from typing import List, Dict, Any, Tuple
import edge_tts

DEFAULT_VOICE = "en-US-ChristopherNeural"

async def generate_speech_and_subtitles(
    text: str,
    output_audio_path: str,
    voice: str = DEFAULT_VOICE,
    words_per_subtitle: int = 3
) -> Tuple[float, List[Dict[str, Any]]]:
    """
    Generates speech audio using Microsoft Edge Neural TTS and computes
    punchy, word-synchronized subtitle cues ideal for TikTok reels.
    """
    communicate = edge_tts.Communicate(text, voice)
    
    sentences = []
    
    os.makedirs(os.path.dirname(os.path.abspath(output_audio_path)), exist_ok=True)
    with open(output_audio_path, "wb") as audio_file:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_file.write(chunk["data"])
            elif chunk["type"] == "SentenceBoundary":
                # Offset and duration are in 100-nanosecond units (10,000,000 units = 1 second)
                start_sec = chunk["offset"] / 10_000_000.0
                duration_sec = chunk["duration"] / 10_000_000.0
                end_sec = start_sec + duration_sec
                sentences.append({
                    "text": chunk["text"].strip(),
                    "start": start_sec,
                    "end": end_sec,
                    "duration": duration_sec
                })

    if not sentences:
        return 0.0, []

    total_duration = sentences[-1]["end"]

    # Split each sentence into small, high-impact bursts of 2-3 words for TikTok style
    subtitle_cues: List[Dict[str, Any]] = []
    
    for sent in sentences:
        words = sent["text"].split()
        if not words:
            continue
        
        sent_duration = max(0.1, sent["duration"])
        total_chars = sum(len(w) for w in words)
        if total_chars == 0:
            total_chars = len(words)
        
        # Group words into chunks of `words_per_subtitle`
        chunks = []
        for i in range(0, len(words), words_per_subtitle):
            chunks.append(words[i:i + words_per_subtitle])
            
        current_time = sent["start"]
        for chunk in chunks:
            chunk_text = " ".join(chunk).upper() # TikTok captions look bold in UPPERCASE
            chunk_chars = sum(len(w) for w in chunk)
            chunk_duration = sent_duration * (chunk_chars / total_chars)
            
            chunk_start = current_time
            chunk_end = current_time + chunk_duration
            current_time = chunk_end
            
            subtitle_cues.append({
                "text": chunk_text,
                "start": round(chunk_start, 2),
                "end": round(chunk_end, 2)
            })

    return total_duration, subtitle_cues

def generate_voice(text: str, output_audio: str, voice: str = DEFAULT_VOICE) -> Tuple[float, List[Dict[str, Any]]]:
    """Synchronous wrapper for generating speech and subtitles."""
    return asyncio.run(generate_speech_and_subtitles(text, output_audio, voice))

if __name__ == "__main__":
    sample_text = "My grandfather left me a locked iron box with only one instruction: never open it on a Tuesday."
    out = "test_audio.mp3"
    dur, subs = generate_voice(sample_text, out)
    print(f"Generated {dur:.2f}s audio at {out}")
    print(f"Total subtitle chunks: {len(subs)}")
    for s in subs[:5]:
        print(f"[{s['start']}s -> {s['end']}s]: {s['text']}")
