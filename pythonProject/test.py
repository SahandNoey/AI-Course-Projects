def f(n):
    if n == 1:
        return 1
    if n == 2:
        return 2
    else:
            return f(n-1) + f(n-2)