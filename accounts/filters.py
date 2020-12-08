import django_filters
from .models import *
from django_filters import DateFilter

class OrderFilter(django_filters.FilterSet):

    class Meta:
        model = Order
        fields = "__all__"
        exclude = 'customer', "date_created", "tag"

    start_date = DateFilter(field_name="date_created", lookup_expr="gte")
    end_date = DateFilter(field_name="date_created", lookup_expr="lte")


