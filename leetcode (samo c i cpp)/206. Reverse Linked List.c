/**
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val;
 *     struct ListNode *next;
 * };
 */
#include <stdio.h>

struct ListNode* reverseList(struct ListNode* head) {
    struct ListNode* current = head;
    struct ListNode* next = NULL;
    struct ListNode* previous = NULL;
    while (current) {
        next = current->next;
        current->next = previous;
        previous = current;
        current = next;
    }
    return previous;
}