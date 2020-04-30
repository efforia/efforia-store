from __future__ import unicode_literals
from django.conf import settings
from django.conf.urls import include, url as django_url
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.conf.urls.static import static
from django.views.generic.base import TemplateView,RedirectView
from django.utils.translation import ugettext_lazy as _
from django.conf.urls.static import static
from django_distill import distill_url as url

# import .views

admin.autodiscover()

def getNone(): return None

# urlpatterns = i18n_patterns(django_url(u'^admin/', include(admin.site.urls)))

urlpatterns = [
    # url(_(r'^shop/volumes/'),TemplateView.as_view(template_name='volumes.html'),name='volumes', distill_func=getNone),
    # url(_(u'^shop/'), include(u'cartridge.shop.urls'), name='shop'),

    url(u'^store/services',TemplateView.as_view(template_name='pages/services.html'), name='store_services', distill_func=getNone),
    url(u'^store/choose',TemplateView.as_view(template_name='pages/choose.html'), name='store_choose', distill_func=getNone),
    # url(u'^store/slip', invent.views.payment_slip, name='store_slip', distill_func=getNone),
    # url(u'^store/bank', invent.views.payment_bank, name='store_bank', distill_func=getNone),
    # url(u'^store/cancel', invent.views.payment_cancel, name='store_cancel', distill_func=getNone),
    # url(u'^store/execute', invent.views.payment_execute, name=u'payment_execute', distill_func=getNone),
    # url(u'^store/pay/(?P<order_id>\\d+)/$', invent.views.payment_redirect, name=u'payment_redirect', distill_func=getNone),
    # url(u'^store/orders/$', "cartridge.shop.views.order_history", name=u'order_history'),
    # url(r'^i18n/', include('django.conf.urls.i18n'), name='set_language', distill_func=getNone),

    url(_(r'^atom/'), TemplateView.as_view(template_name='atom/index.html'), name='sensors', distill_func=getNone),

    url(_(r'^hub/iot'), TemplateView.as_view(template_name='hub/iot.html'), name='iot', distill_func=getNone),
    url(_(r'^hub/eos'), TemplateView.as_view(template_name='hub/eos.html'), name='eos', distill_func=getNone),
    url(_(r'^hub/server'), TemplateView.as_view(template_name='hub/server.html'), name='server', distill_func=getNone),
    url(r'^hub/', TemplateView.as_view(template_name='hub/index.html'), name='hub', distill_func=getNone),

    url(_(r'^tv/eosd'), TemplateView.as_view(template_name='tv/eosd.html'), name='eosd', distill_func=getNone),
    url(_(r'^tv/mediacenter'), TemplateView.as_view(template_name='tv/mediacenter.html'), name='mediacenter', distill_func=getNone),
    url(_(r'^tv/videogame'), TemplateView.as_view(template_name='tv/videogame.html'), name='videogame', distill_func=getNone),
    url(_(r'^tv/'), TemplateView.as_view(template_name='tv/index.html'), name='hubpro', distill_func=getNone),

    #url(_(r'^services/design'), TemplateView.as_view(template_name='services/design.html'), name='hubdesign'),
    #url(_(r'^services/plans'), TemplateView.as_view(template_name='services/plans.html'), name='plans'),
    #url(_(r'^services/cloud'), TemplateView.as_view(template_name='services/cloud.html'), name='services'),
    #url(_(r'^services/partners'), TemplateView.as_view(template_name='services/partners.html'), name='partners'),
    #url(_(r'^services/apps'), TemplateView.as_view(template_name='services/apps.html'), name='apps'),
    #url(_(r'^services/developer'), TemplateView.as_view(template_name='services/developer.html'), name='developer'),
    #url(_(r'^services/'), TemplateView.as_view(template_name='services/index.html'), name='about'),

    url(_(r'^help/localization'), TemplateView.as_view(template_name='help/localization.html'), name='localization', distill_func=getNone),
    url(_(r'^help/warranty'), TemplateView.as_view(template_name='help/warranty.html'), name='warranty', distill_func=getNone),
    url(_(r'^help/documentation'), TemplateView.as_view(template_name='help/documentation.html'), name='documentation', distill_func=getNone),
    url(_(r'^help/'), TemplateView.as_view(template_name='help/index.html'), name='support', distill_func=getNone),

    url(u'^$', TemplateView.as_view(template_name='index.html'), name=u'home', distill_func=getNone),
    # url(r'^accountold/', RedirectView.as_view(url='/'), name=u'old_account_redirect', distill_func=getNone),
    # url(u'^', include(u'mezzanine.urls'))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# handler404 = u'mezzanine.core.views.page_not_found'
# handler500 = u'mezzanine.core.views.server_error'
