import os
import time
import random
import pygame #type: ignore

ARQUIVO_QUIZ = "QUIZ.txt"  # Nome do arquivo de perguntas
ARQUIVO_RANKING = "ranking.txt"  # nome do arquivo de ranking

tempo = 2  # Tempo de espera entre uma pergunta e outra

# Temas fixos
TEMAS_FIXOS = [
    "Programação",
    "Desenhos Animados",
    "Curiosidades",
    "Cultura Brasileira",
    "Sabedoria De Vó"
]

# Função para limpar a tela do terminal
def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

# Função para carregar as perguntas do arquivo
def carregar_perguntas():
    # Cria um dicionário para armazenar as perguntas separadas por tema
    perguntas = {}

    # Abre o arquivo de perguntas em modo leitura com codificação UTF-8
    arquivo = open(ARQUIVO_QUIZ, "r", encoding="utf-8")

    # Lê o arquivo linha por linha
    for linha in arquivo:
        # Divide a linha pelo caractere "|" para separar os campos da pergunta
        partes = linha.strip().split("|")

        # Se a linha não tiver exatamente 7 partes, ela é ignorada
        if len(partes) != 7:
            continue

        # Pega o tema da pergunta, remove espaços e capitaliza corretamente
        tema = partes[1].strip().title()

        # Verifica se o tema está dentro da lista de temas fixos
        if tema not in TEMAS_FIXOS:
            continue

        # Pega o texto da pergunta e as alternativas
        texto = partes[0].strip()
        alternativas = partes[2:6]
        correta = partes[6].strip().upper()

        # Adiciona a pergunta ao dicionário, agrupando pelo tema
        if tema not in perguntas:
            perguntas[tema] = []
        perguntas[tema].append({
            "texto": texto,
            "alternativas": alternativas,
            "correta": correta
        })

    # Fecha o arquivo após leitura
    arquivo.close()

    # Retorna o dicionário com todas as perguntas organizadas
    return perguntas

# Função para mostrar os temas disponíveis ao usuário
def mostrar_temas(perguntas):

    print("""SHOW DO MILHÃO 🌽💸
          
Bem vindo ao jogo do milhão (ou uma cópia barata dele...)""")

    print("\nTemas disponíveis:\n ")

    som_inicio = pygame.mixer.Sound("efeitos sonoros/inicio.mp3")
    som_inicio.set_volume(1) 
    som_inicio.play()

    temas = []
    for i, tema in enumerate(TEMAS_FIXOS):
        # Mostra apenas os temas que têm perguntas
        if tema in perguntas:
            print(f"{i+1} - {tema}")
            temas.append(tema)
    print()
    return temas

# Função para pedir que o usuário escolha um tema
def escolher_tema(temas):
    while True:
        escolha = input("Escolha o número do tema: ")
        if escolha.isdigit():
            escolha = int(escolha)
            if 1 <= escolha <= len(temas):
                return temas[escolha-1]
        print("Opção inválida, tente de novo.")

# Função para escolher a quantidade de perguntas
def escolher_quantidade(max_qtd):
    while True:
        qtd = input(f"""
Prêmio mínimo: R$500.000,00
Prêmio máximo: R$1.000.000,00

Quantas perguntas quer? (min 5, max {max_qtd}): """)
        if qtd.isdigit():
            qtd = int(qtd)
            if 5 <= qtd <= max_qtd:
                return qtd
        print("Quantidade inválida, tente novamente.")

# Função para atualizar o ranking
def atualizar_ranking(nome, acertos):
    ranking = {}

    # tenta carregar o ranking existente
    if os.path.exists(ARQUIVO_RANKING):
        with open(ARQUIVO_RANKING, "r", encoding="utf-8") as f:
            for linha in f:
                partes = linha.strip().split("|")
                if len(partes) == 2 and partes[1].isdigit():
                    nome_existente = partes[0].strip()
                    acertos_existente = int(partes[1])
                    ranking[nome_existente] = acertos_existente

    # atualiza ou adiciona a pontuacao do jogador se for maior
    if nome in ranking:
        ranking[nome] = max(ranking[nome], acertos)
    else:
        ranking[nome] = acertos

    # salva o novo ranking ordenado por acertos decrescentes
    ranking_ordenado = sorted(ranking.items(), key=lambda x: x[1], reverse=True)
    with open(ARQUIVO_RANKING, "w", encoding="utf-8") as f:
        for jogador, pontos in ranking_ordenado:
            f.write(f"{jogador}|{pontos}\n")

