from django.shortcuts import render, get_object_or_404, redirect
from django.core import serializers
from django.http import HttpResponseRedirect, request, JsonResponse, HttpResponse
from django.urls import reverse
from django.contrib import messages
from django.contrib import messages
from django.utils import timezone
import json
from django import template
from .models import Company, Purchase, Product, Stock, InvoiceDetail, Order

register = template.Library()


@register.filter
def get_at_index(list, index):
    return list[index]


# Create your views here.
def uniqid():
    from time import time
    return int(time() % 1000000)


def stockList(request):
    stock = Stock.objects.all()
    context = {
        'stock': stock
    }
    return render(request, 'Inventory/stock.html', context)


def orderDetail(request, code_id):
    order_instance = Order.objects.filter(invoice_id=code_id)
    context = {
        'order': order_instance
    }
    return render(request, 'Inventory/order_detail.html', context)


def invoiceList(request):
    order_id = InvoiceDetail.objects.all()
    context = {
        'order': order_id
    }
    return render(request, 'Inventory/invoice_list.html', context)


def orderid():
    from time import time
    return int(time() % 100000)


def invoice(request):
    price = {}
    context = {
        'company': Company.objects.all(),
        'products': Product.objects.all(),
        'stock': Stock.objects.all(),

    }
    if request.method == "POST":
        invoice_data = {}
        order_data = {}
        total = 0
        for price in request.POST.getlist('total'):
            total = total + int(price)
        status = request.POST.get('status', )
        invoice_num = uniqid()
        date = timezone.now()
        cust_name = request.POST.get('cust_name', )
        cust_add = request.POST.get('cust_add', )
        print(total)
        print(status)
        print(invoice_num)
        print(date)
        print(cust_name)
        print(cust_add)

        try:
            InvoiceDetail.objects.create(invoice_num=invoice_num, date=date, price=total, status=status,
                                         cust_name=cust_name, cust_add=cust_add)
            print("INserted")
        except Exception as e:
            print(e)
        qty_list = []
        product = []
        stock = []
        mrp = []

        for mrps in request.POST.getlist('MRP'):
            mrp.append(mrps)

        for price in request.POST.getlist('price'):
            stock.append(price)
        for qty in request.POST.getlist('Qty'):

            for item in request.POST.getlist('product'):
                stock_update_instance = Stock.objects.get(code=item)
                stock_old = stock_update_instance.stock
                stock_new = stock_old - int(qty)
                Stock.objects.filter(code=item).update(stock=stock_new)

            qty_list.append(qty)
        count = 0
        for item in request.POST.getlist('product'):
            order_invoice = InvoiceDetail.objects.get(invoice_num=invoice_num)
            order_id = orderid()
            purchase_id = Purchase.objects.get(code=item)
            product_inst = Product.objects.get(code=item)
            product_name = product_inst.name

            product.append(product_name)

            print(purchase_id)
            print(order_invoice)
            print(order_id)
            try:
                Order.objects.create(invoice_id=order_invoice, order_id=order_id, item_id=product_inst,
                                     purchase_id=purchase_id, item_price=stock[count], qty=qty_list[count])

                print("Order Inserted")
            except Exception as e:
                print(e)
            count = count + 1
        print(mrp)
        invoice_data = {

            'invoice_id': invoice_num,
            'total': total,
            'qty': qty_list,
            'prod_name': product,
            'stocks': stock,
            'rate': mrp

        }
        print(json.dumps(invoice_data))
        return render(request, 'Inventory/invoice.html', {"invoice_json": json.dumps(invoice_data), "date": date,
                                                          'cust_name': cust_name,
                                                          'cust_add': cust_add,

                                                          })

    return render(request, 'Inventory/invoice_maker.html', context)


def productGet(request, product_id):
    data = {}
    stock_get = Stock.objects.filter(code=product_id)
    for obj in stock_get:
        data['avail'] = True
        data['stock'] = obj.stock
        data['units'] = obj.unit
        data['price'] = obj.price

    return JsonResponse(data)


def index(request):
    stock = Purchase.objects.all()
    return render(request, 'Inventory/index.html', {'stock': stock})


def companyDelete(request, product_id):
    instance = get_object_or_404(Company, code=product_id)
    instance.delete()
    messages.success(request, "Successfully Deleted")
    return redirect("Inventory:CompanyView")


def productDelete(request, code_id):
    instance = get_object_or_404(Product, code=code_id)
    instance.delete()
    messages.success(request, "Successfully Deleted")
    return redirect("Inventory:ProductView")


def productAdd(request):
    company_list = Company.objects.all().order_by('code')
    context = {'company': company_list}
    if request.method == "POST":
        code = request.POST.get('code', )
        name = request.POST.get('name', )
        company = request.POST.get('company', )
        comp_instance = Company.objects.get(code=company)
        try:
            Product.objects.create(code=code, company=comp_instance, name=name)
            messages.success(request, "Product Added")
        except:
            messages.error(request, "Code Already Exist")

        return HttpResponseRedirect(reverse('Inventory:ProductView'))

    return render(request, 'Inventory/product_add.html', context)


