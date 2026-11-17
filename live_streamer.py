import os
import sys
import time
import subprocess
from dotenv import load_dotenv

load_dotenv()

DEFAULT_RTMP_URL = os.getenv("TIKTOK_RTMP_URL", "")
DEFAULT_STREAM_KEY = os.getenv("TIKTOK_STREAM_KEY", "")

def stream_to_tiktok_live(
    video_path: str,
    rtmp_url: str = DEFAULT_RTMP_URL,
    stream_key: str = DEFAULT_STREAM_KEY,
    auto_reconnect: bool = True
):
    """
    Broadcasts a looping video (e.g. Roblox parkour / gameplay) 24/7 to TikTok Live via RTMP.
    Designed to run continuously on a cloud server or local machine.
    """
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video loop file not found: {video_path}")

    if not rtmp_url or not stream_key:
        print("\n⚠️ [TikTok Live] Chave de transmissão ou URL RTMP não configuradas!")
        print("   Para fazer live 24/7, você precisa pegar a Chave RTMP no TikTok Live Studio")
        print("   e preenchê-la no arquivo .env (TIKTOK_RTMP_URL e TIKTOK_STREAM_KEY).\n")
        return

    full_target = f"{rtmp_url.rstrip('/')}/{stream_key}"
    print("=" * 65)
    print("🔴 [TIKTOK LIVE 24/7] INICIANDO TRANSMISSÃO CONTÍNUA")
    print(f"   Arquivo de Origem: {video_path}")
    print(f"   Destino RTMP: {rtmp_url}")
    print(f"   Auto-reconectar: {auto_reconnect}")
    print("=" * 65)

    cmd = [
        "ffmpeg",
        "-re",                          # Lê a fonte na velocidade nativa em tempo real
        "-stream_loop", "-1",           # Loop infinito
        "-i", video_path,
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-b:v", "2800k",
        "-maxrate", "3000k",
        "-bufsize", "6000k",
        "-pix_fmt", "yuv420p",
        "-g", "60",                     # Keyframe a cada 1 segundo (a 60fps)
        "-c:a", "aac",
        "-b:a", "128k",
        "-ar", "44100",
        "-f", "flv",
        full_target
    ]

    while True:
        try:
            print("\n📡 Conectando ao servidor do TikTok e iniciando envio de pacotes...")
            process = subprocess.Popen(cmd)
            process.wait()
            
            if not auto_reconnect:
                break
                
            print("⚠️ Conexão interrompida. Tentando reconectar em 5 segundos...")
            time.sleep(5)
        except KeyboardInterrupt:
            print("\n🛑 Transmissão interrompida pelo usuário.")
            if process:
                process.terminate()
            break
        except Exception as e:
            print(f"Erro na transmissão: {e}")
            if not auto_reconnect:
                break
            time.sleep(5)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Transmissor de Live 24/7 para TikTok")
    parser.add_argument("--video", default="assets/roblox_bg.mp4", help="Caminho do vídeo para transmitir em loop")
    parser.add_argument("--rtmp", default=DEFAULT_RTMP_URL, help="URL RTMP do TikTok")
    parser.add_argument("--key", default=DEFAULT_STREAM_KEY, help="Chave de transmissão")

    args = parser.parse_args()
    stream_to_tiktok_live(args.video, args.rtmp, args.key)
