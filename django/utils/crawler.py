import re
import requests
from bs4 import BeautifulSoup



def get_tr_list(webtoon_id):

    url = 'https://comic.naver.com/webtoon/list.nhn'

    temp_title1 = ''
    temp_date1 = 1

    tr_return = []
    i = 1

    while True:
        params = {
            'titleId': webtoon_id,
            'page': i
        }
        # print(f'{i}번째 반복')
        i += 1
        response = requests.get(url, params)
        source = response.text
        soup = BeautifulSoup(source, 'lxml')
        tr_list = soup.select('tr')

        #########################################################################
        # 시도 3 실패 : for문 안에서 리스트를 삭제하면 그것으로 인해
        #             리스트의 개수 하나가 줄면서 위의 반복되는 리스트에 영향을 주어서 꼬이게 된다.
        # for i, tr in enumerate(tr_list):
        #     print(f'검문 {i}번째')
        #     if re.search(r'.*?th scope.*?', str(tr)) or re.search(r'.*band_banner v2.*', str(tr)):
        #         print(f'삭제 {i}')
        #         del tr_list[i]

        #############################################################
        # 시도 4 : 삭제해야하는 요소가 가장 첫번째 있는 것을 이용한 지저분한 방법
        #      -> 실패 : 마지막 페이지가 10개인 경우 무한 반복됨.
        # if re.search(r'.*?th scope.*?', str(tr_list[0])):
        #     del tr_list[0]
        #
        # if re.search(r'.*band_banner v2.*', str(tr_list[0])):
        #     del tr_list[0]
        #
        # # 삭제 한 후의 값을 저장.
        # tr_return.extend(tr_list)
        #
        # # 삭제 한 후의 tr의 개수가 10개 미만일 경우 마지막 페이지
        # print(len(tr_list))
        # if len(tr_list) < 10:
        #     break

        ##################################################
        # 시도 5 : 요소 동일성 검사

        if re.search(r'.*?th scope.*?', str(tr_list[0])):
            del tr_list[0]

        if re.search(r'.*band_banner v2.*', str(tr_list[0])):
            del tr_list[0]


        # 첫번째 tr요소의 제목을 비교
        temp_title2 = tr_list[0].select_one('td.title > a').text

        # 첫번째 tr요소의 등록일을 비교
        temp_date2 = tr_list[0].select_one('td.num').text

        # 바뀌는 과정 출력
        # print(f'temp_title1: {temp_title1}')
        # print(f'temp_title2: {temp_title2}')
        # print(f'temp_date1: {temp_date1}')
        # print(f'temp_date2: {temp_date2}')
        # print('')

        if temp_title1 == temp_title2 and temp_date1 == temp_date2:
                break
        temp_title1 = temp_title2
        temp_date1 = temp_date2

        # 위에서 삭제 한 후의 값을 저장.
        tr_return.extend(tr_list)

        ##################################################
        # 무한루프가 작동하여 아이피 차단되는 것을 막기위한 안전장치 설정
        if i == 10:
            break

    return tr_return




def get_episode_list(webtoon_id):

    # 시도 1 - 각각의 HTML 페이지를 하나로 합치기
    ###########################################################################
    # BeautifulSoup로 HTML 문서 2개를 저장한 source를 읽으려고 했으나 실패
    # </html>을 만나면 BeautifulSoup이 문서가 종료한 것으로 인지하고 작업을 멈춤.
    # 아래는 파일을 response.txt에 직접써서 하나씩 지워서 </html>이 문제인 것을 파악한 과정.
    # with open('response.txt', 'wt') as f:
    #     f.write(response)
    #
    # source = open('response.txt', 'rt').read()
    ###########################################################################

    # 시도 2 - 외부 함수로 빼기
    #############################################################################
    # 외부함수에서 모든 tr을 가져오되 해당 페이지가 마지막 페이지인지 검사해야 함
    # -> 페이지의 tr이 ( <thead>, <tbody>banner tr 2개를 제외하고 tr이 한 개 이상 존재해야함.
    #############################################################################

    tr_list = get_tr_list(webtoon_id)


    # 예외처리 방법 1 : del 함수 사용
    # # 1) <thead>안의 tr 태그 제거
    # del tr_list[0]
    #
    # # 2) <tbody> 하단에 '다음 화를 미리 만나보세요' 제거
    # # http://comic.naver.com/webtoon/list.nhn?titleId=702672&weekday=sat&page=1
    # if re.search(r'.*band_banner v2.*', str(tr_list[0])):
    #     del tr_list[0]



    # 반복된 BeautifulSoup 객체로 BeautifulSoup을 그대로 쓸 수 있다.
    # soup = BeautifulSoup(tr_list, 'lxml')


    result = []
    for tr in tr_list:

        # # 예외처리 방법2 : continue 사용
        # -> 시도 2의 외부함수로 인해 다시 del tr 함수로 사용
        ###################################################
        # # 1) <thead>안의 tr 제외
        # if re.search(r'.*?th scope.*?', str(tr)):
        #     continue
        # # 2) <tbody> 바로 하단에 '다음 화를 미리 만나보세요' tr 제외
        # if re.search(r'.*?band_banner v2.*', str(tr)):
        #     continue
        ######################################################

        episode_url = tr.select_one('td.title > a').get('href')
        episode_id = re.search(r'.*?\d+.*?(\d+)', episode_url).group(1)
        url_thumbnail = tr.select_one('td > a > img').get('src')
        title = tr.select_one('td.title > a').text
        rating = tr.select_one('div.rating_type > strong').text
        created_date = tr.select_one('td.num').text

        episode = EpisodeData(
            episode_id,
            url_thumbnail,
            title,
            rating,
            created_date
        )
        result.append(episode)
    return result


class EpisodeData:
    def __init__(self, episode_id, url_thumbnail, title, rating, created_date):
        self.episode_id = episode_id
        self.title = title
        self.rating = rating
        self.created_date = created_date
        self.url_thumbnail = url_thumbnail

    def __str__(self):
        return f'{self.episode_id} {self.title} [{self.rating}] ({self.created_date}) {self.url_thumbnail}'



if __name__ == '__main__':
    result = get_episode_list(703835)
    for i in result:
        print(i)
