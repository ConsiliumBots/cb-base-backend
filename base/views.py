
from app.permissions import *
from django.db.models import Avg, Count, Sum
from rest_framework import viewsets
from rest_framework.response import Response
from base.utils import print_exception
from base.permissions import request_to_user


class BaseViewSet(viewsets.ModelViewSet):
    """
    BaseViewSet that allows for specific classes per retrieval.
    """

    @print_exception
    def get_queryset(self, params=None):
        if params != None:
            params = params
        else:
            params = self.request.query_params
            params = {i: params[i] for i in params if not i.startswith('_')}
        order_by = params.pop('order_by', None)
        required_fields = params.pop('required_fields', None)
        unique = params.pop('unique', None)
        limit = params.pop('limit', None)
        params.pop('average_on', None)
        params.pop('count_on', None)
        params.pop('sum_on', None)
        params.pop('page', None)
        params.pop('group_by', None)
        params.pop('nest', None)
        if order_by:
            order_by = order_by.split(",")
        else:
            order_by = []
        results = super().get_queryset().filter(**params).order_by(*order_by)
        if unique and required_fields:
            results = results.distinct(*required_fields.split(","))
        if limit and results.count() > int(limit):
            results = results[:int(limit)]
        return results

    @ property
    def user(self):
        return request_to_user(self.request)

    @print_exception
    def list(self, request, *args, **kwargs):
        params = self.request.query_params
        params = {i: params[i] for i in params}

        average_on = params.pop('average_on', None)
        sum_on = params.pop('sum_on', None)
        count_on = params.pop('count_on', None)
        group_by = params.pop('group_by', None)
        params.pop('nest', None)
        if group_by:
            filters = dict()
            exclusion_filters = dict()
            if sum_on:
                filters['sum'] = Sum(sum_on)
                exclusion_filters[f'{sum_on}__isnull'] = False
            if average_on:
                filters['average'] = Avg(average_on)
                exclusion_filters[f'{average_on}__isnull'] = False
            if count_on:
                filters['count'] = Count(count_on)
                exclusion_filters[f'{count_on}__isnull'] = False
            try:
                return Response(self.get_queryset().filter(**exclusion_filters).values(group_by).annotate(**filters))
            except Exception as E:
                return super().list(request, *args, **kwargs)
        if average_on:
            exclusion_filters = {f'{average_on}__isnull': False}
            return Response(self.get_queryset().filter(**exclusion_filters).aggregate(Avg(average_on)))
        if sum_on:
            exclusion_filters = {f'{sum_on}__isnull': False}
            return Response(self.get_queryset().filter(**exclusion_filters).aggregate(Sum(sum_on)))
        return super().list(request, *args, **kwargs)

    def get_serializer_context(self):
        params = self.request.query_params
        params = {i: params[i] for i in params if not i.startswith('_')}
        params.pop('unique', None)
        params.pop('average_on', None)
        params.pop('group_by', None)
        required_fields = params.pop('required_fields', None)
        nest = params.pop('nest', None)
        context = super().get_serializer_context()
        if required_fields:
            context['fields'] = required_fields.split(",")
        if nest is not None:
            context['nest'] = nest
        return context

    def set_permission_classes(self):
        _class = self.__class__
        if self.action == "retrieve" and hasattr(_class, 'get_permission_classes'):
            self.permission_classes = _class.get_permission_classes
        elif self.action == "list" and hasattr(_class, 'get_permission_classes'):
            self.permission_classes = _class.get_permission_classes
        elif self.action == "create" and hasattr(_class, 'post_permission_classes'):
            self.permission_classes = _class.post_permission_classes
        elif self.action == "partial_update" and hasattr(_class, 'patch_permission_classes'):
            self.permission_classes = _class.patch_permission_classes
        elif self.action == "destroy" and hasattr(_class, 'delete_permission_classes'):
            self.permission_classes = _class.delete_permission_classes

    def get_permissions(self):
        self.set_permission_classes()
        if self.user and self.user.is_superuser:
            return []
        return super().get_permissions()
