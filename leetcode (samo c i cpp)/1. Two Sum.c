/**
 * Note: The returned array must be malloced, assume caller calls free().
 */
typedef struct {
    int key;
    int value;
    UT_hash_handle hh;
} hash_table;

hash_table *hash = NULL, *elem, *tmp;


int* twoSum(int* nums, int numsSize, int target, int* returnSize) {
    int k, i;
    int* result = calloc((*returnSize = 2), sizeof(int));

    if (sizeof(nums) < (sizeof(int)*2)) return result;
    
    for (i = 0; i < numsSize; i++) {
        k = target - nums[i];
        HASH_FIND_INT(hash, &k, elem); // look for element wehere key = k

        if (elem) {
            result[0] = elem->value;
            result[1] = i;
            break;
        } else {
            elem = malloc(sizeof(hash_table));
            elem->key = nums[i];
            elem->value = i;
            HASH_ADD_INT(hash, key, elem);
        }
    }
    HASH_ITER(hh, hash, elem, tmp) {
        HASH_DEL(hash, elem); free(elem);
    }
    return result;
}
