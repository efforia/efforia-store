import json

from http import HTTPStatus

from django.core import serializers
from django.core.exceptions import ImproperlyConfigured
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse, HttpResponseNotFound
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from django.views.generic.detail import SingleObjectTemplateResponseMixin, BaseDetailView
from django.views.generic.list import MultipleObjectTemplateResponseMixin, BaseListView

class HttpResponseNoContent(HttpResponse):
    status_code = HTTPStatus.NO_CONTENT

class JsonRequestResponseMixin(object):
    '''
    Code inspired on django-braces JsonRequestResponseMixin. A mixin that allows you to easily 
    serialize simple data such as a dict or Django models.  Attempts to parse request as JSON. 
    If request is properly formatted, the json is saved to self.request_json as a Python object,
    request_json will be None for imparsible requests. Set the attribute require_json to True to 
    return a 400 'Bad Request' error for requests that don't contain JSON. Note: To allow public 
    access to the view dispatch function, it's needed to use the csrf_exempt decorator.
    '''

    content_type = None
    json_dumps_kwargs = None
    json_encoder_class = DjangoJSONEncoder
    require_json = False
    error_response_dict = {'errors': ['Improperly formatted request']}

    def get_content_type(self):
        return self.content_type or 'application/json'

    def get_json_dumps_kwargs(self):
        if self.json_dumps_kwargs is None:
            self.json_dumps_kwargs = {}
        self.json_dumps_kwargs.setdefault('ensure_ascii', False)
        return self.json_dumps_kwargs

    def render_bad_request_response(self, error_dict=None):
        if error_dict is None:
            error_dict = self.error_response_dict
        json_context = json.dumps(
            error_dict,
            cls=self.json_encoder_class,
            **self.get_json_dumps_kwargs()
        ).encode('utf-8')
        return HttpResponseBadRequest(
            json_context, content_type=self.get_content_type())

    def get_request_json(self):
        try:
            return json.loads(self.request.body.decode('utf-8'))
        except ValueError:
            return None

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.args = args
        self.kwargs = kwargs
        self.request_json = self.get_request_json()
        if all([
            request.method != 'OPTIONS',
            self.require_json,
            self.request_json is None
        ]):
            return self.render_bad_request_response()
        return super(JsonRequestResponseMixin, self).dispatch(
            request, *args, **kwargs)

    def get_data(self, context):
        if isinstance(self, BaseDetailView):
            return list(self.get_queryset().values())[0]
        elif isinstance(self, BaseListView):
            return list(self.get_queryset().values())
        else:
            return context

    def render_json_response(self, context_dict, status=200):
        '''
        Limited serialization for shipping plain data. Do not use for models
        or other complex or custom objects.
        '''
        return JsonResponse(self.get_data(context_dict), safe=False, status=status)

    def render_json_object_response(self, objects, **kwargs):
        '''
        Serializes objects using Django's builtin JSON serializer. Additional
        kwargs can be used the same way for django.core.serializers.serialize.
        '''
        return JsonResponse(serializers.serialize('json', objects), safe=False)

    def render_to_response(self, context, **response_kwargs):
        if self.request.GET.get('format') == 'html':
            return super().render_to_response(context, **response_kwargs)
        else:
            return self.render_json_response(context, **response_kwargs)

class HybridDetailView(JsonRequestResponseMixin, SingleObjectTemplateResponseMixin, BaseDetailView):
    '''
    Hybrid DetailView class, for rendering API options and templates (when available). It contains
    all generic stuff for detail REST API operations, such as PUT, PATCH and DELETE methods
    '''

    def put(self, request, pk, *args, **kwargs):
        try:
            self.model.objects.filter(id=pk).update(**self.request_json)
        except self.model.DoesNotExist:
            self.model.objects.create(**self.request_json)
        return self.render_json_object_response(self.request.body)
    
    def patch(self, request, pk, *args, **kwargs):
        models = self.model.objects.filter(id=pk) 
        if not models:
            return HttpResponseNotFound()
        else:
            models.update(**self.request_json)
            return self.render_json_response({'object_list': models})

    def delete(self, request, pk, *args, **kwargs):
        models = self.model.objects.filter(id=pk)
        if not models:
            return HttpResponseNotFound()
        else:
            models.delete()
            return HttpResponseNoContent()

class HybridListView(JsonRequestResponseMixin, SingleObjectTemplateResponseMixin, BaseListView):
    '''
    Hybrid ListView class, for rendering API options and templates (when available). It contains
    all generic stuff for list REST API operations, such as POST method
    '''

    def post(self, request, *args, **kwargs):
        self.model.objects.create(**self.request_json)
        return self.render_json_object_response(self.request.body, status=201)