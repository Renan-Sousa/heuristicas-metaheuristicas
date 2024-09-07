import sys
import random
import math
import matplotlib.pyplot as plt

grafico = []

class Item:
    def __init__(self, valor, peso):
        self.valor = valor
        self.peso = peso
 
# Gera uma solução inicial aleatória
def solucao_inicial_aleatoria(itens, pesoMaximo, nItens):
    solucao = [0] * nItens # Inicializa a solução como uma lista de 0s
    peso_atual = 0

    for i in range(nItens):
        if random.choice([True, False]):  #Decide aleatoriamente se o item será incluído
            if peso_atual + itens[i].peso <= pesoMaximo:  # Verifica se o item cabe na mochila
                solucao[i] = 1
                peso_atual += itens[i].peso

    return solucao

# Calcula o lucro total da solução
def calcular_lucro_total(itens, solucao, nItens):
    lucro_total = 0
    for i in range(nItens):
        if solucao[i]:
            lucro_total += itens[i].valor
    return lucro_total

# Calcula o peso total da solução
def calcular_peso_total(itens, solucao, nItens):
    peso_total = 0
    for i in range(nItens):
        if solucao[i]:
            peso_total += itens[i].peso
    return peso_total

def BuscaLocal(itens, solucao_inicial, nItens, pesoMaximo):
    melhor_solucao = solucao_inicial[:]
    melhor_valor = calcular_lucro_total(itens, melhor_solucao, nItens)

    melhorou = True
    while melhorou:
        melhorou = False
        vizinho = melhor_solucao[:]   
        
        for i in range(nItens):
            vizinho[i] = 1 - vizinho[i]  
            peso_vizinho = calcular_peso_total(itens, vizinho, nItens)
            valor_vizinho = calcular_lucro_total(itens, vizinho, nItens)
            
            if peso_vizinho <= pesoMaximo and valor_vizinho >= melhor_valor:
                melhorou = True
                melhor_solucao = vizinho 
                melhor_valor = valor_vizinho
                break # First Improvement(ao encontrar uma solução melhor para a busca naquela vizinhança)
            
    return melhor_solucao

def EncontrarIndiceMelhorCustoBeneficio(itens, nItens):
    melhorCB = 0
    for i in range(nItens):
        cb = itens[i].valor / itens[i].peso
        if cb > melhorCB:
            indice = i
            melhorCB = cb
    return indice

def ConstrucaoGulosaAleatoria(itens, nItens, pesoMaximo, alpha):
    solucao = [0] * nItens # inicia a solucao sem nenhum item
    
    #comeca com o item de melhor custo beneficio
    index = EncontrarIndiceMelhorCustoBeneficio(itens, nItens)
    solucao[index] = 1
    
    while True:
        lc = []
        for indice in range(nItens):
            if solucao[indice] == 0:
                solucao[indice] = 1
                novoPeso = calcular_peso_total(itens, solucao, nItens)
                if novoPeso < pesoMaximo:
                    lc.append(indice)
                solucao[indice] = 0
        if lc:
            gc = []
            gc_indices = []
            for i in lc:
                cb = itens[i].valor / itens[i].peso 
                gc.append(cb)
                gc_indices.append(i)

            c_min = min(gc)
            c_max = max(gc)
            valor = c_min + alpha * (c_max - c_min)

            lrc = []
            for k in range(len(gc)):
                if(gc[k] <= valor):
                    indi = gc_indices[k]
                    lrc.append(indi)
                
            ind = random.choice(lrc)
            solucao[ind] = 1
        else:
            break
    
    return solucao
    
    

def grasp(itens, solucao_inicial, nItens, pesoMaximo):
    melhor_solucao = solucao_inicial[:]
    melhor_valor = calcular_lucro_total(itens, melhor_solucao, nItens)
    print(melhor_valor)
    grafico.append(melhor_valor)
    #Parâmetros do grasp
    GRASPMax = 100
    alpha = 0.8
    
    itera = 0

    while itera < GRASPMax:
        solucao_atual = ConstrucaoGulosaAleatoria(itens, nItens, pesoMaximo, alpha)
        solucao_atual = BuscaLocal(itens, solucao_atual, nItens, pesoMaximo)
        # print(solucao_atual)
       
        valor_atual = calcular_lucro_total(itens, solucao_atual, nItens)

        if  valor_atual > melhor_valor:
            print(valor_atual)
            grafico.append(valor_atual)
            melhor_solucao = solucao_atual
            melhor_valor = valor_atual
        
        itera += 1

    return melhor_solucao

if __name__ == "__main__":
    nome_arquivo = sys.argv[1]
    arquivo = open(nome_arquivo, 'r')
    
    # Primeira linha do arquivo: número de itens e capacidade da mochila
    nItens, pesoMaximo = map(int, arquivo.readline().split())

    # Leitura dos itens
    itens = []
    for _ in range(nItens):
        valor, peso = map(int, arquivo.readline().split())
        itens.append(Item(valor, peso))
    arquivo.close()

    solucao_inicial = solucao_inicial_aleatoria(itens, pesoMaximo, nItens)
    solucao_final = grasp(itens, solucao_inicial, nItens, pesoMaximo)

    soma = sum(grafico)
    n = len(grafico)
    media = soma / n

    print(f"{min(grafico)} & {max(grafico)} & {media:.2f}")

    # plt.plot(grafico, 'o-')  # 'o-' combina linhas com marcadores de círculo
    # plt.xticks([])  # Remove os números e rótulos do eixo x
    # plt.yticks([])  # Remove os números e rótulos do eixo y

    # # Adiciona o valor exato de cada ponto no gráfico com duas casas decimais
    # for i, valor in enumerate(grafico):
    #     plt.text(i, valor, f'{valor:.2f}', fontsize=9, ha='right', va='bottom')

    # plt.title('Evolução da distância no TSP')
    # plt.show()