def stockget(request, product_id):
    data = {}
    stock_get = Stock.objects.filter(code=product_id)
    for obj in stock_get:
        data['avail'] = True
        data['stock'] = obj.stock
        data['units'] = obj.unit
        data['price'] = obj.price

    return JsonResponse(data)


def productViewDetail(request, code_id):
    instance = get_object_or_404(Stock, code=code_id)
    context = {
        'code': instance.code.code,
        'name': instance.code.name,
        'company': instance.code.company,
        'stock': instance.stock,
        'price': instance.price,
        'pur_price': instance.pur_price
    }
    if request.method == "POST":
        name = request.POST.get('name', )
        stock = request.POST.get('stock', )
        price = request.POST.get('price', )
        pur_price = request.POST.get('pur_price', )
        Stock.objects.filter(code=code_id).update(stock=stock, price=price, pur_price=pur_price)
        Product.objects.filter(code=code_id).update(name=name)
        company_list = Purchase.objects.all()
        return HttpResponseRedirect(reverse('Inventory:ProductView'))

    return render(request, 'Inventory/product_detail.html', context)


def companyAdd(request):
    if request.method == "POST":
        code = request.POST.get('code', )
        name = request.POST.get('name')
        try:
            Company.objects.create(code=code, name=name)
            messages.success(request, "Company Added")
        except:
            messages.error(request, "Code Already Exist")
        company_list = Company.objects.all()
        context = {'company': company_list}
        return HttpResponseRedirect(reverse('Inventory:CompanyView'))

    return render(request, 'Inventory/company_add.html')


def purchaseAdd(request):
    company = Company.objects.all().order_by('code')
    product = Product.objects.all().order_by('code')
    context = {'company': company,
               'product': product}
    if request.method == "POST":
        company = request.POST.get('company', )
        product = request.POST.get('product', )
        stock = request.POST.get('stock', )
        product_price = request.POST.get('price', )
        purchase_price = request.POST.get('purchase_price', )
        unit = request.POST['unit']
        comp_instance = Company.objects.get(code=company)
        pro_instance = Product.objects.get(code=product)
        date = timezone.now()

        try:
            purchase = Purchase.objects.create(code=pro_instance, units=unit, company=comp_instance,
                                               Product_price=product_price, Purchase_price=purchase_price, stock=stock,
                                               date=date)
            stock_get = Stock.objects.filter(code=pro_instance).values_list('stock', flat=True)
            if not stock_get:
                Stock.objects.create(code=pro_instance, stock=stock, unit=unit, price=product_price,
                                     pur_price=purchase_price)
            else:
                for obj in stock_get:
                    print(obj)
                    new_stock = int(obj) + int(stock)
                    Stock.objects.filter(code=pro_instance).update(stock=new_stock, price=product_price,
                                                                   pur_price=purchase_price)
                    print(new_stock)
                print("Successful")
            messages.success(request, "Purchase Added")
        except Exception as e:
            print(e)
            messages.error(request, "Code Already Exist")

        return HttpResponseRedirect(reverse('Inventory:index'))

    return render(request, 'Inventory/purchase_add.html', context)


def companyView(request):
    company_list = Company.objects.all().order_by('code')
    context = {'company': company_list}
    return render(request, 'Inventory/company.html', context)


def purchaseDetail(request, code_id):
    instance = get_object_or_404(Purchase, pk=code_id)
    context = {
        'pk': code_id,
        'code': instance.code.code,
        'name': instance.code.name,
        'company': instance.company.code,
        'company_name': instance.company.name,
        'stock': instance.stock,
        'price': instance.Product_price,
        'purchase_price': instance.Purchase_price,
        'unit': instance.get_units_display()
    }
    if request.method == "POST":
        stock = request.POST.get('stock', )
        price = request.POST.get('price', )
        unit = request.POST.get('unit', )
        date = timezone.now()
        purchase_price = request.POST.get('purchase_price', )
        Purchase.objects.filter(pk=code_id).update(stock=stock, Purchase_price=purchase_price, Product_price=price,
                                                   units=unit, date=date)
        product = Product.objects.filter(code=Purchase.objects.filter(pk=code_id).values('code'))

        Stock.objects.filter(code=product).update(stock=stock, unit=unit, price=price, pur_price=purchase_price)

        return HttpResponseRedirect(reverse('Inventory:index'))

    return render(request, 'Inventory/purchase_detail.html', context)


def purchaseDelete(request, code_id):
    instance = get_object_or_404(Purchase, pk=code_id)
    code = instance.code
    Stock.objects.filter(code=code).delete()
    instance.delete()
    messages.success(request, "successfully Deleted")
    return redirect("Inventory:index")


def productView(request):
    product_list = Product.objects.all()
    return render(request, 'Inventory/products.html', {'product': product_list})


def companyDetailView(request, code_id):
    instance = get_object_or_404(Company, pk=code_id)
    context = {
        'code': instance.code,
        'name': instance.name,
    }
    if request.method == "POST":
        code = request.POST.get('code', )
        name = request.POST.get('name', )
        print(code)
        print(name)
        Company.objects.filter(code=code_id).update(code=code, name=name)
        company_list = Company.objects.all()
        return HttpResponseRedirect(reverse('Inventory:CompanyView'))

    return render(request, 'Inventory/company_detail.html', context)
