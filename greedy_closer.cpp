#include <iostream>
#include <vector>
#include <fstream>
#include <math.h>

using namespace std;

typedef struct city {
    int id;
    int coord_x;
    int coord_y;
} City;

int distance(City cityI, City cityA) {
    int xd = cityI.coord_x - cityA.coord_x;
    int yd = cityI.coord_y - cityA.coord_y;
    int dist = (int)(sqrt(xd * xd + yd * yd));
    return dist;
}

int closerCity(int numCities, vector<City>& cities, vector<int>& path) {
    vector<bool> visited(numCities, false);
    int totalDistance = 0;
    int inicialCity = 0;
    path.push_back(1);
    visited[inicialCity] = true;

    for(int i = 0; i < numCities - 1; i++) {
        int nextCity = -1;
        int minDist = 99999999;

        for (int i = 0; i < numCities; i++) {
            if (!visited[i] && i != inicialCity) {
                int dist = distance(cities[inicialCity], cities[i]);

                if (dist < minDist) {
                    minDist = dist;
                    nextCity = i;
                }
            }
        }

        if (nextCity != -1) {
            totalDistance += minDist;
            path.push_back(nextCity + 1);
            visited[nextCity] = true;
            inicialCity = nextCity;
        }
    }

    totalDistance += distance(cities[path.back() - 1], cities[0]);

    return totalDistance;
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
    
    vector<int> path;
    int minDistance = closerCity(numCity, cities, path);

    cout << "Distancia Minima: " << minDistance << endl;
    
    return 0;
}