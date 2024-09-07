import sys
import random
import math

class Cidade:
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y

def distancia(cidadeA, cidadeB):
    return math.sqrt((cidadeA.x - cidadeB.x) ** 2 + (cidadeA.y - cidadeB.y) ** 2)

# Calcula a distância total de uma rota
def calcular_distancia_total(cidades, rota):
    distancia_total = 0  
    num_cidades = len(rota)
    for i in range(num_cidades - 1):
        distancia_total += distancia(cidades[rota[i]], cidades[rota[i+1]])
    # Adiciona a distância do último para o primeiro
    distancia_total += distancia(cidades[rota[-1]], cidades[rota[0]])
    return distancia_total

# Gera uma solução inicial aleatória
def rota_inicial_aleatoria(num_cidades):
    rota = list(range(num_cidades))
    random.shuffle(rota)
    return rota

# Gera vizinhos utilizando o método 2-opt
def vizinhanca_2opt(rota):
    vizinhos = []
    num_cidades = len(rota)
    for i in range(num_cidades - 1):
        for j in range(i + 2, num_cidades):
            if i == 0 and j == num_cidades - 1:
                continue
            nova_rota = rota[:]
            nova_rota[i:j+1] = reversed(nova_rota[i:j+1])
            vizinhos.append(nova_rota)
    return vizinhos

def f(rota, cidades):
    return calcular_distancia_total(cidades, rota)

def simulated_annealing(solucao_inicial, cidades):
    solucao_atual = solucao_inicial
    melhor_solucao = solucao_inicial
    pior_solucao = solucao_inicial

    temperatura = 5000 
    temperatura_final = 0.001
    alpha = 0.9
    iter_temp = 50  
    iter = 0

    # Calcula o custo inicial da solução
    custo_atual = f(solucao_atual, cidades)
    melhor_custo = custo_atual
    pior_custo = custo_atual

    while temperatura > temperatura_final:  # Enquanto a temperatura for maior que a final
        
        while iter < iter_temp:
            iter += 1
            vizinhos = vizinhanca_2opt(solucao_atual)
            vizinho_aleatorio = random.choice(vizinhos)
            
            custo_vizinho = f(vizinho_aleatorio, cidades)
    
            if custo_vizinho < melhor_custo:
                melhor_custo = custo_vizinho
                melhor_solucao = vizinho_aleatorio
            
            if custo_vizinho > pior_custo:
                pior_custo = custo_vizinho
                pior_solucao = vizinho_aleatorio

            if custo_vizinho < custo_atual:
                solucao_atual = vizinho_aleatorio
                custo_atual = custo_vizinho
            else:
                delta = custo_vizinho - custo_atual  
                probabilidade = random.uniform(0, 1)
                funcao_prob = math.exp(-delta / temperatura)
                if probabilidade < funcao_prob:
                    solucao_atual = vizinho_aleatorio
                    custo_atual = custo_vizinho

        temperatura *= alpha  # Resfriamento
        iter = 0
    
    return melhor_solucao, pior_solucao, melhor_custo, pior_custo

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
    melhor_rota, pior_rota, melhor_custo, pior_custo = simulated_annealing(rota_inicial, cidades)

    # Formatando a saída com duas casas decimais
    print(f'Distância Total Inicial: {calcular_distancia_total(cidades, rota_inicial):.2f}')
    print(f'Distância Melhor Rota: {melhor_custo:.2f}')
    print(f'Distância Pior Rota: {pior_custo:.2f}')
