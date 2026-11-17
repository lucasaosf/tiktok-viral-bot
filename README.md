# 🎬 TikTok Viral Automation — US & Europe (Dark Channel & Live 24/7)

Sistema automatizado em Python para criação em massa de **vídeos virais (Shorts/TikTok)** e **transmissão contínua de Lives 24/7 de Roblox** com foco em monetização em **Dólar (USD)** nos **Estados Unidos e Europa**.

---

## 🚀 Como Funciona o Sistema

O robô automatiza o pipeline completo de produção de conteúdo *Faceless* (sem mostrar o rosto) em alta definição:

1. **Roteiros Virais em Inglês (`story_generator.py`):**
   - Cria histórias com ganchos fortes nos primeiros 3 segundos (*hooks*) para máxima retenção.
   - Textos calculados para durar **mais de 60 segundos** (requisito obrigatório para monetização do *TikTok Creator Rewards Program*).

2. **Voz Neural Americana (`voice_engine.py`):**
   - Gera narração natural e cinematográfica usando a voz oficial do TikTok gringo (`en-US-ChristopherNeural` da Microsoft Edge-TTS).
   - Calcula os milissegundos exatos de cada palavra para sincronização labial e legendagem.

3. **Legendas Dinâmicas Coloridas (`subtitle_engine.py`):**
   - Gera legendas no padrão *pop-up* (amarelo e branco com contorno preto grosso) no formato `.ass`.
   - Posicionamento no terço superior-médio da tela para não cobrir nem ser coberto pela interface do TikTok (botões de like/comentário e descrição).

4. **Renderização Vertical 9:16 (`video_engine.py`):**
   - Compila gameplay satisfatória de Roblox em **1080x1920 a 60 FPS**.
   - Corta o vídeo no tempo exato do áudio com padding suave.

5. **Transmissão Contínua de Live 24/7 (`live_streamer.py`):**
   - Transmite um loop ininterrupto de gameplays de Roblox para o TikTok Live via protocolo RTMP.
   - Permite receber presentes de live (Coins/Diamonds) convertíveis em dólares.

---

## 📦 Instalação

### 1. Pré-requisitos
* Python 3.10 ou superior
* FFmpeg instalado no sistema

### 2. Instalar dependências
```bash
pip install -r requirements.txt
```

---

## 🎯 Modos de Uso

### A. Gerar 1 vídeo viral completo:
```bash
python main.py --generate
```
O vídeo pronto em 1080x1920 será salvo na pasta `output/` junto com um arquivo de texto contendo o título, gancho e hashtags otimizadas.

### B. Gerar múltiplos vídeos em lote (Batch):
```bash
python main.py --count 3
```

### C. Iniciar Transmissão de Live 24/7 no TikTok:
Preencha a URL e a Chave no `.env` (ou passe via linha de comando):
```bash
python main.py --live
```

---

## 🇺🇸 Dicas para o TikTok Entregar nos EUA e Europa
1. **Hospedagem nos EUA:** Ao rodar na nuvem (VPS, Render ou Oracle Cloud), escolha servidores localizados nos Estados Unidos (ex: Ohio, Virgínia, Oregon).
2. **Metadados em Inglês:** Todas as legendas, títulos e hashtags geradas pelo bot já são 100% calibradas para o público norte-americano.
3. **Horários de Postagem:** Os melhores horários para o fuso horário americano (EST/PST) são entre 14:00 e 19:00 (horário de Brasília).
