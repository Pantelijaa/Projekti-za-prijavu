int min(int a, int b) {
    return (a < b) ? a : b;
}

int max(int a , int b) {
    return (a > b) ? a : b;
}

int maxArea(int* height, int heightSize) {
    int* start = height;
    int* end = height + heightSize - 1;
    int res = 0;
    int area = 0;
    while (start < end) {
        area = min(*start, *end) * (end - start);
        res = max(res, area);

        if (*start <= *end) {
            start++;
        } else {
            end--;
        }

    }
    return res;
}