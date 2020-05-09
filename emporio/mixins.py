import json

from django.core import serializers
from django.core.exceptions import ImproperlyConfigured
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.detail import SingleObjectTemplateResponseMixin, BaseDetailView
from django.views.generic.list import MultipleObjectTemplateResponseMixin, BaseListView

class JSONResponseMixin(object):
    """
    A mixin that allows you to easily serialize simple data such as a dict or
    Django models.
    """
    content_type = None
    json_dumps_kwargs = None
    json_encoder_class = DjangoJSONEncoder

    def get_content_type(self):
        return self.content_type or "application/json"

    def get_json_dumps_kwargs(self):
        if self.json_dumps_kwargs is None:
            self.json_dumps_kwargs = {}
        self.json_dumps_kwargs.setdefault('ensure_ascii', False)
        return self.json_dumps_kwargs

    def render_json_response(self, context_dict, status=200):
        """
        Limited serialization for shipping plain data. Do not use for models
        or other complex or custom objects.
        """
        json_context = json.dumps(
            list(context_dict['object_list'].values()),
            cls=self.json_encoder_class,
            **self.get_json_dumps_kwargs()).encode('utf-8')
        return HttpResponse(json_context,
                            content_type=self.get_content_type(),
                            status=status)

    def render_json_object_response(self, objects, **kwargs):
        """
        Serializes objects using Django's builtin JSON serializer. Additional
        kwargs can be used the same way for django.core.serializers.serialize.
        """
        json_data = serializers.serialize("json", objects, **kwargs)
        return HttpResponse(json_data, content_type=self.get_content_type())

class JsonRequestResponseMixin(JSONResponseMixin):
    """
    Extends JSONResponseMixin.  Attempts to parse request as JSON.  If request
    is properly formatted, the json is saved to self.request_json as a Python
    object.  request_json will be None for imparsible requests.
    Set the attribute require_json to True to return a 400 "Bad Request" error
    for requests that don't contain JSON.
    Note: To allow public access to your view, you'll need to use the
    csrf_exempt decorator or CsrfExemptMixin.
    """
    require_json = False
    error_response_dict = {"errors": ["Improperly formatted request"]}

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

    @method_decorator(csrf_exempt)
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
        if request.method == 'POST':
            self.model.objects.create(**self.request_json)
            return JsonResponse(self.request_json, status=201)
        return super(JsonRequestResponseMixin, self).dispatch(
            request, *args, **kwargs)

class HybridDetailView(JsonRequestResponseMixin, SingleObjectTemplateResponseMixin, BaseDetailView):
    def render_to_response(self, context):
        # Look for a 'format=json' GET argument
        if self.request.GET.get('format') == 'html':
            return super().render_to_response(context)
        else:
            return self.render_json_response(context)

class HybridListView(JsonRequestResponseMixin, SingleObjectTemplateResponseMixin, BaseListView):
    def render_to_response(self, context):
        # Look for a 'format=json' GET argument
        if self.request.GET.get('format') == 'html':
            return super().render_to_response(context)
        else:
            return self.render_json_response(context)