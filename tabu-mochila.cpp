#include <iostream>
#include <fstream>
#include <vector>
#include <algorithm>
#include <limits>

using namespace std;

#define CRITERIO_PARADA 100

struct Item {
    int value;
    int weight;
    float ratio;
};

// Função para calculo do lucro total de uma solução
int calculateTotalProfit(vector<Item> &items, vector<int> &solution) {
    int totalProfit = 0;
    for (int i = 0; i < items.size(); ++i) {
        if (solution[i]) {
            totalProfit += items[i].value;
        }
    }
    return totalProfit;
}

// Função para calculo do peso total de uma solução 
int calculateTotalWeight(vector<Item> &items, vector<int> &solution) {
    int totalWeight = 0;
    for (int i = 0; i < items.size(); ++i) {
        if (solution[i]) {
            totalWeight += items[i].weight;
        }
    }
    return totalWeight;
}

// Função para calcular as proporções valor/peso de cada item em uma solução
void calculateRatios(int nItems, vector<Item> &items) {
    for (int i = 0; i < nItems; i++) {
        items[i].ratio = (float)items[i].value / (float)items[i].weight;
    }
}

int evaluate(int nItems, int maxWeight, vector<Item> &items, vector<int> &solution) {
    // Calcula o valor total dos itens selecionados
    int totalValue = calculateTotalProfit(items, solution);
    
    // Calcula o peso total dos itens selecionados
    int totalWeight = calculateTotalWeight(items, solution);

    // Calcula o excesso de carga
    int excessWeight = max(0, totalWeight - maxWeight);

    // Calcula a penalidade (soma de todos os items)
    vector<int> all(nItems, 1);
    int maxProfit = calculateTotalProfit(items, all);
    int penalty =  maxProfit * excessWeight;

    // Retorna o valor total da penalidade
    return totalValue - penalty;
}


// Função para solução inicial usando método guloso
vector<int> inicialSolution(int nItems, int maxWeight, vector<Item> &items) {
    vector<int> solution(nItems, 0);
    vector<bool> chosen(nItems, false);
    calculateRatios(nItems, items);
    int currentWeight = 0;

    while (currentWeight < maxWeight) {
        float maxRatio = 0.0;
        int bestItem = -1;

        for (int i = 0; i < nItems; i++) {
            if (!chosen[i] && items[i].ratio > maxRatio) {
                maxRatio = items[i].ratio;
                bestItem = i;
            }
        }

        if (bestItem == -1 || currentWeight + items[bestItem].weight > maxWeight) {
            break;
        }

        currentWeight += items[bestItem].weight;
        solution[bestItem] = 1; 
        chosen[bestItem] = true;
    }

    return solution;
}

// Função da Busca Tabu
vector<int> tabuSearch(int nItems, int maxWeight, vector<Item> &items, vector<int> &inicial_solution) {
    vector<int> solution = inicial_solution;
    vector<int> bestSolution = inicial_solution;
    vector<int> tabuList(nItems, 0);
    vector<int> neighbor;

    int bestEvaluation = evaluate(nItems, maxWeight, items, bestSolution);
    int iter = 0;
    int tabu_duration = 2;

    while (iter < CRITERIO_PARADA) {
        iter++;
        vector<int> evaluations;     
        int i;
        for (i = 0; i < nItems; i++) {
            neighbor = solution;
            neighbor[i] = 1 - neighbor[i];
            int a =  evaluate(nItems, maxWeight, items, neighbor);
            evaluations.push_back(a);
        }

        int first = 1;
        int bestNeighborIndex;
        int bestNeighborEvaluation;

        for (i = 0; i < nItems; i++) {
            if(tabuList[i] == 0) {
                if(first == 1) {
                    first = 0;
                    bestNeighborIndex = i;
                    bestNeighborEvaluation = evaluations[i];
                } else {
                    if (evaluations[i] > bestNeighborEvaluation) {
                        bestNeighborEvaluation = evaluations[i];
                        bestNeighborIndex = i;
                    }
                }
            }
        }

        // Diminui a espera na lista tabu
        for (int i = 0; i < nItems; i++) {
            if(tabuList[i] > 0) {
                tabuList[i]--;
            }
        }
        
        // Adiciona a melhor solução entre os vizinhos na lista tabu
        tabuList[bestNeighborIndex] = tabu_duration;

        // Melhor Solução entre os vizinhos 
        solution[bestNeighborIndex] = 1 - solution[bestNeighborIndex];

        // Melhor Solução Geral
        if(evaluate(nItems, maxWeight, items, solution) > bestEvaluation) {
            bestSolution = solution;
        }
    }    

    return bestSolution;
}

int main(int argc, char const *argv[]) {
    string filename = argv[1];
    ifstream file(filename);

    file.is_open();

    int nItems, wMax;
    file >> nItems >> wMax;

    vector<Item> items;
    Item product;

    for (int i = 0; i < nItems; i++) {
        file >> product.value >> product.weight;
        items.push_back(product);
    }
    
    file.close();
    
    // vector<int> inicial_solution = {1, 0, 0, 1, 0, 1, 1, 0};
    vector<int> inicial_solution = inicialSolution(nItems, wMax, items);
    vector<int> final_solution = tabuSearch(nItems, wMax, items, inicial_solution);
    
    // Imprime os resultados iniciais do algoritmo
    cout << "Solução Inicial: " << endl;
    for (int i = 0; i < nItems; i++) {
        cout << inicial_solution[i] << " ";
    }
    cout << endl; 
    cout << "Peso Inicial: " << calculateTotalWeight(items, inicial_solution) << endl;
    cout << "Valor Inicial: " << calculateTotalProfit(items, inicial_solution) << endl;
    cout << "Função Objetivo: " <<  evaluate(nItems, wMax, items, inicial_solution) << endl;

    // Imprime os resultados Finais do algoritmo
    cout << endl; 
    cout << "Solução Final: " << endl;
    for (int i = 0; i < nItems; i++) {
        cout << final_solution[i] << " ";
    }

    cout << endl; 
    cout << "Peso Final: " << calculateTotalWeight(items, final_solution) << endl;
    cout << "Valor Final: " << calculateTotalProfit(items, final_solution) << endl;
    cout << "Função Objetivo: " <<  evaluate(nItems, wMax, items, final_solution) << endl;

    return 0;
}