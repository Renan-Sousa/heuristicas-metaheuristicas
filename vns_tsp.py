import sys
import random
import math



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

def AlteraVizinhança(s, s1, k, cidades):
    distanciaS1 = calcular_distancia_total(cidades, s1)
    distS = calcular_distancia_total(cidades, s)
    if  distanciaS1 < distS:
        print(f"{distanciaS1:.1f}")
        s = s1
        k = 1
    else: 
        k = k+1
    return s, k

def VNS(cidades, rota):
    s = rota[:]

    VNSMax = 20
    k = 1

    while k < VNSMax:
        s1 = Pertubacao(s, k)
        s2 = BuscaLocal(cidades, s1)
        s, k = AlteraVizinhança(s, s2, k, cidades)
    return s

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
    s0 = rota_inicial_aleatoria(num_cidades)
    
    distanciaInicial = calcular_distancia_total(cidades, s0)
    print(f"{distanciaInicial:.2f}")
    sfinal = VNS(cidades, s0)
