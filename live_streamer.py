import os
import sys
import time
import subprocess
from dotenv import load_dotenv

load_dotenv()

DEFAULT_RTMP_URL = os.getenv("TIKTOK_RTMP_URL", "")
DEFAULT_STREAM_KEY = os.getenv("TIKTOK_STREAM_KEY", "")

def get_font_param() -> str:
    """Retorna o parâmetro de fonte compatível com Windows e Linux para o drawtext do FFmpeg."""
    if os.name == "nt":
        # Windows
        win_font = "C\\:/Windows/Fonts/arialbd.ttf"
        if os.path.exists("C:/Windows/Fonts/arialbd.ttf"):
            return f"fontfile='{win_font}'"
        return "fontfile='C\\:/Windows/Fonts/arial.ttf'"
    else:
        # Linux / Nuvem
        for p in ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", "/usr/share/fonts/TTF/DejaVuSans.ttf"]:
            if os.path.exists(p):
                return f"fontfile='{p}'"
        return "font='Arial'"

def stream_to_tiktok_live(
    video_path: str,
    rtmp_url: str = DEFAULT_RTMP_URL,
    stream_key: str = DEFAULT_STREAM_KEY,
    with_overlay: bool = True,
    auto_reconnect: bool = True,
    test_mode: bool = False
):
    """
    Transmite um loop ininterrupto de vídeo (ex: gameplay de Roblox) 24/7 para o TikTok Live via RTMP.
    Inclui banners visuais atraentes para converter espectadores em seguidores.
    """
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Arquivo de vídeo não encontrado: {video_path}")

    if test_mode:
        print("\n🧪 [MODO DE TESTE] Testando codificação e pipeline de transmissão por 5 segundos...")
        full_target = "assets/test_stream_output.flv"
    else:
        if not rtmp_url or not stream_key:
            print("\n" + "=" * 65)
            print("⚠️ [TIKTOK LIVE] CHAVE DE TRANSMISSÃO NÃO CONFIGURADA")
            print("=" * 65)
            print("Para iniciar a Live 24/7, você precisa colocar sua Stream Key no arquivo .env:")
            print("   TIKTOK_RTMP_URL=rtmp://live-push.tiktok.com/live/")
            print("   TIKTOK_STREAM_KEY=sua_chave_aqui")
            print("\nAssim que colar sua chave, basta rodar este comando novamente!")
            print("=" * 65 + "\n")
            return
        full_target = f"{rtmp_url.rstrip('/')}/{stream_key}"

    print("=" * 65)
    print("🔴 [TIKTOK LIVE 24/7] TRANSMISSOR PROFISSIONAL PRONTO")
    print(f"   Arquivo Base: {video_path}")
    print(f"   Destino: {'TESTE LOCAL' if test_mode else rtmp_url}")
    print(f"   Banners de Engajamento: {'Ativados' if with_overlay else 'Desativados'}")
    print(f"   Auto-reconectar: {auto_reconnect}")
    print("=" * 65)

    vf_filters = ["scale=1080:1920:force_original_aspect_ratio=increase", "crop=1080:1920"]
    if with_overlay:
        font_p = get_font_param()
        top_text = f"drawtext=text='24/7 ROBLOX SPEEDRUN':{font_p}:fontcolor=white:fontsize=48:box=1:boxcolor=black@0.65:boxborderw=14:x=(w-text_w)/2:y=240"
        bottom_text = f"drawtext=text='FOLLOW FOR GOOD LUCK!':{font_p}:fontcolor=yellow:fontsize=44:box=1:boxcolor=black@0.65:boxborderw=14:x=(w-text_w)/2:y=h-360"
        vf_filters.extend([top_text, bottom_text])

    vf_chain = ",".join(vf_filters)

    cmd = [
        "ffmpeg", "-y",
        "-re",                          # Taxa de quadros nativa em tempo real
        "-stream_loop", "-1",           # Loop infinito ininterrupto
        "-i", video_path,
        "-vf", vf_chain,
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-b:v", "2800k",
        "-maxrate", "3000k",
        "-bufsize", "6000k",
        "-pix_fmt", "yuv420p",
        "-g", "60",                     # Keyframe a cada 1 segundo para estabilidade máxima
        "-c:a", "aac",
        "-b:a", "128k",
        "-ar", "44100",
        "-f", "flv"
    ]

    if test_mode:
        cmd.extend(["-t", "5", full_target])
        print("Executando teste local de 5 segundos...")
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if res.returncode == 0:
            print("✅ [TESTE APROVADO] O pipeline de streaming 24/7 está 100% calibrado e pronto para o TikTok!")
            if os.path.exists(full_target):
                os.remove(full_target)
        else:
            print("Erro no teste:", res.stderr.decode("utf-8", errors="ignore")[-400:])
        return

    cmd.append(full_target)

    # Loop de transmissão contínua com reconexão automática
    reconnect_count = 0
    while True:
        try:
            print(f"\n📡 [STATUS] Conectando aos servidores do TikTok Live... (Sessão #{reconnect_count + 1})")
            process = subprocess.Popen(cmd)
            process.wait()
            
            if not auto_reconnect:
                break
                
            reconnect_count += 1
            print("⚠️ Conexão com o TikTok oscilou. Reconectando automaticamente em 5 segundos...")
            time.sleep(5)
        except KeyboardInterrupt:
            print("\n🛑 Transmissão de Live encerrada pelo usuário.")
            if process:
                process.terminate()
            break
        except Exception as e:
            print(f"Erro inesperado: {e}")
            if not auto_reconnect:
                break
            time.sleep(5)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Transmissor de Live 24/7 para TikTok")
    parser.add_argument("--video", default="assets/roblox_bg.mp4", help="Caminho do vídeo para transmitir em loop")
    parser.add_argument("--rtmp", default=DEFAULT_RTMP_URL, help="URL RTMP do TikTok")
    parser.add_argument("--key", default=DEFAULT_STREAM_KEY, help="Chave de transmissão")
    parser.add_argument("--test", action="store_true", help="Executa um teste local de 5s para validar o pipeline")
    parser.add_argument("--no-overlay", action="store_true", help="Desativa os banners de follow na tela")

    args = parser.parse_args()
    stream_to_tiktok_live(
        video_path=args.video,
        rtmp_url=args.rtmp,
        stream_key=args.key,
        with_overlay=not args.no_overlay,
        test_mode=args.test
    )
