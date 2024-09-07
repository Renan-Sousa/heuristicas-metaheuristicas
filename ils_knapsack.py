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
        if random.choice([True, False]):  # Decide aleatoriamente se o item será incluído
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

# Busca Local para encontrar o otimo local com politica first improvement
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

# Causa uma pertubacao na solucao
def Pertubacao(solucao, itens, nItens, d, pesoMaximo):
    pert = solucao[:]
    for i in range(d):
        index = random.randint(0, nItens-1)
        pert[index] = 1 - pert[index]
        if calcular_peso_total(itens, pert, nItens) > pesoMaximo:
            # Só aceita a mudança caso não ultrapasse a capacidade
            pert[index] = 1 - pert[index]
    return pert
    
def ils(itens, solucao_inicial, nItens, pesoMaximo):
    melhor_solucao = BuscaLocal(itens, solucao_inicial,nItens, pesoMaximo)
    melhor_valor = calcular_lucro_total(itens, melhor_solucao, nItens)
    # mpeso = calcular_peso_total(itens, melhor_solucao, nItens)
    
    grafico.append(melhor_valor)
    print(melhor_valor)

    itera = 0
    ILSMax = int(0.9 * nItens) # permite mudar no máximo metade da solucão
    d = 1

    while itera < ILSMax:
        itera = itera + 1
    
        solucao_pertubada = Pertubacao(melhor_solucao, itens, nItens, d, pesoMaximo)
        nova_solucao = BuscaLocal(itens, solucao_pertubada, nItens, pesoMaximo)
    
        novo_valor = calcular_lucro_total(itens, nova_solucao, nItens)
        novoPeso = calcular_peso_total(itens, nova_solucao, nItens)
        # print(novoPeso)
        if novoPeso <= pesoMaximo and novo_valor > melhor_valor:
            print(novo_valor)
            grafico.append(novo_valor)
            melhor_solucao = nova_solucao
            melhor_valor = novo_valor
            itera = 0
            d = 1
        else:
            d = d + 1 # quando não encontra um solução melhor aumenta o número de alterações na solução

    return melhor_solucao

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

    solucao_inicial = solucao_inicial_aleatoria(itens, pesoMaximo, nItens)
   
    valor = calcular_lucro_total(itens, solucao_inicial, nItens)
    grafico.append(valor)
    print(valor)

    solucao_final = ils(itens, solucao_inicial, nItens, pesoMaximo)
    valorFinal = calcular_lucro_total(itens, solucao_final, nItens)
   
    soma = sum(grafico)
    n = len(grafico)
    media = soma / n

    print(f"{min(grafico)} & {max(grafico)} & {media:.2f}")
    
    # plt.plot(grafico, 'o-')  # 'o-' combina linhas com marcadores de círculo
    # plt.xticks([])  # Remove os números e rótulos do eixo x
    # plt.yticks([])  # Remove os números e rótulos do eixo x

    # # Adiciona o valor exato de cada ponto no gráfico
    # for i, valor in enumerate(grafico):
    #     plt.text(i, valor, str(valor), fontsize=9, ha='right', va='bottom')
    # plt.title('Evolução do Valor Total na Busca ILS')

    # plt.show()