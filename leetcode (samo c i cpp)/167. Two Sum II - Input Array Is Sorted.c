/**
 * Note: The returned array must be malloced, assume caller calls free().
 */
#include <stdbool.h>

int* twoSum(int* numbers, int numbersSize, int target, int* returnSize) {
    *returnSize = 2;
    int* result = malloc(sizeof(int) * 2);
    int total;
    int left = 0;
    int right = numbersSize - 1;
    while (true) {
        total = numbers[left] + numbers[right];
        if (total == target) {
            result[0] = left + 1;
            result[1] = right + 1;
            return result;
        } else if (total > target) {
            right--;
        } else {
            left++;
        }
    }
}