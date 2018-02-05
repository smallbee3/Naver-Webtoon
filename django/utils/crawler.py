import re
import requests
from bs4 import BeautifulSoup



def get_episode_list(webtoon_id, page):
    url = 'https://comic.naver.com/webtoon/list.nhn'
    params = {
        'titleId': webtoon_id,
        'page': page
    }

    response = requests.get(url, params)
    soup = BeautifulSoup(response.text, 'lxml')

    tr_list = soup.select('tr')
    ##################################################
    # # 예외처리 방법 1 : del 함수 사용
    # # 1) <thead>안의 tr 태그 제거
    # del tr_list[0]
    #
    # # 2) <tbody> 하단에 '다음 화를 미리 만나보세요' 제거
    # # http://comic.naver.com/webtoon/list.nhn?titleId=702672&weekday=sat&page=1
    # if re.search(r'.*band_banner v2.*', str(tr_list[0])):
    #     del tr_list[0]

    result = []
    for tr in tr_list:

        # # 예외처리 방법2 : continue 사용
        ##################################################
        # 1) <thead>안의 tr 제외
        if re.search(r'.*?th scope.*?', str(tr)):
            continue
        # 2) <tbody> 바로 하단에 '다음 화를 미리 만나보세요' tr 제외
        elif re.search(r'.*?band_banner v2.*', str(tr)):
            continue

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
    result = get_episode_list(679519, 2)
    for i in result:
        print(i)


# 1인용기분 703835
# 노곤하개 702672
# 열대어 703629
# 우리 오빠는 아이돌 700843
# 연애학 696602