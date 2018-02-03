from django.http import HttpResponse
from django.shortcuts import render, redirect

from .models import Webtoon


def webtoon_list(request):
    # return HttpResponse(f'list')

    webtoon_list = Webtoon.objects.order_by('-webtoon_id')

    context = {
        'webtoon_list': webtoon_list,
    }
    return render(request, 'webtoon/webtoon_list.html', context)




def webtoon_detail(request, pk):
    # return HttpResponse(f'detail : {pk}')

    webtoon = Webtoon.objects.get(pk=pk)
    context = {
        'webtoon': webtoon
    }
    return render(request, 'webtoon/webtoon_detail.html', context)