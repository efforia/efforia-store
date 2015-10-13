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

                        url(_(r'^hub/howitworks'), TemplateView.as_view(template_name='howitworks.html'), name='howitworks'),
                        url(_(r'^hub/whatisitfor'), TemplateView.as_view(template_name='whatisitfor.html'), name='whatisitfor'),
                        url(_(r'^hub/devices'), TemplateView.as_view(template_name='devices.html'), name='devices'),
                        url(_(r'^hub/apps'), TemplateView.as_view(template_name='apps.html'), name='apps'),
                        url(r'^hub/', TemplateView.as_view(template_name='pages/hub.html'), name='hub'),

                        url(_(r'^uses/personalcomputing'), TemplateView.as_view(template_name='personalcomputing.html'), name='personalcomputing'),
                        url(_(r'^uses/internetofthings'), TemplateView.as_view(template_name='internetofthings.html'), name='internetofthings'),
                        url(_(r'^uses/mediacenter'), TemplateView.as_view(template_name='mediacenter.html'), name='mediacenter'),
                        url(_(r'^uses/videogame'), TemplateView.as_view(template_name='videogame.html'), name='videogame'),
                        url(_(r'^uses/server'), TemplateView.as_view(template_name='server.html'), name='server'),
                        url(_(r'^hubpro/'), TemplateView.as_view(template_name='pages/hubpro.html'), name='uses'),

                        url(_(r'^support/documentation'), TemplateView.as_view(template_name='documentation.html'), name='documentation'),
                        url(_(r'^support/developer'), TemplateView.as_view(template_name='developer.html'), name='developer'),
                        url(_(r'^support/services'), TemplateView.as_view(template_name='services.html'), name='services'),
                        url(_(r'^support/warranty'), TemplateView.as_view(template_name='warranty.html'), name='warranty'),
                        url(_(r'^support/'), TemplateView.as_view(template_name='support.html'), name='support'),

                        url(_(r'^about/opensource'), TemplateView.as_view(template_name='opensource.html'), name='opensource'),
                        url(_(r'^about/localization'), TemplateView.as_view(template_name='localization.html'), name='localization'),
                        url(_(r'^about/partners'), TemplateView.as_view(template_name='partners.html'), name='partners'),
                        url(_(r'^about/'), TemplateView.as_view(template_name='about.html'), name='about'),

                        url(u'^$', TemplateView.as_view(template_name='index.html'), name=u'home'),
						url("^$", "mezzanine.pages.views.page", {"slug": "/"}, name="home"),
                        (u'^', include(u'mezzanine.urls'))
)

handler404 = u'mezzanine.core.views.page_not_found'
handler500 = u'mezzanine.core.views.server_error'
