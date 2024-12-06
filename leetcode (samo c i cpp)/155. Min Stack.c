#include <stdbool.h>
#include <stdlib.h>

typedef struct stack {
    int val;
    int minVal;
    struct stack* next;
} MinStack;

MinStack* head = NULL;

MinStack* minStackCreate() {
    return NULL;
}

void minStackPush(MinStack* obj, int val) {
    MinStack* node = (MinStack*)malloc(sizeof(MinStack));
    node->val = val;
    node->next = head;
    head = node;
    if (head->next == NULL) {
        head->minVal = val;
    } else {
        head->minVal = (val < head->next->minVal) ? val : head->next->minVal;
    }
}

void minStackPop(MinStack* obj) {
    MinStack* temp = head;
    head = head->next;
    free(temp);
}

int minStackTop(MinStack* obj) {
    return head->val;
}

int minStackGetMin(MinStack* obj) {
    return head->minVal;
}

void minStackFree(MinStack* obj) {
    while(head != NULL) {
        minStackPop(head);
    }
}

int main() {
    MinStack* head = NULL;
    minStackPush(head, -2);
    minStackPush(head, 0);
    minStackPush(head, -3);
    minStackGetMin(head);
    minStackPop(head);
    minStackTop(head);
    minStackGetMin(head);

    return 0;
}