# Função principal do jogo
def main():
    pygame.mixer.init()
    
    # criação de canais para que não tenha sobreposição e cancelamento de som
    canal_fundo = pygame.mixer.Channel(0)
    canal_efeitos = pygame.mixer.Channel(1)

    musica_fundo = pygame.mixer.Sound("efeitos sonoros/musicaFundo.mp3")
    som_certo = pygame.mixer.Sound("efeitos sonoros/certaResposta.mp3")
    som_errado = pygame.mixer.Sound("efeitos sonoros/errado.mp3")
    som_risada = pygame.mixer.Sound("efeitos sonoros/risada.mp3")
    som_inicio = pygame.mixer.Sound("efeitos sonoros/inicio.mp3")
    som_inicio = pygame.mixer.Sound("efeitos sonoros/umMilhão.mp3")
    som_milhao = pygame.mixer.Sound("efeitos sonoros/umMilhão.mp3")


    canal_fundo.set_volume(0.4)
    canal_fundo.play(musica_fundo, loops=-1)

    # Limpa a tela antes de iniciar
    limpar_tela()

    # Carrega as perguntas do arquivo
    perguntas = carregar_perguntas()

    # Se não houver perguntas, o programa é encerrado
    if not perguntas:
        print("Não há perguntas disponíveis.")
        return

    # variável para armazenar o nome
    nome = input("Digite o seu nome: ")

    # Mostra os temas e permite que o usuário escolha um
    temas = mostrar_temas(perguntas)
    tema_escolhido = escolher_tema(temas)

    # Pega a lista de perguntas do tema escolhido
    perguntas_tema = perguntas[tema_escolhido]

    # Usuário escolhe quantas perguntas deseja responder
    qtd = escolher_quantidade(len(perguntas_tema))

    # Seleciona aleatoriamente as perguntas para o quiz
    perguntas_selecionadas = random.sample(perguntas_tema, qtd)

    # Limpa a tela e informa o tema escolhido
    limpar_tela()
    print(f"Quiz do tema: {tema_escolhido}\n")

    # Variável para contar os acertos
    acertos = 0

    # Inicia o loop das perguntas
    for i, pergunta in enumerate(perguntas_selecionadas, 1):
        # Mostra o número e texto da pergunta
        print(f"{i}. {pergunta['texto']}\n")

        # Exibe as alternativas (A, B, C, D)
        for idx, alt in enumerate(pergunta['alternativas']):
            print(f"  {chr(65+idx)}) {alt}")

        # Pede resposta até que uma válida seja digitada
        while True:
            resposta = input("\nResposta (A, B, C ou D): ").upper()
            if resposta in ["A", "B", "C", "D"]:
                break
            print("Resposta inválida, tente de novo.")

        # Verifica se a resposta está correta
        if resposta == pergunta['correta']:
            print("Resposta correta!\n")
            acertos += 1
            # Mostra o valor do prêmio acumulado
            print(f"Prêmio: R${acertos}00.000,00")
            canal_efeitos.play(som_certo)
            time.sleep(tempo)
            limpar_tela()
        else:
            # Se a resposta estiver errada, mostra a resposta correta
            print(f"Errado! Resposta correta: {pergunta['correta']}")
            print("Você errou, fim de jogo!\n")

            canal_efeitos.play(som_errado)
            time.sleep(tempo)
            canal_efeitos.play(som_risada)

            time.sleep(3)

            # Mostra quanto ele acumulou antes de errar
            print(f"Você perdeu: R${acertos}00.000,00")
            atualizar_ranking(nome, acertos)
            break

    # Se o jogador acertar todas as perguntas escolhidas, ele vence
    if acertos == qtd:
        # Aguarda um tempo antes de mostrar a tela final
        limpar_tela()

        if acertos == 10:
            print("PARABÉNS!!! 🎉🎉🎉")
            print("Você acertou o número máximo de perguntas, e ganhou o grande prêmio!!!")
            print(f"Prêmio máximo conquistado: R$1.000.000,00")

            som_milhao = pygame.mixer.Sound("efeitos sonoros/umMilhão.mp3")
            som_milhao.set_volume(1) 
            som_milhao.play()
            
            time.sleep(5)

        else:
            # Mostra mensagem de vitória e prêmio final
            print("PARABÉNS!!! 🎉🎉🎉")
            print("Você acertou todas as perguntas!")
            print(f"Prêmio conquistado: R${acertos}00.000,00")
        atualizar_ranking(nome, acertos)

# Início do programa
if __name__ == "__main__":
    main()
