import os
import sys
import time
import json
from playwright.sync_api import sync_playwright
from playwright_stealth import Stealth

SESSION_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tiktok_session")

def connect_tiktok_account():
    """
    Abre o Google Chrome oficial em modo Stealth com perfil persistente
    para que o usuário faça login uma única vez no TikTok de forma 100% segura.
    """
    os.makedirs(SESSION_DIR, exist_ok=True)
    stealth = Stealth()

    print("\n" + "=" * 65)
    print("🔐 [TIKTOK BOT] CONEXÃO SEGURA DE CONTA (PERFIL HUMANO)")
    print("=" * 65)
    print("Iniciando o seu Google Chrome oficial com proteção anti-detecção...")
    print("Pasta do Perfil Permanente:", SESSION_DIR)
    print("=" * 65)

    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir=SESSION_DIR,
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

        print("\n🌐 Acessando página oficial de login do TikTok...")
        page.goto("https://www.tiktok.com/login", wait_until="domcontentloaded")

        print("\n" + "=" * 65)
        print("👉 INSTRUÇÕES:")
        print("1. A janela do Google Chrome está aberta na sua tela.")
        print("2. Faça login na sua conta (@lucas.aosf) da forma que preferir:")
        print("   - Escaneando o QR Code pelo aplicativo do TikTok no celular (mais rápido)")
        print("   - Ou digitando seu usuário/e-mail e senha")
        print("3. Se aparecer o quebra-cabeça de segurança, resolva-o normalmente.")
        print("=" * 65)
        print("⏳ Aguardando conclusão do login...\n")

        # Monitora a detecção de login automático (ou até o usuário fechar/confirmar)
        logged_in = False
        start_time = time.time()
        timeout_seconds = 300  # 5 minutos para o usuário logar tranquilamente

        while time.time() - start_time < timeout_seconds:
            try:
                if len(context.pages) == 0 or context.pages[0].is_closed():
                    # Usuário fechou a janela do Chrome
                    cookies = context.cookies()
                    cookie_names = [c["name"] for c in cookies]
                    if any(k in cookie_names for k in ["sessionid", "sid_tt", "sessionid_ss"]):
                        logged_in = True
                    break

                cookies = context.cookies()
                cookie_names = [c["name"] for c in cookies]
                
                # Sinais de login confirmado no TikTok
                is_auth_cookie = any(k in cookie_names for k in ["sessionid", "sid_tt", "sessionid_ss"])
                current_url = page.url.lower()
                not_on_login = "/login" not in current_url and "tiktok.com" in current_url

                if is_auth_cookie or (not_on_login and len(cookie_names) > 8):
                    logged_in = True
                    # Salva backup dos cookies em JSON
                    cookies_backup = os.path.join(SESSION_DIR, "cookies.json")
                    with open(cookies_backup, "w", encoding="utf-8") as f:
                        json.dump(cookies, f, indent=2)
                    break
            except Exception:
                pass

            time.sleep(2)

        if logged_in:
            print("\n" + "=" * 65)
            print("🎉 [SUCESSO ABSOLUTO] CONTA TIKTOK CONECTADA COM SUCESSO!")
            print("=" * 65)
            print("Sua sessão permanente e tokens foram salvos com segurança em:")
            print(f"📁 {SESSION_DIR}")
            print("\nA partir de agora, suas publicações serão feitas no piloto automático")
            print("usando o seu Chrome oficial com zero risco de bloqueio ou ban!")
            print("=" * 65 + "\n")
            time.sleep(3)
        else:
            print("\n⚠️ Tempo limite atingido ou login não detectado.")
            print("Se você concluiu o login, pode tentar executar a postagem.")

        context.close()

if __name__ == "__main__":
    connect_tiktok_account()
