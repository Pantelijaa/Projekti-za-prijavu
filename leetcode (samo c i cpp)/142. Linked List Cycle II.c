/**
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val;
 *     struct ListNode *next;
 * };
 */

struct ListNode* findPos(struct ListNode *head,struct ListNode *slow) {
    while (head != slow) {
        head = head->next;
        slow = slow->next;
    }
    return head;
}

struct ListNode *detectCycle(struct ListNode *head) {
    struct ListNode* slow = head;
    struct ListNode* fast = head;

    while (fast && fast->next) {
        slow = slow->next;
        fast = fast->next->next;
        if (slow == fast) return findPos(head, slow);
    }
    return NULL;
}
/*
 ILI AKO MORA DA SE VRATI TACNA ADRESA U ULAZNOJ LISTI:
*/
/*
struct ListNode* findPos(struct ListNode **head,struct ListNode **slow) {
    while (*head != *slow) {
        head = &((*head)->next);
        slow = &((*slow)->next);
    }
    return *head;
}

struct ListNode *detectCycle(struct ListNode *head) {
    struct ListNode* slow = head;
    struct ListNode* fast = head;

    while (fast && fast->next) {
        slow = slow->next;
        fast = fast->next->next;
        if (slow == fast) return findPos(&head, &slow);
    }
    return NULL;
}
*/