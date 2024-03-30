from django.http import HttpResponse
from django.shortcuts import render
import json
from .models import Blogpost
from datetime import date



def index(request):
    myposts = Blogpost.objects.all()
    return render(request,"blog/index.html",
                  {'myposts':myposts})
def blogpost(request,id):
    post=Blogpost.objects.filter(post_id=id)[0]
    return render(request,"blog/blogpost.html",{'post':post})

def createpost(request):
    print("Yahaan Tak To Aa Raha Hai")
    if request.method=="POST":
        print("HO GYA")    
        title=    request.POST.get('title','')
        head0=    request.POST.get('head0','')
        chead0=   request.POST.get('chead0','')
        head1=    request.POST.get('head1','')
        chead1=   request.POST.get('chead1','')
        thumbnail=request.POST.get('thumbnail','')
        # post = Blogpost(request.POST,request.FILES)
        post = Blogpost(title=title,head0=head0,chead0=chead0,head1=head1,chead1=chead1,pub_date=date.today(),thumbnail=thumbnail)
        print(thumbnail)
        post.save()
        print("Saved")
    return render(request,"blog/createpost.html")
    
    