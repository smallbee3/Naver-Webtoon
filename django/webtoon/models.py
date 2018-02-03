from django.db import models

from utils.crawler import get_episode_list


class Webtoon(models.Model):
    webtoon_id = models.CharField(max_length=100)
    title = models.CharField(max_length=100)


    def __str__(self):
        return '[{}] {}'.format(self.webtoon_id, self.title)


    def get_episode_list(self):

        w = Webtoon.objects.get(pk=self.pk)

        result = get_episode_list(self.webtoon_id)

        # 초급 : 기존에 저장된 웹툰이 있을 경우 저장하지 않음.
        if not w.episode_set.exists():
            for i in result:
                w.episode_set.create(
                    episode_id=i.episode_id,
                    title=i.title,
                    rating=i.rating,
                    created_date=i.created_date,
                )
                w.save()





class Episode(models.Model):
    webtoon = models.ForeignKey(Webtoon, on_delete=models.CASCADE)
    episode_id = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    rating = models.CharField(max_length=100)
    created_date = models.CharField(max_length=100)


    def __str__(self):
        return '{} - {} ({}화)'.format(self.webtoon.title, self.title, self.episode_id)
