#include <stdbool.h>
bool isAnagram(char* s, char* t) {
    int hashmap[26] = {0};
    int i = 0;

    while (s[i]) hashmap[s[i++] - 'a']++;
    i = 0;
    while (t[i]) hashmap[s[i++] - 'a']--;

    for (i = 0; i < 26; i++) {
        if (hashmap[i] != 0) return false;
    }
    return true;
}