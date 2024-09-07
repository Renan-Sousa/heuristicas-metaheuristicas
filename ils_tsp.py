import sys
import random
import math

import matplotlib.pyplot as plt
grafico = []

class Cidade:
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y

# Calcula a distancia de uma cidade a outra
def distancia(cidadeA, cidadeB):
    return math.sqrt((cidadeA.x - cidadeB.x) ** 2 + (cidadeA.y - cidadeB.y) ** 2)

# Calcula a distância total de uma rota
def calcular_distancia_total(cidades, rota):
    distancia_total = 0  
    num_cidades = len(rota)
    for i in range(num_cidades - 1):
        distancia_total += distancia(cidades[rota[i]-1], cidades[rota[i+1]-1])
    # Adiciona a distância do último para o primeiro
    distancia_total += distancia(cidades[rota[-1]-1], cidades[rota[0]-1])  
    return distancia_total

def rota_inicial_aleatoria(num_cidades):
    rota = list(range(num_cidades))
    random.shuffle(rota)
    return rota

def BuscaLocal(cidades, rota):
    melhor_solucao = rota[:]
    melhor_distancia = calcular_distancia_total(cidades, melhor_solucao)

    melhorou = True
    while melhorou:
        melhorou = False
        for i in range(1, len(rota) - 1):
            for j in range(i + 1, len(rota)):
                vizinho = melhor_solucao[:]
                vizinho[i], vizinho[j] = vizinho[j], vizinho[i]

                distancia_vizinho = calcular_distancia_total(cidades, vizinho)

                if distancia_vizinho < melhor_distancia:
                    melhor_solucao = vizinho[:]
                    melhor_distancia = distancia_vizinho
                    melhorou = True
    return melhor_solucao

def Pertubacao(rota, d):
    solucao = rota[:]
    n = len(solucao)
    for i in range(d):
        # vai selecionar duas cidades aleatórias para mudar de posição
        i, j = random.sample(range(n), 2)
        solucao[i], solucao[j] = solucao[j], solucao[i] 
    return solucao

def isl(cidades, rota_inicial, num_cidades):
    solucao_inicial = rota_inicial[:]
    melhor_solucao = BuscaLocal(cidades, solucao_inicial)
    melhor_distancia = calcular_distancia_total(cidades, melhor_solucao)
    grafico.append(melhor_distancia)
    print(f'{melhor_distancia:.2f}')
    
    itera = 0
    ILSMax = int(0.3 * num_cidades) 
    d = 1

    while itera < ILSMax:
        itera = itera + 1
        solucao_pertubada = Pertubacao(melhor_solucao, d)
        nova_solucao = BuscaLocal(cidades, solucao_pertubada)
        nova_distancia = calcular_distancia_total(cidades, nova_solucao)

        if nova_distancia < melhor_distancia:
            print(f'{nova_distancia:.2f}')
            grafico.append(nova_distancia)
            melhor_solucao = nova_solucao
            melhor_distancia = nova_distancia
            itera = 0
            d = 1
        else:
            d = d + 1 # quando não encontra um solução melhor aumenta o número de alterações na solução

    return melhor_solucao

# Execução principal do programa
if __name__ == "__main__":
    nome_arquivo = sys.argv[1]
    
    with open(nome_arquivo, 'r') as arquivo:
        # Ignora as linhas iniciais até encontrar 'NODE_COORD_SECTION'
        ler = False
        cidades = []
        
        for linha in arquivo:
            linha = linha.strip()
            if linha == "NODE_COORD_SECTION":
                ler = True
                continue
            if linha == "EOF":
                break
            if ler:
                id, x, y = map(float, linha.split())
                cidades.append(Cidade(int(id), x, y))
    
    num_cidades = len(cidades)
    
    rota_inicial = rota_inicial_aleatoria(num_cidades)
    dist = calcular_distancia_total(cidades, rota_inicial)
    grafico.append(dist)

    print(f'{dist:.2f}')
    solucao_final = isl(cidades, rota_inicial, num_cidades)


    soma = sum(grafico)
    n = len(grafico)
    media = soma / n

    print(f"{max(grafico):.2f} & {min(grafico):.2f} & {media:.2f}")

    # plt.plot(grafico, 'o-')  # 'o-' combina linhas com marcadores de círculo
    # plt.xticks([])  # Remove os números e rótulos do eixo x
    # plt.yticks([])  # Remove os números e rótulos do eixo y

    # # Adiciona o valor exato de cada ponto no gráfico com duas casas decimais
    # for i, valor in enumerate(grafico):
    #     plt.text(i, valor, f'{valor:.2f}', fontsize=9, ha='right', va='bottom')

    # plt.title('Evolução da distância no TSP')
    # plt.show()
    