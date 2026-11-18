import os
import sys
import time
import random
import argparse
from playwright.sync_api import sync_playwright
from playwright_stealth import Stealth

SESSION_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tiktok_session")

def human_delay(min_s=1.0, max_s=2.5):
    """Gera uma pausa aleatória imitando a velocidade humana de leitura e navegação."""
    time.sleep(random.uniform(min_s, max_s))

def upload_video_to_tiktok(video_path: str, caption: str = "", auto_post: bool = True) -> bool:
    """
    Realiza o upload 100% seguro de um vídeo para o TikTok via Creator Center
    usando o perfil permanente do Google Chrome com tecnologia Stealth anti-detecção.
    """
    if not os.path.exists(video_path):
        print(f"❌ Erro: Arquivo de vídeo não encontrado em: {video_path}")
        return False

    if not os.path.exists(SESSION_DIR):
        print("⚠️ [AVISO] Sua conta ainda não foi conectada!")
        print("   Por favor, execute o arquivo 'conectar_conta.bat' primeiro para fazer login.")
        return False

    print("\n" + "=" * 65)
    print("🚀 [TIKTOK AUTO-UPLOADER] INICIANDO POSTAGEM SEGURA (STEALTH)")
    print(f"   Vídeo: {os.path.basename(video_path)}")
    print(f"   Tamanho: {os.path.getsize(video_path) / (1024*1024):.1f} MB")
    print(f"   Perfil do Chrome: {SESSION_DIR}")
    print("=" * 65)

    stealth = Stealth()

    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir=SESSION_DIR,
            channel="chrome",
            headless=False,
            viewport={"width": 1280, "height": 850},
            args=[
                "--no-first-run",
                "--no-default-browser-check",
                "--disable-blink-features=AutomationControlled"
            ]
        )

        page = context.pages[0] if context.pages else context.new_page()
        stealth.apply_stealth_sync(page)

        print("\n🌐 Acessando o TikTok Creator Center...")
        page.goto("https://www.tiktok.com/creator-center/upload?lang=en", wait_until="domcontentloaded")
        human_delay(2.5, 4.0)

        # Verifica se caiu na tela de login
        if "login" in page.url.lower():
            print("\n⚠️ A sessão expirou ou a conta não está logada.")
            print("   Por favor, execute 'conectar_conta.bat' para renovar seu acesso.")
            context.close()
            return False

        print("🔍 Localizando área de upload de vídeo...")

        # Procura pelo seletor de input de arquivo (direto na página ou dentro de iframe)
        file_input = None
        for _ in range(15):
            file_inputs = page.locator('input[type="file"]')
            if file_inputs.count() > 0:
                file_input = file_inputs.first
                break
            
            # Checa em iframes do TikTok Studio
            for frame in page.frames:
                frame_inputs = frame.locator('input[type="file"]')
                if frame_inputs.count() > 0:
                    file_input = frame_inputs.first
                    break
            
            if file_input:
                break
            human_delay(0.8, 1.5)

        if not file_input:
            print("❌ Não foi possível encontrar o campo de upload de vídeo no Creator Center.")
            context.close()
            return False

        print("📤 Enviando arquivo de vídeo para a plataforma...")
        file_input.set_input_files(video_path)
        human_delay(3.0, 5.0)

        print("⏳ Aguardando processamento do vídeo pelo TikTok...")
        # Aguarda a aparição do campo de legenda / título
        caption_editor = None
        editor_selectors = [
            'div[contenteditable="true"]',
            'div.DraftEditor-root',
            'div[data-e2e="caption-editor"]',
            'div[class*="public-DraftEditor"]',
            'div[class*="notranslate"]'
        ]

        for _ in range(30):
            for sel in editor_selectors:
                el = page.locator(sel)
                if el.count() > 0 and el.first.is_visible():
                    caption_editor = el.first
                    break
            if caption_editor:
                break
            human_delay(1.0, 2.0)

        if caption_editor and caption:
            print("✍️ Preenchendo legenda e hashtags com digitação humana...")
            caption_editor.click()
            human_delay(0.5, 1.0)
            
            # Limpa qualquer texto inicial (às vezes o TikTok insere o nome do arquivo)
            page.keyboard.press("Control+A")
            page.keyboard.press("Backspace")
            human_delay(0.3, 0.7)

            # Digita a legenda caractere por caractere simulando velocidade humana
            for char in caption:
                page.keyboard.type(char)
                time.sleep(random.uniform(0.015, 0.055))

            human_delay(1.5, 2.5)

        # Aguarda botão de postar ficar ativo
        print("🔍 Verificando botão de publicação...")
        post_btn = None
        btn_selectors = [
            'button[data-e2e="post_video_button"]',
            'button:has-text("Post")',
            'button:has-text("Publicar")',
            'div.btn-post > button'
        ]

        for _ in range(25):
            for b_sel in btn_selectors:
                btn = page.locator(b_sel)
                if btn.count() > 0 and btn.first.is_visible() and btn.first.is_enabled():
                    post_btn = btn.first
                    break
            if post_btn:
                break
            human_delay(1.0, 2.0)

        if not post_btn:
            print("⚠️ Botão de postar ainda não habilitado. O vídeo pode estar terminando o upload.")
            print("   Você pode clicar em 'Post' manualmente na janela do Chrome.")
            time.sleep(5)
            context.close()
            return True

        if auto_post:
            print("🖱️ Clicando no botão 'Post' (Publicar)...")
            human_delay(1.0, 2.0)
            post_btn.click()
            human_delay(4.0, 6.0)

            print("\n" + "=" * 65)
            print("🎉 [SUCESSO] VÍDEO PUBLICADO COM SUCESSO NO TIKTOK!")
            print(f"   Vídeo: {os.path.basename(video_path)}")
            print("=" * 65 + "\n")
            time.sleep(3)
        else:
            print("\n👀 [MODO DE REVISÃO] Vídeo e legenda carregados na tela!")
            print("   Confira na janela aberta e clique em 'Post' quando desejar.")
            time.sleep(10)

        context.close()
        return True

def get_latest_video():
    """Retorna o vídeo mais recente na pasta output."""
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
    if not os.path.exists(output_dir):
        return None, None

    mp4_files = [
        os.path.join(output_dir, f) for f in os.listdir(output_dir)
        if f.lower().endswith(".mp4")
    ]
    if not mp4_files:
        return None, None

    mp4_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
    latest_video = mp4_files[0]

    # Procura legenda correspondente
    caption_file = latest_video.rsplit(".", 1)[0] + "_caption.txt"
    caption_text = ""
    if os.path.exists(caption_file):
        with open(caption_file, "r", encoding="utf-8") as f:
            caption_text = f.read().strip()

    return latest_video, caption_text

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Uploader Stealth de Vídeos para o TikTok")
    parser.add_argument("--video", default="", help="Caminho do vídeo MP4 para upload")
    parser.add_argument("--caption", default="", help="Legenda do vídeo")
    parser.add_argument("--no-auto-post", action="store_true", help="Não clica em postar automaticamente (modo revisão)")

    args = parser.parse_args()

    v_path = args.video
    c_text = args.caption

    if not v_path:
        v_path, auto_c = get_latest_video()
        if not c_text:
            c_text = auto_c

    if not v_path:
        print("❌ Nenhum vídeo encontrado na pasta output/ para publicar.")
        sys.exit(1)

    upload_video_to_tiktok(video_path=v_path, caption=c_text, auto_post=not args.no_auto_post)
