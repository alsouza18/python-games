# -*- coding: utf-8 -*-
import gradio as gr
import random
import os
import urllib.request

# ====================== LÓGICA DO JOGO ======================

def criar_baralho():
    naipes = ['♠', '♥', '♦', '♣']
    valores = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    return [valor + naipe for naipe in naipes for valor in valores] * 2  # 2 baralhos para mais variedade

def valor_carta(carta):
    valor = carta[:-1]
    if valor in ['J', 'Q', 'K']:
        return 10
    elif valor == 'A':
        return 11  # Ás inicialmente vale 11
    else:
        return int(valor)

def calcular_pontos(mao):
    pontos = sum(valor_carta(c) for c in mao)
    ases = sum(1 for c in mao if c.startswith('A'))

    # Ajusta o valor dos Ases de 11 para 1, se necessário, para evitar estourar (passar de 21)
    while pontos > 21 and ases:
        pontos -= 10  # Reduz 10 pontos (efetivamente transformando um Ás de 11 para 1)
        ases -= 1     # Decrementa o contador de Ases que ainda podem ser ajustados
    return pontos

# ====================== INTERFACE GRADIO ======================

# URLs para os arquivos de som curtos e apropriados
# Estes são efeitos sonoros curtos, não músicas longas.
# Links atualizados para serem diretos e funcionais.
SOUND_START_URL = "https://www.myinstants.com/media/sounds/game-start-super-mario-64.mp3" # Novo exemplo de som mais expressivo para início
SOUND_HIT_URL = "https://www.myinstants.com/media/sounds/bell.mp3" # Novo exemplo de som para 'comprar' (hit) - som de sino/campainha
SOUND_WIN_URL = "https://www.myinstants.com/media/sounds/correct-sound-effect.mp3" # Exemplo de som curto para vitória (funcional)
SOUND_LOSE_URL = "https://www.myinstants.com/media/sounds/fail-sound-effect.mp3" # Exemplo de som curto para derrota (funcional)

# Nomes de arquivo locais que serão usados após o download
SOUND_START = "sound_start.mp3"
SOUND_HIT = "sound_hit.mp3" # Nome do arquivo local para o som de 'comprar'
SOUND_WIN = "sound_win.mp3"
SOUND_LOSE = "sound_lose.mp3"

# Função para baixar os arquivos de som
def baixar_sons():
    """Baixa os arquivos de som se eles ainda não existirem"""
    sons = [
        (SOUND_START_URL, SOUND_START),
        (SOUND_HIT_URL, SOUND_HIT),
        (SOUND_WIN_URL, SOUND_WIN),
        (SOUND_LOSE_URL, SOUND_LOSE)
    ]
    
    for url, arquivo in sons:
        if not os.path.exists(arquivo):
            try:
                print(f"Baixando {arquivo}...")
                urllib.request.urlretrieve(url, arquivo)
                print(f"✓ {arquivo} baixado com sucesso!")
            except Exception as e:
                print(f"⚠ Erro ao baixar {arquivo}: {e}")
                print(f"  O jogo funcionará, mas sem este som.")

# Baixa os sons ao iniciar o programa
print("Verificando arquivos de som...")
baixar_sons()
print("Pronto para jogar!\n")

def get_sound(sound_file):
    """Retorna o arquivo de som se ele existir, caso contrário None"""
    return sound_file if os.path.exists(sound_file) else None

def novo_jogo(nome_jogador="Jogador"):
    baralho = criar_baralho()
    random.shuffle(baralho)

    # Distribui 2 cartas para o único jogador
    mao = [baralho.pop(), baralho.pop()]
    pontos = calcular_pontos(mao)

    status_msg = f"Jogo iniciado! É a sua vez, {nome_jogador}. ({pontos} pontos)"
    game_state_str = "PLAYING"

    return (
        mao, pontos,
        baralho, status_msg, game_state_str, get_sound(SOUND_START)
    )

def handle_jogada(player_action, mao, pontos, baralho, status_atual, game_state_str, nome_jogador="Jogador"):
    sound_to_play = None

    # Se o jogo já acabou, não permite mais jogadas
    if game_state_str == "GAME_OVER":
        return mao, pontos, baralho, status_atual, game_state_str, None

    if player_action == "hit":
        mao.append(baralho.pop())
        pontos = calcular_pontos(mao)
        if pontos > 21:
            status_msg = f"{nome_jogador} estourou! Você perdeu! 😭 ({pontos} pontos)"
            game_state_str = "GAME_OVER"
            sound_to_play = get_sound(SOUND_LOSE)
        else:
            status_msg = f"É a sua vez, {nome_jogador}. ({pontos} pontos)"
            sound_to_play = get_sound(SOUND_HIT) # Som para a ação de 'comprar'

    elif player_action == "stand":
        game_state_str = "GAME_OVER"
        if pontos > 21: # Caso o jogador tenha estourado e tentou 'stand'
             status_msg = f"{nome_jogador} estourou! Você perdeu! 😭 ({pontos} pontos)"
             sound_to_play = get_sound(SOUND_LOSE)
        else:
            status_msg = f"{nome_jogador} parou com {pontos} pontos. Fim de jogo. ({pontos} pontos)"
            sound_to_play = get_sound(SOUND_WIN) # Consideramos 'parar' sem estourar como um tipo de 'vitória' na partida individual

    return (
        mao, calcular_pontos(mao),
        baralho, status_msg, game_state_str, sound_to_play
    )

