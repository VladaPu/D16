from django_filters import FilterSet, DateTimeFilter
from django.forms import DateTimeInput
from .models import Posts, Response


class PostFilter(FilterSet):
    time_in_filter = DateTimeFilter(
        field_name='time_in',
        lookup_expr='gt',
        widget=DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local'},
        )
    )

    class Meta:
        model = Posts
        fields = {
            'headline': ['icontains'],
            'category': ['exact'],
        }


class ResponseFilter(FilterSet):
    class Meta:
        model = Response
        fields = [
            'res_post'
        ]

    def __init__(self, *args, **kwargs):
        super(ResponseFilter, self).__init__(*args, **kwargs)
        self.filters['res_post'].queryset = Posts.objects.filter(to_reg_user_id=self.request)
