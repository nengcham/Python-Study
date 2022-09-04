'''
n x m 크기의 직사각형을 자르려고 한다. 직사각형의 각 변은 x축, y츅에 평행하며,
직사각형의 왼쪽 아래 꼭짓점의 좌표를 (0, 0), 오른쪽 위 쪽짓점의 좌표를 (n, m)으로 한다.

이 직사각형을 x축, 혹은 y축에 평행한 선분을 이용하여 여러 조각으로 잘라내려 한다.
직사각형을 자르는 선분은 x축 좌표와 y축 좌표를 이용해 표현한다.

직사각형을 잘라낸 후 만들어지는 작은 직사각형 중 가장 큰 직사각형을 넓이를 찾아 return 하라.
'''


def solution(n, m, x_axis, y_axis):
    x_axis.insert(0, 0)
    x_axis.append(n)
    x_list = []
    for i, j in enumerate(x_axis):
        try:
            x_list.append(x_axis[i+1] - x_axis[i])
        except:
            pass

    y_axis.insert(0, 0)
    y_axis.append(m)
    y_list = []
    for i, j in enumerate(y_axis):
        try:
            y_list.append(y_axis[i+1] - y_axis[i])
        except:
            pass

    x_list.sort()
    y_list.sort()
    answer = x_list[-1]*y_list[-1]
    return answer


if __name__ == '__main__':
    print(solution(n=3, m=4, x_axis=[2], y_axis=[1, 2]))

