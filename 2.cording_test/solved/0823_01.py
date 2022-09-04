def solution(n, queries):
    answer = []
    for i, j in enumerate(queries):
        globals()[f's{i}'] = []

    def push(query: list):
        globals()[f's{query[0]}'].append(query[1])

    def pop(a):
        try:
            answer.append(globals()[f's{a}'][-1])
        except:
            answer.append(-1)

    for i in queries:
        if i[1] != -1:
            push(i)
        else:
            pop(i[0])
    return print(answer)


if __name__ == '__main__':
    solution(3, [[1, 4], [2, 2], [1, 3], [1, 6], [3, -1], [2, -1]])
    # [4, 2]
    print('-------------')
    solution(4, [[1, 3], [1, 2], [3, 6], [3, -1], [4, 5], [2, -1], [3, -1], [1, -1]])
    # [6, 3, 5, 2]
    print('-------------')
    solution(5, [[1, -1], [2, -1], [3, -1], [4, -1], [5, -1]])
    # [-1, -1, -1, -1, -1]