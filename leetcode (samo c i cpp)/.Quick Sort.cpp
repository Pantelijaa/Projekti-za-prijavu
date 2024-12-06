#include <vector>
#include <iostream>

int partition(std::vector<int>& myArray, int low, int high) {
    int pivot = myArray[low];
    int i = low - 1;
    int j = high + 1;

    while (true) {
        do {
            i++;
        } while (myArray[i] < pivot);

        do {
            j--;
        } while (myArray[j] > pivot); 


        if (i >= j) {
            return j;
        }
        std::swap(myArray[i], myArray[j]);

    }    
}

void quickSort(std::vector<int>& myArray, int low, int high) {
    if (low < high) {
        int p = partition(myArray, low, high);

        quickSort(myArray, low, p);
        quickSort(myArray, p + 1, high);
    }
}

int main() {

    std::vector<int> myArray = {20, 12 , 123, 52, 2, 10 ,6};
    int arrayLenght = myArray.size();

    quickSort(myArray, 0, arrayLenght - 1);

    for (const int& i : myArray) {
        std::cout << i << " ";
    }
    std::cout << std::endl;

    return 0;
}