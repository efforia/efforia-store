from __future__ import unicode_literals
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.conf.urls.static import static
from django.views.generic.base import TemplateView,RedirectView
from django.utils.translation import ugettext_lazy as _

admin.autodiscover()

urlpatterns = i18n_patterns(u'', (u'^admin/', include(admin.site.urls)))

urlpatterns += patterns(u'',
                        url(_(r'^shop/volumes/'),TemplateView.as_view(template_name='volumes.html'),name='volumes'),
                        url(_(u'^shop/'), include(u'cartridge.shop.urls'), name='shop'),

			            url(u'^store/slip', "store.views.payment_slip"),
			            url(u'^store/bank', "store.views.payment_bank"),
                        url(u'^store/cancel', "store.views.payment_cancel"),
                        url(u'^store/execute', "store.views.payment_execute", name=u'payment_execute'),
                        url(u'^store/pay/(?P<order_id>\\d+)/$', "store.views.payment_redirect", name=u'payment_redirect'),
                        url(u'^store/orders/$', "cartridge.shop.views.order_history", name=u'order_history'),
                        url(r'^i18n/', include('django.conf.urls.i18n'), name='set_language'),

                        url(_(r'^hub/iot'), TemplateView.as_view(template_name='hub/iot.html'), name='internetofthings'),
                        url(_(r'^hub/howitworks'), TemplateView.as_view(template_name='hub/howitworks.html'), name='howitworks'),
                        url(_(r'^hub/whatisitfor'), TemplateView.as_view(template_name='hub/whatisitfor.html'), name='whatisitfor'),
                        url(_(r'^hub/sensors'), TemplateView.as_view(template_name='hub/sensors.html'), name='sensors'),
                        url(r'^hub/', TemplateView.as_view(template_name='hub/index.html'), name='hub'),

                        url(_(r'^hubpro/personalcomputing'), TemplateView.as_view(template_name='hubpro/personalcomputing.html'), name='personalcomputing'),
                        url(_(r'^hubpro/mediacenter'), TemplateView.as_view(template_name='hubpro/mediacenter.html'), name='mediacenter'),
                        url(_(r'^hubpro/videogame'), TemplateView.as_view(template_name='hubpro/videogame.html'), name='videogame'),
                        url(_(r'^hubpro/server'), TemplateView.as_view(template_name='hubpro/server.html'), name='server'),
                        url(_(r'^hubpro/'), TemplateView.as_view(template_name='hubpro/index.html'), name='uses'),

                        url(_(r'^services/plans'), TemplateView.as_view(template_name='services/plans.html'), name='plans'),
                        url(_(r'^services/cloud'), TemplateView.as_view(template_name='services/cloud.html'), name='services'),
                        url(_(r'^services/partners'), TemplateView.as_view(template_name='services/partners.html'), name='partners'),
                        url(_(r'^services/apps'), TemplateView.as_view(template_name='services/apps.html'), name='apps'),
                        url(_(r'^services/'), TemplateView.as_view(template_name='services/index.html'), name='about'),

                        url(_(r'^help/localization'), TemplateView.as_view(template_name='help/localization.html'), name='localization'),
                        url(_(r'^help/warranty'), TemplateView.as_view(template_name='help/warranty.html'), name='warranty'),
                        url(_(r'^help/documentation'), TemplateView.as_view(template_name='help/documentation.html'), name='documentation'),
                        url(_(r'^help/developer'), TemplateView.as_view(template_name='help/developer.html'), name='developer'),
                        url(_(r'^help/'), TemplateView.as_view(template_name='help/index.html'), name='support'),

                        url(u'^$', TemplateView.as_view(template_name='index.html'), name=u'home'),
						url("^$", "mezzanine.pages.views.page", {"slug": "/"}, name="home"),
                        (u'^', include(u'mezzanine.urls'))
)

handler404 = u'mezzanine.core.views.page_not_found'
handler500 = u'mezzanine.core.views.server_error'
