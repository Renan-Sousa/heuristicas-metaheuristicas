#include <iostream>
#include <fstream>
#include <vector>

using namespace std;

struct Item {
    int value;
    int weight;
    float ratio;
};

int calculateProfit(vector<Item>& items, vector<int>& solution) {
    int totalProfit = 0;
    for (int i = 0; i < items.size(); ++i) {
        if (solution[i]) {
            totalProfit += items[i].value;
        }
    }
    return totalProfit;
}

int calculateWeight(vector<Item>& items, vector<int>& solution) {
    int totalWeight = 0;
    for (int i = 0; i < items.size(); ++i) {
        if (solution[i]) {
            totalWeight += items[i].weight;
        }
    }
    return totalWeight;
}

void calculateRatios(int nItems, vector<Item> &items) {
    for (int i = 0; i < nItems; i++) {
        items[i].ratio = (float)items[i].value / (float)items[i].weight;
    }
}

vector<int> greedySearch(int nItems, int maxWeight, vector<Item> &items) {
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
    
    vector<int> solution = greedySearch(nItems, wMax, items);

    cout << "Solução Final: " << endl;
    for (int i = 0; i < nItems; i++) {
        cout << solution[i] << " ";
    }
    cout << endl;
    cout << endl;
    cout << "Peso Final: " << calculateWeight(items, solution) << endl;
    cout << "Valor Final: " << calculateProfit(items, solution) << endl;

    return 0;
}
