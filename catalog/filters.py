from django_filters import rest_framework as filters


class ImageFilter(filters.FilterSet):
    original_url = filters.CharFilter(method="filter_by_original_url")

    def filter_by_original_url(self, queryset, name, value):
        if value is None:
            return queryset
        try:
            return queryset.filter(original_url=value)
        except:
            return queryset.none()


class ImageMetadataFilter(filters.FilterSet):
    original_url = filters.CharFilter(method="filter_by_original_url")

    def filter_by_original_url(self, queryset, name, value):
        if value is None:
            return queryset
        try:
            return queryset.filter(image__original_url=value)
        except:
            return queryset.none()