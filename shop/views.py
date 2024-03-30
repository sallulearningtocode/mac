from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test
from .models import Product,Contact,Orders,OrderUpdate
from math import ceil
import json
from datetime import date
from django.views.decorators.csrf import csrf_exempt
from PayTm import Checksum
def about(request):
    return render(request,"shop/aboutus.html")



def addProduct(request):
    print("Reached addProduct")
    if (request.method=='POST'):
        product_name=request.POST.get('product_name','')
        category=request.POST.get('category','')
        subcategory=request.POST.get('subcategory','')
        price=request.POST.get('price')
        print("Product Details :-  "+product_name+"\n"+category+"\n"+subcategory+"\n"+price)
        desc=request.POST.get('desc','')
        product=Product(product_name=product_name,category=category,
                subcategory=subcategory,price=price,desc=desc,pub_date=date.today())
        if product:
            render(request,"shop/addProduct.html",{'success':"Product Added Successfully"})
        product.save()
    return render(request,"shop/addProduct.html")

def contactus(request):
    thank=False
    if(request.method=="POST"):
        name=request.POST.get('name','')
        email = request.POST.get('email','')
        phone = request.POST.get('phone','')
        desc =  request.POST.get('desc','')
        contact = Contact(name=name,email=email,phone=phone,desc=desc)
        contact.save()
        thank=True

    return render(request,"shop/contactus.html",{'thank':thank})


def productview(request,myid):
    product=Product.objects.filter(id=myid)
    print(product)
    return render(request,"shop/productview.html",{'product':product[0]})

def searchMatch(query,item):
    if query in item.desc.lower() or query in item.product_name.lower() or query in item.category.lower():
        return True
    else:
        return False

def search(request):

    showcartandsearch=True
    query = request.GET.get('search').lower()
    allProds=[]
    catprods = Product.objects.values('category','id')
    cats={item['category'] for item in catprods}
    for cat in cats:

        prodtemp = Product.objects.filter(category = cat)
        prod = [item for item in prodtemp if searchMatch(query,item)]
        n=len(prod)
        nSlides = n//4+ceil(n/4)-(n//4)
        if len(prod)!=0:
            allProds.append([prod, range(1,nSlides), nSlides])


    length=len(allProds[0][0])  
    params = {'allprods':allProds,"msg":'','showcartandsearch':showcartandsearch,'length':length}

    if len(allProds) == 0 or len(query)<4:
        params = {'msg': "No results for"+ " "+" '"+ query+"' " +"" +" Try checking your spelling or use more general terms"}

    print("Absolutely Fine")
    return render(request,"shop/search.html",params)


def tracker(request):
    if(request.method=="POST"):
        orderid=request.POST.get('orderid','')
        email=request.POST.get('email','')
        try:
            order = Orders.objects.filter(order_id=orderid, email=email)
            print(len(order))
            if len(order)>0:
                update = OrderUpdate.objects.filter(order_id=orderid)
                updates = []
                for  item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps({"status":"success","updates":updates, "itemsJson":order[0].item_json}, default=str)
                return HttpResponse(response) 
            else:
                return HttpResponse('{"status":"no item"}')

        except Exception as e:
            return HttpResponse('{"status":"error"} ')
        
    return render(request,"shop/tracker.html")


def index(request):

    allProds=[]
    catprods=Product.objects.values('category','id')
    cats={item['category'] for item in catprods}
    for cat in cats:
        prod=Product.objects.filter(category=cat)
        n=len(prod) 
        nSlides=n//4+ceil((n/4)-(n//4))
        allProds.append([prod,range(1,nSlides),nSlides])
    params={'allProds':allProds}
    return render(request,"shop/index.html",params)


def checkout(request):
    if(request.method=="POST"):
        item_json = request.POST.get('itemsJson','') 
        name=request.POST.get('name','')
        amount=request.POST.get('amount','')
        email = request.POST.get('email','')
        address =  request.POST.get('address1','') +" "+ request.POST.get('address2','')
        city =  request.POST.get('city','')
        state =  request.POST.get('state','')
        zip_code =  request.POST.get('zip_code','')
        phone = request.POST.get('phone','')
        order = Orders(item_json=item_json,name=name,email=email,address=address,
                       city=city,state=state,zip_code=zip_code,phone=phone,amount=amount)
        order.save()
        update = OrderUpdate(order_id=order.order_id, 
                             update_desc = "The Order has been placed")
        update.save()
        id=order.order_id    
        thank=True
        return render(request,"shop/checkout.html",{'thank':thank,'id':id})
    print("rendered Paytm.html Successfully")
    return render(request,'shop/checkout.html')


@csrf_exempt
def handlerequest(request):
    # paytm will send you post request here
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        print(i+'='+form[i])
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('order successful')
        else:
            print('order was not successful because' + response_dict['RESPMSG'])
    return render(request, 'shop/paymentstatus.html', {'response': response_dict})

def cart(request):
    products=Product.objects.values('id')
    allprods={item['id'] for item in products}
    for allprod in allprods:
        allprods.append([products,range(1,len(products))])

    return render(request,"shop/cart.html",{'allprods':allprods})