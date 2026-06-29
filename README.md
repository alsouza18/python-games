# 🃏 Jogo de 21 (Blackjack)

Um jogo de Blackjack interativo para um jogador, desenvolvido com Gradio.

## 📋 Descrição

Jogue uma partida individual de Blackjack! O objetivo é chegar o mais perto possível de 21 pontos sem estourar (ultrapassar 21).

### Regras do Jogo

- **Valores das cartas:**
  - Números (2-10): valor nominal
  - J, Q, K: valem 10 pontos
  - Ás: vale 11 pontos (ajusta automaticamente para 1 se necessário para não estourar)

- **Como jogar:**
  1. Digite seu nome
  2. Clique em "Novo Jogo" para começar
  3. Escolha entre:
     - **Hit (Comprar)**: pegar mais uma carta
     - **Stand (Parar)**: manter suas cartas e encerrar o jogo
  4. Se ultrapassar 21 pontos, você perde automaticamente!

## 🚀 Instalação

### Pré-requisitos

- Python 3.6 ou superior

### Instalar dependências

```bash
pip install gradio
```

Ou, se preferir usar pip3:

```bash
pip3 install gradio
```

## ▶️ Como Executar

1. Navegue até a pasta do jogo:
```bash
cd python-games
```

2. Execute o jogo com Python 3:
```bash
python3 jogo_21.py
```

3. Abra seu navegador e acesse:
```
http://127.0.0.1:7860
```

4. Para parar o jogo, pressione `Ctrl+C` no terminal.

## 🎮 Como Usar

1. **Digite seu nome** no campo "Seu Nome"
2. Clique em **"Novo Jogo"** para iniciar uma nova partida
3. Suas cartas e pontos serão exibidos
4. Escolha sua jogada:
   - **Hit (Comprar)**: receba mais uma carta
   - **Stand (Parar)**: mantenha suas cartas atuais
   - **Reiniciar Partida**: comece uma nova partida a qualquer momento

## 🎵 Recursos

- Interface gráfica amigável com Gradio
- Sistema de pontuação automático
- Ajuste inteligente do valor dos Ases
- Mensagens de status do jogo
- Suporte para efeitos sonoros (quando disponíveis)

## 📝 Observações

- O jogo usa 2 baralhos completos (104 cartas) para maior variedade
- Os efeitos sonoros são opcionais e o jogo funciona normalmente sem eles
- A interface é acessível pelo navegador e pode ser compartilhada na rede local

## 🛠️ Solução de Problemas

**Problema**: Erro ao executar com `python`
- **Solução**: Use `python3` em vez de `python`

**Problema**: ModuleNotFoundError: No module named 'gradio'
- **Solução**: Execute `pip3 install gradio`

**Problema**: A página não carrega
- **Solução**: Verifique se o programa está rodando e acesse http://127.0.0.1:7860

## 👨‍💻 Tecnologias Utilizadas

- Python 3
- Gradio (interface web)
- urllib (para download de recursos)

---

Divirta-se jogando! 🎲🃏
