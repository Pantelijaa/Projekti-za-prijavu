class Solution {
public:
    vector<vector<string>> groupAnagrams(vector<string>& strs) {
        unordered_map<string, vector<string>> res;
        vector<vector<string>> result;
        for (const string& s : strs) {
            vector<int> counters(26, 0);
            for (const char& c : s) counters[c - 'a']++;

            string key = to_string(counters[0]);
            for (int i = 1; i < 26; i++) key += ',' + to_string(counters[i]);
            // anagrami ce imati isti key
            res[key].push_back(s);
        }

        for (const auto& pair : res) result.push_back(pair.second);

        return result;
    }
};