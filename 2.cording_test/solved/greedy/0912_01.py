class Solution:

    '''
    거스름돈으로 사용할 단위 : 500, 100, 50, 10
    거슬러줘야 할 돈 n
    최소한의 동전 수를 구하시오
    '''
    @staticmethod
    def change(n):
        money = n
        count = 0
        coin_type = [500, 100, 50, 10]
        for coin in coin_type:
            count += money // coin
            money %= coin
        return count

    '''
    1이 될 때까지
    어떠한 수 N이 1이 될 때까지 다음의 두 과정 중 하나를 반복적으로 선택하여 수행하고자 한다.
    단 두번째 연산은 N이 K로 나누어 떨어질 때만 선택할 수 있다.
    1. N에서 1을 뺀다.
    2. N을 K로 나눈다.
    N과 K가 주어질 때 N이 1이 될 때까지 1번 혹은 2번의 과정을 수행해야 하는 최소 횟수를 리턴하는 프로그램을 작성하시오. 
    '''
    @staticmethod
    def while_one(n, k):
        result = 0
        while n >= k:
            while n % k != 0:
                n -= 1
                result += 1
            n //= k
            result += 1
        while n > 1:
            n -= 1
            result += 1
        return result


if __name__ == '__main__':
    print(Solution.change(1260))      # 6
    print(Solution.while_one(25, 3))  # 6