def formatar_mao(mao):
    return "  ".join(mao) if mao else ""


# Interface
with gr.Blocks(title="🃏 Jogo 21 - Blackjack (Jogador Individual)") as demo:
    gr.Markdown("# 🃏 Jogo de 21 (Blackjack) - Jogador Individual")
    gr.Markdown("Jogue uma partida individual de Blackjack. Tente chegar o mais perto possível de 21 sem estourar!")

    nome_jogador_input = gr.Textbox(label="Seu Nome", value="Jogador", interactive=True)

    with gr.Row():
        cartas_display = gr.Textbox(label="Suas Cartas", value="", interactive=False, scale=1)
        pontos_display = gr.Textbox(label="Seus Pontos", value="", interactive=False, scale=0)
        status = gr.Textbox(label="Status do Jogo", value="Digite seu nome e clique em Novo Jogo para começar", interactive=False, scale=2)

    game_state = gr.Textbox(visible=False, value="INITIAL")  # Para controlar estado

    # Componente de áudio (visível para depuração)
    audio_output = gr.Audio(autoplay=True, visible=True, type="filepath", label="Som do Jogo (para depuração)")

    with gr.Row():
        btn_novo = gr.Button("Novo Jogo", variant="primary")
        btn_hit = gr.Button("Hit (Comprar)", variant="secondary")
        btn_stand = gr.Button("Stand (Parar)")
        btn_reiniciar = gr.Button("Reiniciar Partida") # Novo botão de reinício

    # Variáveis de estado para o backend (apenas para um jogador)
    mao_state = gr.State()
    pontos_state = gr.State()
    baralho_state = gr.State()
    nome_jogador_state = gr.State(value="Jogador") # Armazena o nome do jogador

    # Eventos
    # Ao digitar o nome, atualiza o estado
    nome_jogador_input.change(lambda name: name, inputs=nome_jogador_input, outputs=nome_jogador_state)

    btn_novo.click(
        novo_jogo,
        inputs=[nome_jogador_state], # Passa o nome do jogador
        outputs=[
            mao_state, pontos_state,
            baralho_state, status, game_state, audio_output
        ]
    ).then(
        lambda m: formatar_mao(m), inputs=mao_state, outputs=cartas_display
    ).then(
        lambda p: str(p), inputs=pontos_state, outputs=pontos_display
    ).then( # Move clear audio to the very end
        lambda: None,
        outputs=audio_output
    )

    btn_hit.click(
        lambda *args: handle_jogada("hit", *args),
        inputs=[
            mao_state, pontos_state,
            baralho_state, status, game_state, nome_jogador_state
        ],
        outputs=[
            mao_state, pontos_state,
            baralho_state, status, game_state, audio_output
        ]
    ).then(
        lambda m: formatar_mao(m), inputs=mao_state, outputs=cartas_display
    ).then(
        lambda p: str(p), inputs=pontos_state, outputs=pontos_display
    ).then( # Move clear audio to the very end
        lambda: None,
        outputs=audio_output
    )

    btn_stand.click(
        lambda *args: handle_jogada("stand", *args),
        inputs=[
            mao_state, pontos_state,
            baralho_state, status, game_state, nome_jogador_state
        ],
        outputs=[
            mao_state, pontos_state,
            baralho_state, status, game_state, audio_output
        ]
    ).then(
        lambda m: formatar_mao(m), inputs=mao_state, outputs=cartas_display
    ).then(
        lambda p: str(p), inputs=pontos_state, outputs=pontos_display
    ).then( # Move clear audio to the very end
        lambda: None,
        outputs=audio_output
    )

    # Evento para o novo botão de reinício
    btn_reiniciar.click(
        novo_jogo, # Reutiliza a função de novo_jogo para resetar tudo
        inputs=[nome_jogador_state], # Passa o nome do jogador
        outputs=[
            mao_state, pontos_state,
            baralho_state, status, game_state, audio_output
        ]
    ).then(
        lambda m: formatar_mao(m), inputs=mao_state, outputs=cartas_display
    ).then(
        lambda p: str(p), inputs=pontos_state, outputs=pontos_display
    ).then( # Move clear audio to the very end
        lambda: None,
        outputs=audio_output
    )

demo.launch(share=True)
