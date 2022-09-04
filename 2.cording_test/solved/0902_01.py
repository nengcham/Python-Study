# -*- coding: utf-8 -*-

"""
=========================================================================================================================================================

* 프로젝트명: 지역농작물 및 로컬푸드 활성화를 위한 데이터 분석 모델
* 스크립트명: 네이버 뉴스 크롤링 스크립트

=========================================================================================================================================================
"""


#%% 라이브러리 임포트

from bs4 import BeautifulSoup
import requests
from urllib.parse import quote
import pandas as pd
from tqdm import tqdm
import re
import gc
from datetime import timedelta, date


#%% 공통 함수 설정

#-----------------------------------------------------------------------------
# 날짜 생성 함수
# 설명 : 검색 시작일과 종료일 사이의 모든 날짜를 (15)일 단위로 잘라 periodSet에 저장
#-----------------------------------------------------------------------------

def getPeriod(start,end,period):
    """
    Parameters
    ----------
    start : datetime ex.'2020-01-01'
        생성 원하는 기간 시작일
    end : datetime ex.'2020-12-31'
        생성 원하는 기간 종료일
    period : int ex.13, 15, 30
        날짜 생성 기간을 며칠 단위로 나눌 것인지 설정

    """
    periodSet = []
    sDate = date.fromisoformat(start)
    endDate = date.fromisoformat(end)
    while(True):
        initPeriod = sDate.day % period
        if initPeriod == 0:
            initPeriod = period
        eDate = sDate + timedelta(days=(period -initPeriod))
        if sDate.day > (30 - period):
            if sDate.month < 12:
                eDate = date(sDate.year,sDate.month +1,1) - timedelta(days=1)
            else:
                eDate = date(sDate.year,12,31)
        if eDate >= endDate:
            periodSet.append((sDate.isoformat(),endDate.isoformat()))
            break
        else:
            periodSet.append((sDate.isoformat(),eDate.isoformat()))
        sDate = eDate + timedelta(days=1)
    return periodSet


#%% 공통 전역변수 설정

#-------------------------------------------------------------------------------------------
# 크롤링 검색 시작일/ 종료일 설정 부분
# 설명: 검색 원하는 날짜 형식에 맞춰서 입력 ex) '2020-01-01', '2020-12-31' - 1년 기간 권장
#-------------------------------------------------------------------------------------------

s_date = "2020-01-01" # 검색 시작일 입력
l_date = "2020-12-31" # 검색 종료일 입력


#-------------------------------------------------------------------------------------------
# 전체 검색 기간 리스트 생성
# 설명 : 검색 간격 15일로 getPeriod 함수 호출(1년간 15일 간격 날짜 리스트 생성)
#-------------------------------------------------------------------------------------------
dates = getPeriod(s_date,l_date,15)


#-------------------------------------------------------------------------------------------
# 크롤링 원하는 검색어 설정
# 설명 : 네이버 뉴스 크롤링을 위한 검색어 11개 입력
#-------------------------------------------------------------------------------------------

query_list = ['로컬푸드']

#-------------------------------------------------------------------------------------------
# news_dict 생성
# 설명 : 크롤링 데이터를 담을 빈 딕셔너리 설정
#-------------------------------------------------------------------------------------------

news_dict = {'division': [],
             'kwd': [],
             'date': [],
             'title': [],
             'contents': [],
             'url': []
             }


#%% 본문

#-------------------------------------------------------------------------------------------
# 네이버 뉴스 크롤링 스크립트
# 설명 : 검색 키워드로 검색한 네이버 뉴스 기사의 제목, 날짜, 기사내용, url 크롤링을 위한 스크립트
#-------------------------------------------------------------------------------------------

for query in query_list:
    url_query = quote(query)

    for start_date,last_date in dates:
        start_date = start_date.replace("-","")
        last_date = last_date.replace("-","")

        news_df = pd.DataFrame(columns=('division','kwd','date','title','contents','url'))
        page_num = 400 # 네이버뉴스 사이트 최대 검색결과 페이지 수(최대 4000건, 페이지당 10건씩)

        url = f"https://search.naver.com/search.naver?where=news&query={url_query}&sm=tab_opt&sort=0&photo=0&field=0&pd=3&ds={start_date}&de={last_date}&docid=&related=0&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so%3Ar%2Cp%3Afrom{start_date}to{last_date}&is_sug_officeid=0"

        # 안티 크롤링 회피위한 user-agent값 입력
        headers = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36" }

        ###### 마지막 페이지 자동으로 # 동일한 기사는 패스 #######
        print(f"----START NaverNews Crwl({start_date}->{last_date})----") # 크롤링 중인 기간 및 시간 출력

        for _ in tqdm(range(0,page_num)):
            saerch_url = requests.get(url)
            soup = BeautifulSoup(saerch_url.text, 'html.parser')
            links = soup.find_all('div',{'class':'info_group'})

            for link in links:
                # naver_news가 존재하다면 df생성, 없다면 continue
                try:
                    division = '뉴스'
                    kwd = query
                    news_url = link.findAll('a',{'class':'info'})[1].get('href')
                    news_link = requests.get(news_url, headers=headers)   # http header 필요
                    news_html = BeautifulSoup(news_link.text, 'html5lib')
                    newsdate = news_html.find('span',{'class','t11'}).text[:10]
                    newsdate = newsdate.replace(".","")
                    title = news_html.find('h3',{'id':'articleTitle'}).text
                    title = re.sub('\n','',title)
                    title = re.sub(r'\[[^\]]*\]', '', title)
                    # 기사 본문 내용 중 특수문자 등 불필요한 내용 제거
                    contents = news_html.find('div',{'id':'articleBodyContents'}).text
                    contents = contents.replace('// flash 오류를 우회하기 위한 함수 추가','')
                    contents = contents.replace("function _flash_removeCallback() {}","")
                    contents = contents.replace("\n\t\'","")
                    contents = re.sub(r'\☞.*', '', contents)
                    contents = re.sub(r'\• .*', '', contents)
                    contents = re.sub(r'관련기사.*', '', contents)
                    contents = re.sub(r'\→ .*', '', contents)
                    contents = re.sub(r'\[[^\]]*\]', '', contents)

                    news_dict['division'].append(division)
                    news_dict['kwd'].append(kwd)
                    news_dict['date'].append(newsdate)
                    news_dict['title'].append(title)
                    news_dict['contents'].append(contents)
                    news_dict['url'].append(news_url)
                except:
                    continue

            # 페이지 넘기기
            try:
                next_page = soup.find('a',{'class':'btn_next'}).get('href')
                url = 'https://search.naver.com/search.naver'+ next_page
            except:
                break

    news_df = pd.DataFrame.from_dict(news_dict) # 딕셔너리 데이터프레임으로 출력
    news_df.drop_duplicates(['contents'])       # 중복행 제거
    print(f'{query} 검색 기사:',len(news_df),'건 수집')

    # 뉴스 크롤링 결과 CSV로 저장
    file_path = 'C:/LFA_project21/03.Output/01.Crawling Result/'
    news_df.to_csv(file_path + f'news_{query}.csv', index=False, encoding='utf-8-sig') # 크롤링 결과 csv 파일로 내보내기
    # 메모리 관리
    gc.collect()
