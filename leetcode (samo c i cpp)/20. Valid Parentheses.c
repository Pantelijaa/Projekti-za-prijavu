#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

typedef struct Node {
    char value;
    struct Node* next;
} NODE;

typedef struct Stack {
    NODE* top;
    size_t len;
} STACK;

// initialize node
NODE* Node(char value, NODE* next) {
    NODE* root = (NODE*)malloc(sizeof(NODE));
    if (root == NULL) exit(EXIT_FAILURE);
    root->value = value;
    root->next = next;
    return root;
}
// initialize stack
STACK* Stack() {
    STACK* stack = (STACK*)malloc(sizeof(STACK));
    if (stack == NULL) exit(EXIT_FAILURE);
    stack->top = NULL;
    stack->len = 0;
    return stack;
}

// append new element to top of the stack
void append(STACK* stack, char value) {
    NODE* node = Node(value, stack->top);
    stack->top = node;
    stack->len += 1;
}

// remove element from top of the stack
char pop(STACK* stack) {
    if (stack->top == NULL) {
        return NULL;
    }
    char value = stack->top->value;
    NODE* deleteNode = stack->top;
    stack->top = stack->top->next;
    stack->len -= 1;
    free(deleteNode);
    return value;
}

void freeStack(struct Stack* stack) {
    while (pop(stack) != NULL) {
        pop(stack);
    }
    free(stack);
}

char opposite_parenthesis(char closing) {
    char opening = NULL;
    if (closing == ')') {
        opening = '(';
    } else if (closing == '}') {
        opening = '{';
    } else if (closing == ']') {
        opening = '[';
    }
    return opening;
}

bool isValid(char* s) {
    STACK* stack = Stack();
    char* chr;

    for (chr = s; *chr != '\0'; chr++) {
        if (opposite_parenthesis(*chr) == NULL) {
            append(stack, *chr);
        } else if (stack->len != 0 && opposite_parenthesis(*chr) == pop(stack)) {
            continue;
        } else return false;
    }
    bool result = stack->len == 0;
    freeStack(stack);
    return result;
}



int main() {

    isValid("()");
    isValid("[)");

    return 0;
}