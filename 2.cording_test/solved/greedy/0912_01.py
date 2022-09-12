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
    배열 
    '''
    @staticmethod
    def large_num(n, m, k):



if __name__ == '__main__':
    print(Solution.change(1260))

