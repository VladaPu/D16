from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.urls import reverse
from django.utils.translation import gettext as _
from ckeditor_uploader.fields import RichTextUploadingField


class RegUsers(models.Model):
    reg_user = models.OneToOneField(User,  on_delete=models.CASCADE)


class Category(models.Model):
    name = models.CharField(max_length=30, unique=True, help_text=_('Category name'))
    subscriber = models.ManyToManyField(User, through='Subscriptions')

    def __str__(self):
        return self.name.title()


class Posts(models.Model):
    tanks = 'TK'
    healers = 'HL'
    damage_dealers = 'DD'
    merchants = 'MR'
    guild_masters = 'GM'
    quest_givers = 'QG'
    smiths = 'SM'
    leather_workers = 'LW'
    potion_masters = 'PM'
    enchanters = 'EH'

    TYPE = [
        (tanks, 'Танки'), (healers, 'Хилеры'), (damage_dealers, 'ДД'), (merchants, 'Торговцы'),
        (guild_masters, 'Гильдмастера'), (quest_givers, 'Квестгиверы'), (smiths, 'Кузнецы'),
        (leather_workers, 'Кожевники'), (potion_masters, 'Зельевары'), (enchanters, 'Мастера заклинаний')
    ]

    type_post = models.CharField(max_length=2, choices=TYPE, default='MR')
    time_in = models.DateTimeField(auto_now_add=True)
    headline = models.CharField(max_length=128)
    text = RichTextUploadingField(config_name='my-toolbar')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category')
    to_reg_user = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])


class Response(models.Model):
    time_in = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    res_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reply_user')
    res_post = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name='reply')
    status = models.BooleanField(default=False)

    def __str__(self):
        return 'Response by {} on {}'. format(self.res_user, self.res_post)

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.res_post.id)])


class Subscriptions(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )
    to_category = models.ForeignKey(
        to=Category,
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )




