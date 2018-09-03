from django.db import models

# Create your models here.

class Company(models.Model):
    code = models.CharField(primary_key=True,max_length=10)
    name = models.CharField(max_length=250)
    def __str__(self):
        return self.name

class Product(models.Model):
    company = models.ForeignKey(Company,on_delete=models.CASCADE,)
    code = models.CharField(primary_key=True, max_length=10)
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name

class Purchase(models.Model):
    code = models.ForeignKey(Product,default='001',related_name='product')
    company = models.ForeignKey(Company,related_name='company')
    Product_price = models.IntegerField(default=0)
    Purchase_price = models.IntegerField(default=0)
    stock = models.IntegerField(default=0)
    UNITS = (('KG','KiloGrams'),('G','Grams'),('Units', 'units'))
    units = models.CharField(max_length=25,choices=UNITS)
    date = models.DateTimeField()

    def __str__(self):
        return self.code.name

class Stock(models.Model):
    code = models.ForeignKey(Product)
    stock = models.IntegerField(default=0)
    unit = models.CharField(max_length=25)
    price = models.IntegerField(default=0)
    pur_price = models.IntegerField(default=0)

    def __str__(self):
        return str(self.stock)

class InvoiceDetail(models.Model):
    invoice_num = models.IntegerField(unique=True)
    date = models.DateTimeField()
    price = models.IntegerField(default=0)
    STATUS = (('UN','Unpaid'),('P','Paid'))
    status = models.CharField(max_length=5,choices=STATUS)
    cust_name = models.CharField(max_length=250)
    cust_add = models.CharField(max_length=500)

class Order(models.Model):
    invoice_id = models.ForeignKey(InvoiceDetail,db_column='invoice_num')
    order_id = models.IntegerField()
    item_id = models.ForeignKey(Product)
    qty = models.IntegerField(default=0)
    item_price = models.IntegerField()
    purchase_id = models.ForeignKey(Purchase)




