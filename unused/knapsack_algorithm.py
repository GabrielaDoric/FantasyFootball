import numpy as np

# A Dynamic Programming based Python
# Program for 0-1 Knapsack problem
# Returns the maximum value that can
# be put in a knapsack of capacity W
def knapSack(C, price, val, n):
    K = [[0 for x in range(C + 1)] for x in range(n + 1)]

    # Build table K[][] in bottom up manner
    for i in range(n + 1):
        for c in range(C + 1):

            if i == 0 or c == 0:
                K[i][c] = 0
            elif price[i - 1] <= c:
                K[i][c] = max(val[i - 1] + K[i - 1][c - price[i - 1]],
                              K[i - 1][c])
            else:
                K[i][c] = K[i - 1][c]

    return K[n][C]


# Driver program to test above function
val = [60, 100, 120]
wt = [10, 20, 30]
W = 50
n = len(val)
print(knapSack(W, wt, val, n))