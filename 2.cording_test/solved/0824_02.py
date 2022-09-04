# def solution(cookie: list):
#     answer = -1
#     for i, j in enumerate(cookie):
#         sum1 = sum(cookie[:i])
#         sum2 = sum(cookie[i:])
#         if sum1 == sum2:
#             answer = sum1
#     return answer

def solution(cookie):
    answer = 0
    for l in range(len(cookie) - 2):
        for m in range(l + 1, len(cookie) - 1):
            for r in range(m + 1, len(cookie)):
                a = sum(cookie[l:m + 1])
                answer = a if a == sum(cookie[m+1:r+1]) and answer < a else 0
    return answer


if __name__ == '__main__':
    print(solution([1, 1, 2, 3]))
    print('-------')
    print(solution([1, 2, 4, 5]))

