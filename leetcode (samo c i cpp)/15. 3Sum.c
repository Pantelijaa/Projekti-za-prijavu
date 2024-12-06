/**
 * Return an array of arrays of size *returnSize.
 * The sizes of the arrays are returned as *returnColumnSizes array.
 * Note: Both returned array and *columnSizes array must be malloced, assume caller calls free().
 */
#include <stdlib.h>

int cmpfunc (const void * a, const void * b) {
   return ( *(int*)a - *(int*)b );
}

int** threeSum(int* nums, int numsSize, int* returnSize, int** returnColumnSizes) {
    int cap = 8;
    int** result = (int**)malloc(sizeof(int*) * cap);
    int* columns = (int*)malloc(sizeof(int) * cap);
    int* triple;
    int i, left, right;
    int sum, count, target;

    qsort(nums, numsSize, sizeof(int), cmpfunc);

    count = 0;
    
    for (i = 0; i < numsSize - 2; i++) {
        if (nums[i] > 0) break;
        if (i > 0 && nums[i] == nums[i - 1]) continue;

        target = 0 - nums[i];
        left = i + 1;
        right = numsSize - 1;
        while (left < right) {
            sum = nums[left] + nums[right];
            if (sum == target) {
                triple = (int*)malloc(sizeof(int) * 3);
                triple[0] = nums[i];
                triple[1] = nums[left];
                triple[2] = nums[right];

                result[count] = triple;
                columns[count] = 3;
                count++;

                if (count == cap) {
                    cap *= 2;
                    result = (int**)realloc(result, sizeof(int*) * cap);
                    columns = (int*)realloc(columns, sizeof(int) * cap);
                }                
            }
            left++;
            right--;

            while (left < right && nums[left] == nums[left - 1]) left++;
            while (left < right && nums[right] == nums [right + 1]) right++;
        }

    }
    *returnSize = count;
    *returnColumnSizes = columns;

    return result;
}

int main() {
    int nums[6] = {-1,0,1,2,-1,-4};
    int size = 6;
    int *returnSize, **returnColumnSizes;

    threeSum(nums, size, returnSize, returnColumnSizes);

    return 0;
}