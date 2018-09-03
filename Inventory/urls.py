from django.conf.urls import url
from . import views

app_name='Inventory'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^stock/$', views.stockList, name='stockList'),
    url(r'^invoice_list/$', views.invoiceList, name='invoiceList'),
    url(r'^add/$', views.purchaseAdd, name='purchaseAdd'),
    url(r'^invoice/$', views.invoice, name='invoice'),
    url(r'^(?P<code_id>[0-9]+)/$', views.purchaseDetail, name='purchaseDetailView'),
    url(r'^order/(?P<code_id>[0-9]+)/$', views.orderDetail, name='orderDetail'),
    url(r'^company/$', views.companyView, name='CompanyView'),
    url(r'^company/add/$', views.companyAdd, name='CompanyAdd'),
    url(r'^products/add/$', views.productAdd, name='ProductAdd'),
    url(r'^products/$', views.productView, name='ProductView'),
    url(r'^products/(?P<code_id>[0-9]+)/$', views.productViewDetail,name='product_detail'),
    url(r'^company/(?P<code_id>[0-9]+)/$', views.companyDetailView, name='CompDetailView'),
    url(r'^products/stock/(?P<product_id>[0-9]+)/$', views.stockget, name='stockget'),
    url(r'^invoice/product_get/(?P<product_id>[0-9]+)/$', views.productGet, name='productget'),
    url(r'^company/(?P<code_id>[0-9]+)/delete/$', views.companyDelete, name='CompanyDelete'),
    url(r'^(?P<code_id>[0-9]+)/delete/$', views.purchaseDelete, name='PurchaseDelete'),
    url(r'^products/(?P<code_id>[0-9]+)/delete/$', views.productDelete, name='ProductDelete')
]