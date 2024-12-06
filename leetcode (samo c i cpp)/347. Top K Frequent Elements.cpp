#include <iostream>
#include <vector>
#include <unordered_map>
using namespace std;

vector<int> topKFrequent(vector<int>& nums, int k) {
    unordered_map<int, int> count;
    vector<vector<int>> freq(nums.size() + 1); // Zbog nule
    vector<int> res;

    if (k == 0) return res;
                                            //  num: count
    for (int n : nums) count[n]++;  // count = {3: 2, 2: 2, 1: 3}

    for (const auto& i : count) {
        cout << i.first << " " << i.second << '\n';
    }
                                                                                        //  0   1     2     3
    for (const auto& entry : count) freq[entry.second].push_back(entry.first); // freq = [ [], [], [2, 3], [1]]

    for (int i = freq.size() - 1; i > 0; i--) {
        for (int n : freq[i]) {
            res.push_back(n);
            if (res.size() == k) {
                return res;
            }
        }
    }
    return res;
}
 
int main() {
    vector<int> test = {1, 1, 1,2 ,2 ,3, 3};
    int k = 2;

    vector<int> res = topKFrequent(test, k);
    cout << "[";
    for (const int i : res) {
        cout << i << ", "; 
    }
    cout << "]" << endl;
    return 0;
}