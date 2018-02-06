from django.http import HttpResponse
from django.shortcuts import render

from .models import Webtoon
from utils.crawler_all_episode import *
from utils.crawler_new_episode import *


def webtoon_list(request):
    # return HttpResponse(f'list')

    webtoon_list = Webtoon.objects.order_by('-pk')

    context = {
        'webtoon_list': webtoon_list,
    }
    return render(request, 'webtoon/webtoon_list.html', context)


def webtoon_detail(request, pk):
    # return HttpResponse(f'detail : {pk}')

    w = Webtoon.objects.get(pk=pk)

    ####################################################
    # 레벨 2 : - 모델이 아닌 뷰에 크롤링 코드 넣기
    #         - 해당 에피소드(디테일 페이지) 접속 시 중복여부 체크 후 크롤링
    #
    # if not w.episode_set.exists():
    #     # webtoon의 id값 - ex) 1인용기분 703835
    #     webtoon_id = w.webtoon_id
    #     result = get_all_episode_list(webtoon_id)
    #     for i in result:
    #         w.episode_set.create(
    #             episode_id=i.episode_id,
    #             title=i.title,
    #             rating=i.rating,
    #             created_date=i.created_date,
    #         )
    #         # w.save()
    #         # 인스턴스 형태로 생성한것이 아니라 Relate Manager를
    #         # 통해 생성한 것이라서 필요없음?

    ####################################################
    # 레벨 3 : 신규 에피소드 업데이트시 기존 데이터 삭제 후 다시 전체 크롤링
    #
    # webtoon_id = w.webtoon_id
    # result = get_all_episode_list(webtoon_id)
    #
    # if not w.episode_set.exists():
    #     print(f'"{w.title}" 최초 크롤링실행')
    #
    #     # 새로 에피소드 불러오기
    #     episode_set_create(w=w, result=result)
    #
    # elif not result[0].title == w.episode_set.first().title:
    #     print(f'크롤링 최근 title: {result[0].title}')
    #     print(f'기존 최근 title: {w.episode_set.first().title}')
    #     print(f'"{w.title}" 신규에피소드 업데이트 크롤링실행')
    #
    #     # 기존 에피소드 삭제
    #     w.episode_set.all().delete()
    #
    #     # 새로 에피소드 불러오기
    #     episode_set_create(w=w, result=result)

    ####################################################
    # 레벨 4 : 신규 에피소드 업데이트시 기존 데이터는
    #         그대로 두고 신규데이터만 추가
    webtoon_id = w.webtoon_id
    result = get_all_episode_list(webtoon_id)

    if not w.episode_set.exists():
        print(f'"{w.title}" 최초 크롤링실행')

        # 최초 에피소드 불러오기
        episode_set_create(w=w, result=result)

    else: # update_result를 생성해야되기 때문에 elif 안씀.
        update_result = get_new_episode_list(webtoon_id, w)
        if update_result:
            # 신규 에피소드'만' 추가하기
            episode_set_create(w=w, result=update_result)

    # context = {'w': w}
    #  -> w를 전달하면 템플릿내에서 .order_by로 정렬할 수가 없어서
    #     인스턴스 대신 pk가 역순으로 정렬된 리스트 자체를 전달.

    episode_list = w.episode_set.all().order_by('-pk')

    context = {
        'episode_list': episode_list
    }
    return render(request, 'webtoon/webtoon_detail.html', context)


# 에피소드 인스턴스 생성 부분을 함수로 별도 분리
def episode_set_create(w, result):
    for i in result:
        w.episode_set.create(
            episode_id=i.episode_id,
            title=i.title,
            rating=i.rating,
            created_date=i.created_date,
        )
