import re
import requests
from bs4 import BeautifulSoup


def get_new_episode_list(webtoon_id, w):
    url = 'https://comic.naver.com/webtoon/list.nhn'

    i = 1
    # while_loop_break = 0

    result = []

    while True:
        params = {
            'titleId': webtoon_id,
            'page': i
        }
        print('')
        print(f'{i}페이지 신규 에피소드 여부 확인중...')
        print('')
        response = requests.get(url, params)
        source = response.text
        soup = BeautifulSoup(source, 'lxml')
        tr_list = soup.select('tr')

        if re.search(r'.*?th scope.*?', str(tr_list[0])):
            del tr_list[0]

        if re.search(r'.*band_banner v2.*', str(tr_list[0])):
            del tr_list[0]

        last_episode_id = str(w.episode_set.last().episode_id)

        for tr in tr_list:

            episode_url = tr.select_one('td.title > a').get('href')
            new_episode_id = re.search(r'.*?\d+.*?(\d+)', episode_url).group(1)
            print('[가장 최근 에피소드와 크롤링한 에피소드와 비교]')
            print(f'new_episode_id: {new_episode_id}')
            print(f'last_episode_id: {last_episode_id}')

            if last_episode_id != new_episode_id:

                # episode_url = tr.select_one('td.title > a').get('href')
                # episode_id = re.search(r'.*?\d+.*?(\d+)', episode_url).group(1)
                # 주석처리하지 않으면 위에서 만든 episode_id가 덮어씌워짐.

                url_thumbnail = tr.select_one('td > a > img').get('src')
                title = tr.select_one('td.title > a').text
                rating = tr.select_one('div.rating_type > strong').text
                created_date = tr.select_one('td.num').text

                episode = EpisodeData(
                    new_episode_id,
                    url_thumbnail,
                    title,
                    rating,
                    created_date
                )
                # result.append(episode)
                # 신규 에피소드 추가 시 기존 리스트가 역순으로 되어 있어서 문제가 됨.
                # 굉장히 간단히 역순으로 넣어주면 되는 것을 pk를 바꾸는 방법으로 생각해서
                # 1시간 날라감.
                result.insert(0, episode)

                print(f'신규 에피소드 [episode_id: {episode.episode_id} title: {episode.title} 추가')
            else:
                # while_loop_break = 1
                print(f'{i}페이지에서 신규 에피소드 추가 작업 종료')
                return result

                # return result로 함수 전체가 종료되는지 모르고
                # 가장 안쪽의 for문만 빠져나오는지 알고 while문을 빠져나가는
                # 무의미한 장치 설정.
                # break

        # if while_loop_break == 1:
        #     print('while문 탈출')
        #     # return result
        #     return

        ##################################################
        # 무한루프가 작동하여 아이피 차단되는 것을 막기위한 안전장치 설정
        if i == 5:
            print('')
            print('"지나친 크롤링으로 crawler_new_episode.py의 크롤링 차단장치 작동"')
            print('')
            break
        i += 1


class EpisodeData:
    def __init__(self, episode_id, url_thumbnail, title, rating, created_date):
        self.episode_id = episode_id
        self.title = title
        self.rating = rating
        self.created_date = created_date
        self.url_thumbnail = url_thumbnail

    def __str__(self):
        return f'{self.episode_id} {self.title} [{self.rating}] ({self.created_date}) {self.url_thumbnail}'

# 1인용기분 703835
# 노곤하개 702672
# 열대어 703629
# 우리 오빠는 아이돌 700843
# 연애학 696602
