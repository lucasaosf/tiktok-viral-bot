# 🎬 TikTok Viral Automation — US & Europe (Dark Channel, Auto-Upload & Live 24/7)

Sistema profissional em Python para criação em massa de **vídeos virais (Shorts/TikTok)**, **publicação 100% automatizada com tecnologia anti-detecção (Stealth)** e **transmissão contínua de Lives 24/7 de Roblox** com foco em monetização em **Dólar (USD)** nos **Estados Unidos e Europa**.

---

## 🚀 Como Funciona o Sistema

O robô automatiza o ciclo completo de crescimento no TikTok:

1. **Roteiros Virais em Inglês (`story_generator.py`):**
   - Histórias com ganchos fortes nos primeiros 3 segundos (*hooks*) para máxima retenção.
   - Textos calculados para durar **mais de 60 segundos** (requisito obrigatório para o *TikTok Creator Rewards Program*).

2. **Voz Neural Americana (`voice_engine.py`):**
   - Narração natural e cinematográfica usando a voz oficial do TikTok gringo (`en-US-ChristopherNeural` da Microsoft Edge-TTS).
   - Milissegundos exatos mapeados para sincronização labial e legendagem.

3. **Legendas Dinâmicas Coloridas (`subtitle_engine.py`):**
   - Legendas no padrão *pop-up* (amarelo neon e branco com contorno preto) no formato `.ass`.
   - Posicionamento no terço superior para não conflitar com a interface do TikTok.

4. **Renderização Vertical 9:16 (`video_engine.py`):**
   - Compila gameplay de Roblox em **1080x1920 a 60 FPS**.

5. **Conexão Segura & Postagem Automática (`tiktok_auth.py` e `tiktok_uploader_stealth.py`):**
   - Usa o executável oficial do Google Chrome com perfil persistente (`tiktok_session/`).
   - Tecnologia **Playwright Stealth** que mascara `navigator.webdriver = false`.
   - Digitação e navegação com variações de velocidade humana para **risco zero** de ban ou shadowban.

6. **Transmissão Contínua de Live 24/7 (`live_streamer.py`):**
   - Transmite Roblox ininterruptamente com trilha sonora Lofi e banners de engajamento (*Follow for Good Luck*).
   - Reconexão automática em caso de oscilação de rede.

---

## 📦 Instalação Rápida

```bash
pip install -r requirements.txt
playwright install chromium
```

---

## 🎯 Como Usar no Dia a Dia (Arquivos .BAT com 1 Clique)

### 1. Conectar a sua Conta (Passo Único):
Dê dois cliques em **`conectar_conta.bat`**.
- O Google Chrome oficial abrirá na página do TikTok.
- Faça login na sua conta (`@lucas.aosf`) via QR Code ou senha.
- Sua sessão ficará salva permanentemente em `tiktok_session/` (o robô nunca mais pedirá senha).

### 2. Gerar Vídeos em Lote:
Dê dois cliques em **`gerar_videos.bat`**.
- Digite a quantidade de vídeos desejada (ex: 3).
- Os vídeos de >60s serão renderizados em `output/` com suas legendas e hashtags.

### 3. Publicar Automaticamente no TikTok:
Dê dois cliques em **`publicar_automatico.bat`**.
- **Opção 1:** O robô abre o Creator Center, faz upload do vídeo mais recente, digita a legenda/hashtags e publica sozinho.
- **Opção 2:** Modo revisão (carrega tudo na tela para você conferir antes de postar).

### 4. Iniciar a Live 24/7:
Dê dois cliques em **`iniciar_live.bat`**.
- **Opção 1:** Inicia a transmissão ao vivo (requer Stream Key no `.env`).
- **Opção 2:** Faz um teste local de 5 segundos.

---

## 🇺🇸 Estratégia de Crescimento (EUA & Europa)
- **Frequência:** 3 vídeos por dia (14:00, 17:00 e 21:00 horário de Brasília — horários nobres nos EUA).
- **Meta:** Atingir 1.000 seguidores para desbloquear a chave de Live RTMP e link na bio.
- **Monetização:** RPM de $0.80 a $2.50+ USD por mil views após qualificação.
