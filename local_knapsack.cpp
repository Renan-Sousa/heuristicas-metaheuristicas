#include <iostream>
#include <vector>
#include <fstream>
#include <ctime> 

using namespace std;

struct Product {
    int profit;
    int weight;
};

int calculateProfit(vector<Product>& items, vector<bool>& solution) {
    int totalProfit = 0;
    for (int i = 0; i < items.size(); ++i) {
        if (solution[i]) {
            totalProfit += items[i].profit;
        }
    }
    return totalProfit;
}

int calculateWeight(vector<Product>& items, vector<bool>& solution) {
    int totalWeight = 0;
    for (int i = 0; i < items.size(); ++i) {
        if (solution[i]) {
            totalWeight += items[i].weight;
        }
    }
    return totalWeight;
}

vector<bool> createInicialSolution(int nItems, int wMax, vector<Product>& items) {
    vector<bool> solution(nItems);

    for (int i = 0; i < nItems; ++i) {
        solution[i] = rand() % 2; 
    }
    
    while (calculateWeight(items, solution) > wMax) {
        int index = rand() % nItems;
        solution[index] = false;
    }

    return solution;
}

void localSearch(vector<Product> items, int wMax, int iterations, vector<bool>& solution, int nItems) {
    int bestProfit = calculateProfit(items, solution);
    int index;

    for (int i = 0; i < iterations; i++) {
        index = rand() % nItems;
        solution[index] = !solution[index];

        if (calculateWeight(items, solution) <= wMax) {
            int newProfit = calculateProfit(items, solution);
            if (newProfit > bestProfit) {
                bestProfit = newProfit;
            }
        }
        else {
            solution[index] = !solution[index];
        }
    }
}

int main(int argc, char const *argv[]) {
    srand(time(0));
    
    string filename = argv[1];
    ifstream file(filename);

    file.is_open();

    int nItems, wMax;
    file >> nItems >> wMax;

    vector<Product> products;
    Product prod;

    for (int i = 0; i < nItems; i++) {
        file >> prod.profit >> prod.weight;
        products.push_back(prod);
    }
    
    file.close();
    
    /////////////////////////////////////////////////////////////////////////
    vector<bool> knapsack;
    knapsack = createInicialSolution(nItems, wMax, products);

    cout << "Solução Inicial: " << endl;
    for (int i = 0; i < knapsack.size(); ++i) {
        cout << knapsack[i] << " ";
    }
    cout << endl;
    cout << "Peso Inicial: " << calculateWeight(products, knapsack) << endl;
    cout << "Valor Inicial: " << calculateProfit(products, knapsack) << endl;
    
    /////////////////////////////////////////////////////////////////////////
    int iterations = 100;
    localSearch(products, wMax, iterations, knapsack, nItems);
    
    cout << endl;
    cout << "Solução Final: " << endl;
    for (int i = 0; i < knapsack.size(); ++i) {
        cout << knapsack[i] << " ";
    }
    cout << endl;
    cout << "Peso Final: " << calculateWeight(products, knapsack) << endl;
    cout << "Valor Final: " << calculateProfit(products, knapsack) << endl;

}
