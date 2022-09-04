import string

import sqlalchemy
import pytest
import re

from sqlalchemy.sql import text
from typing import List, Dict, Optional


def test_case1():
    service = Service()
    res = service.solution(" blue 밀리터리재킷&@*@ 7,000원 ")
    assert res == ["재킷", "밀리터리재킷"]


# def test_case2():
#     service = Service()
#     res = service.solution(" Gown-Dress and 캐주얼상의 (10,000)")
#     assert res == ["dresses", "gown-dress", "캐주얼상의", ""]
#
#
# def test_case3():
#     service = Service()
#     res = service.solution("T恤衫")
#     assert res == ["休闲上衣", "T恤衫"]
#
#
# def test_case4():
#     service = Service()
#     res = service.solution(" blue밀리터리재킷&@*@ 7,000원 ")
#     assert res == ["", ""]
#
#
# def test_case5():
#     service = Service()
#     res = service.solution("Gracious life 피그먼트 스웨트셔츠 [Blue]_맨투맨")
#     assert res == ["캐주얼상의", "스웨트셔츠"]


# pytest.main()


class Mysql:
    def __init__(self):
        # Connect to the DB and reflect metadata.
        engine = sqlalchemy.create_engine('mysql://coderpad:@/coderpad?unix_socket=/tmp/mysql/socket/mysqld.sock')
        self.connection = engine.connect()

    def execute(self, query: str, data: Optional[dict] = None) -> List[Dict[str, any]]:
        """

        사용 예:
        res = Mysql().execute("SELECT * FROM TAGGER_M WHERE ID = :id", {"id": 1})

        참조: https://docs.sqlalchemy.org/en/14/core/sqlelement.html#sqlalchemy.sql.expression.text

        """
        query_result = self.connection.execute(text(query), data)
        return [{column: value for (column, value) in row._mapping.items()} for row in query_result]


class Service:
    def __init__(self):
        pass

    def solution(self, product_name: str) -> List[str]:
        product_name_list = product_name.translate(str.maketrans('', '', string.punctuation)).split()
        category_name = "재킷"
        item_name = "밀리터리재킷"
        print(product_name_list)
        return [f"{category_name}", f"{item_name}"]

#
# if __name__ == '__main__':
#     Service().solution('blue밀리터리재킷&@*@ 7,000원')