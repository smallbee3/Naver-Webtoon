from django.http import HttpResponse
from django.shortcuts import render, redirect

from .models import Webtoon
from utils.crawler import get_episode_list



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

    # 레벨 2 : 모델이 아닌 뷰에 크롤링 코드 넣기
    #        해당 에피소드(디테일 페이지) 접속 시 중복여부 체크 후 크롤링

    if not w.episode_set.exists():
        # webtoon의 id값 - ex) 1인용기분 703835
        webtoon_id = w.webtoon_id
        result = get_episode_list(webtoon_id)
        for i in result:
            w.episode_set.create(
                episode_id=i.episode_id,
                title=i.title,
                rating=i.rating,
                created_date=i.created_date,
            )
            # w.save()
            # 인스턴스 형태로 생성한것이 아니라 Relate Manager를
            # 통해 생성한 것이라서 필요없음?


    context = {
        'w': w
    }
    return render(request, 'webtoon/webtoon_detail.html', context)