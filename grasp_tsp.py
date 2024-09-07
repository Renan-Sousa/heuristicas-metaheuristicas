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

def ConstrucaoGulosaAleatoria(cidades, alpha):
    solucao = [1]
    
    iter = 0
    max_iter = len(cidades) - 1
    
    while iter < max_iter:
        iter += 1 
        lc = [cidade for cidade in cidades if cidade.id not in solucao]

        gc = []
        for i in range(len(lc)):
            gc.append((distancia(cidades[solucao[-1]-1], lc[i]), lc[i].id))

        c_min = min(gc, key=lambda x: x[0])
        c_max = max(gc, key=lambda x: x[0])
        valor = c_min[0] + alpha * (c_max[0] - c_min[0])

        lrc = []
        for k in range(len(lc)):
            if(gc[k][0] <= valor):
                lrc.append(gc[k])
        
        escolha = random.choice(lrc)
        solucao.append(cidades[escolha[1]-1].id)

    return solucao

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

def grasp(cidades):
    melhor_distancia = 100000000

    #Parâmetros do grasp
    GRASPMax = 100
    alpha = 0.8
    
    iter = 0

    while iter < GRASPMax:
        solucao_atual = ConstrucaoGulosaAleatoria(cidades, alpha)
        solucao_atual = BuscaLocal(cidades, solucao_atual)
        distanciaAtual = calcular_distancia_total(cidades, solucao_atual)

        if  distanciaAtual < melhor_distancia:
            print(distanciaAtual)
            grafico.append(distanciaAtual)
            melhor_solucao = solucao_atual
            melhor_distancia = distanciaAtual
        
        iter += 1

    return melhor_solucao, melhor_distancia

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

    rota, distancia = grasp(cidades)
    # print(f'Rota: {rota}')
    print(f'Melhor distância rota: {distancia:.2f}')


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