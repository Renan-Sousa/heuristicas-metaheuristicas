import sys
import random
import math

class Item:
    def __init__(self, valor, peso):
        self.valor = valor
        self.peso = peso
        self.cb = valor / peso if peso != 0 else 0  # Custo/Benefício do item

# Gera uma solução inicial aleatória
def solucao_inicial_aleatoria(itens, pesoMaximo):
    solucao = [0] * len(itens)  # Inicializa a solução como uma lista de 0s
    peso_atual = 0

    for i in range(len(itens)):
        if random.choice([True, False]):  # Decide aleatoriamente se o item será incluído
            if peso_atual + itens[i].peso <= pesoMaximo:  # Verifica se o item cabe na mochila
                solucao[i] = 1
                peso_atual += itens[i].peso

    return solucao

# Calcula o lucro total da solução
def calcular_lucro_total(itens, solucao):
    lucro_total = 0
    for i in range(len(itens)):
        if solucao[i]:
            lucro_total += itens[i].valor
    return lucro_total

# Calcula o peso total da solução
def calcular_peso_total(itens, solucao):
    peso_total = 0
    for i in range(len(itens)):
        if solucao[i]:
            peso_total += itens[i].peso
    return peso_total

# Gera vizinhos da solução atual trocando a inclusão/exclusão de cada item
def vizinhanca_flip(solucao, itens, pesoMaximo):
    vizinhos = []
    for i in range(len(solucao)):
        vizinho = solucao[:]
        vizinho[i] = 1 - vizinho[i]  # Troca o estado do item (incluir/excluir)
        if calcular_peso_total(itens, vizinho) <= pesoMaximo:  # Verifica se o peso não excede o máximo
            vizinhos.append(vizinho)
    return vizinhos

# Função objetivo: retorna o valor total da solução
def f(solucao, itens, pesoMaximo):
    valor = calcular_lucro_total(itens, solucao)
    return valor

# Algoritmo de Simulated Annealing
def simulated_annealing(solucao_inicial, itens, pesoMaximo):
    solucao_atual = solucao_inicial
    melhor_solucao = solucao_inicial
    pior_solucao = solucao_inicial
    
    temperatura = 5000  # Temperatura inicial
    temperatura_final = 0.001  # Temperatura final
    alpha = 0.95  # Taxa de resfriamento
    iter_temp = 100  # Número de iterações por temperatura
    iter = 0

    while temperatura > temperatura_final:  # Enquanto a temperatura for maior que a final
        
        while iter < iter_temp:
            iter += 1
            vizinhos = vizinhanca_flip(solucao_atual, itens, pesoMaximo)
            vizinho_aleatorio = random.choice(vizinhos)
            
            fitness_atual = f(solucao_atual, itens, pesoMaximo)
            fitness_vizinho = f(vizinho_aleatorio, itens, pesoMaximo)
            fitness_melhor_solucao = f(melhor_solucao, itens, pesoMaximo)
            fitness_pior_solucao = f(pior_solucao, itens, pesoMaximo)
    
            if fitness_vizinho > fitness_atual:
                solucao_atual = vizinho_aleatorio
                if fitness_vizinho > fitness_melhor_solucao:
                    melhor_solucao = solucao_atual
            else:
                if fitness_vizinho < fitness_pior_solucao:
                    pior_solucao = vizinho_aleatorio
                
                delta = fitness_vizinho - fitness_atual  
                probabilidade = random.uniform(0, 1)
                funcao_prob = math.exp(delta / temperatura)
                if probabilidade < funcao_prob:
                    solucao_atual = vizinho_aleatorio

        temperatura *= alpha  # Resfriamento
        iter = 0
    
    return melhor_solucao, pior_solucao

# Execução principal do programa
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

    # Gera uma solução inicial aleatória e aplica o algoritmo de Simulated Annealing
    solucao_inicial = solucao_inicial_aleatoria(itens, pesoMaximo)
    melhor_solucao, pior_solucao = simulated_annealing(solucao_inicial, itens, pesoMaximo)

    # Impressão dos resultados
    print(f"Peso Inicial: {calcular_peso_total(itens, solucao_inicial)} | Valor Inicial: {calcular_lucro_total(itens, solucao_inicial)}")
    print(f"Melhor Peso Final: {calcular_peso_total(itens, melhor_solucao)} | Melhor Valor Final: {calcular_lucro_total(itens, melhor_solucao)}")
    print(f"Pior Peso Final: {calcular_peso_total(itens, pior_solucao)} | Pior Valor Final: {calcular_lucro_total(itens, pior_solucao)}")
