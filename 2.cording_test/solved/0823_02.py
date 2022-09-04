def solution(N, K):

    answer = 0
    for i in [i for i in range(2**N-1) if i % 3 == 0]:
        if len(str(bin(i)[2:]).replace('0', '')) == K:
            answer += 1
    return print(answer)


if __name__ == '__main__':
    solution(6, 3)
