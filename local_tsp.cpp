#include <iostream>
#include <vector>
#include <fstream>
#include <math.h>
#include <algorithm>
#include <random>

using namespace std;

typedef struct city {
    int id;
    int coord_x;
    int coord_y;
} City;

void printPath(int numCities, vector<int> path)  {
    for (int i = 0; i < numCities; i++) {
        cout << path[i] << " ";
    }
    cout << endl;
}

vector<int> createInicialSolution(int numCities) {
    vector<int> solution;

    for (int i = 0; i < numCities; ++i) {
        solution.push_back(i+1);
    }

    random_device rd;
    mt19937 gen(rd());
    shuffle(solution.begin(), solution.end(), gen);
    
    return solution;
}

int evaluate(int numCities, vector<int> path, vector<City> cities) {
    int totalDistance = 0;
    int city_1, city_2, dist, xd, yd;

    for (int i = 0; i < numCities-1 ; i++) {
        city_1 = path[i]-1;
        city_2 = path[i+1]-1;
        
        xd = cities[city_1].coord_x - cities[city_2].coord_x; 
        yd = cities[city_1].coord_y - cities[city_2].coord_y;
        dist = (int) (sqrt( xd*xd + yd*yd) ); 
        
        totalDistance = totalDistance + dist;
    }
    
    return totalDistance; 
}

void Swap(vector<int>& path, int i, int k) {
    int aux = path[i];
    path[i] = path[k];
    path[k] = aux;
}

void localSearch(int numCities, vector<int> path, vector<City> cities) {
    int bestDistance = evaluate(numCities, path, cities);
    cout << "Distância inicial: "<< bestDistance << endl;

    int i = 0;
    int k = numCities;
    int newDist;
    while (i < k) {
        Swap(path, i, k);
        newDist = evaluate(numCities, path, cities);
        if(newDist < bestDistance)
            bestDistance = newDist;
        else
            Swap(path, i, k);

        i++; k--;
    }

    //printPath(numCities, path);
    cout << "Distância final: "<< bestDistance << endl;
}

int main(int argc, char const *argv[]) {

    string filename = argv[1];
    ifstream file(filename);
    string ignore;

    file.is_open();

    for (int i = 0; i < 6; ++i)
        getline(file, ignore);


    vector<City> cities;
    City ct;
    int numCity = 0;

    while (file >> ct.id >> ct.coord_x >> ct.coord_y) {    
        cities.push_back(ct);
        numCity++;
    }

    file.close();
    
    vector<int> inicialpath = createInicialSolution(numCity);
 
    cout << "SOLUÇÃO INICIAL" << endl;
    printPath(numCity, inicialpath);

    localSearch(numCity, inicialpath, cities);

    return 0;
}
