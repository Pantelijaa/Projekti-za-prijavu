/**
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val;
 *     struct ListNode *next;
 * };
 */
struct ListNode {
    int val;
    struct ListNode *next;
}

struct ListNode* reverse(struct ListNode** head) {
    struct ListNode* curr = *head;
    struct ListNode* prev = NULL;
    struct ListNode* next = NULL;
    while (curr != NULL) {
        next = curr->next;
        curr->next = prev;
        prev = curr;
        curr = next;
    }
    return prev;
}
void reorderList(struct ListNode* head) {
    if (head == NULL) {
        return;
    }
    struct ListNode* reversedHead = reverse(&head);
    while ((head->next < reversedHead->next)) {
        ;
    }
}

int main() {

    reorderList();

    return 0;
}