def solution(n, k):
    answer = 0
    
    answer = n * 12000 + (k - n // 10) * 2000
    
    return answer