/**
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val;
 *     struct ListNode *next;
 * };
 */
bool recursiveTraverse(struct ListNode* slow, struct ListNode* fast) {
    if (fast == NULL || fast->next == NULL) return false;
    if (fast == slow) return true;
    return recursiveTraverse(slow->next, fast->next->next);
}
bool hasCycle(struct ListNode *head) {
    if (head == NULL) return false;
    return recursiveTraverse(head, head->next);
}