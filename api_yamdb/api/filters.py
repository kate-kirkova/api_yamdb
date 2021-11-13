from django_filters import rest_framework as filters

from reviews.models import Title


class TitleFilter(filters.FilterSet):
    genre = filters.Filter(field_name='genre__slug')
    category = filters.Filter(field_name='category__slug')
    name = filters.Filter(field_name='name', lookup_expr='contains')

    class Meta:
        model = Title
        fields = ('name', 'year', 'genre', 'category')
