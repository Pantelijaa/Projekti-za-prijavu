#include <stdbool.h>
#include <string.h>
#include <ctype.h>

bool isPalindrome(char* s) {
    char* r = s + strlen(s) - 1;
    char leftChar, rightChar;
    while (s < r) {
        if (!isalnum(*s)) {
            s++;
            continue;
        } else if (!isalnum(*r)) {
            r--;
            continue;
        }
        leftChar = tolower(*s);
        rightChar = tolower(*r);

        if (leftChar != rightChar) return false;
        s++;
        r--;
    }
    return true;
}


int main() {

    isPalindrome("A man, a plan, a canal: Panama");

    return 0;
}