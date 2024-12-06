#include <stdlib.h>
#include <stdbool.h>

struct ListNode {
    int val;
    struct ListNode* next;
};

void insertAtEnd(struct ListNode** head, int val)
{
    struct ListNode* newNode = (struct ListNode*)malloc(sizeof(struct ListNode));
    // store the val in the new ListNode
    newNode->val = val;
    // Since the node will be last its next will be NULL
    newNode->next = NULL;
    // in case this is the first node make the newNode as
    // the head of the LinkedList
    if (*head == NULL) {
        *head = newNode;
        return;
    }
    // Create a pointer to iterate till the last node
    struct ListNode* current = *head;
    while (current->next != NULL) {
        current = current->next;
    }
    // make the next of the tail to the new ListNode
    current->next = newNode;
}

struct ListNode* removeNthFromEnd(struct ListNode* head, int n) {
    if (!head) return NULL;
    struct ListNode* slow = head;
    struct ListNode* fast = head;
    for (int i = 0; i < n; i++) {
        fast = fast->next;
    }
    while (fast && fast->next) {
        fast = fast->next;
        slow = slow->next;
    }

    if (fast == NULL ) {
        head = head->next;
    } else {
        slow->next = slow->next->next;
    }

    return head;
}

int main() {
    struct Node* head = NULL;
    insertAtEnd(&head, 10);
    removeNthFromEnd(head, 1);

    return 0;
}