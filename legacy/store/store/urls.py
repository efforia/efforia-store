from __future__ import unicode_literals
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.conf.urls.static import static
from mezzanine.core.views import direct_to_template

admin.autodiscover()

urlpatterns = i18n_patterns(u'', (u'^admin/', include(admin.site.urls)))

urlpatterns += patterns(u'', 
                        (u'^shop/', include(u'cartridge.shop.urls')), 
			url(u'^store/slip', u'store.views.payment_slip'), 
			url(u'^store/bank', u'store.views.payment_bank'), 
                        url(u'^store/cancel', u'store.views.payment_cancel'), 
                        url(u'^store/execute', u'store.views.payment_execute', name=u'payment_execute'), 
                        url(u'^store/pay/(?P<order_id>\\d+)/$', u'store.views.payment_redirect', name=u'payment_redirect'), 
                        url(u'^account/orders/$', u'cartridge.shop.views.order_history', name=u'shop_order_history'), 
                        #url(u'^$', direct_to_template, {u'template': u'index.html'}, name=u'home'), 
						url("^$", "mezzanine.pages.views.page", {"slug": "/"}, name="home"),
                        (u'^', include(u'mezzanine.urls'))
)

handler404 = u'mezzanine.core.views.page_not_found'
handler500 = u'mezzanine.core.views.server_error'
