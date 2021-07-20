from django import forms
from django.shortcuts import render
from .models import Time
from .forms import TimeForm, TimesModel
from django.contrib import messages

# Create your views here.
def index(request):
    aux = None
    serieA = Time.objects.filter(serie='A')
    serieB = Time.objects.filter(serie='B')

    context = {
        'serieA': serieA,
        'serieB': serieB
    }
    return render(request,'index.html', context)

def cadastro(request):
    form = TimesModel(request.POST or None)
    if str(request.method) == 'POST' :
        if form.is_valid():
            form.save()
            messages.success(request, 'Cadastro feito')
            form = TimeForm()
    else:
        messages.error(request,'Erro ao cadastrar')

    context = {
        'form' : form
    }
    return render(request,'cadastro.html', context)

# def product_new(request):
#     if request.method == 'POST':
#         form = ProductForm(request.POST)
#         if form.is_valid():
#             product = Product()
#             product.user = request.user
#             product.name = form.cleaned_data['name']
#             product.quantity = form.cleaned_data['quantity']
#             product.price = form.cleaned_data['price']
#             product.short_description = form.cleaned_data['short_description']
#             product.description = form.cleaned_data['description']
#             product.status = 'Active'
#             product.save()

#             categories = Category.objects.filter(id__in=request.POST.getlist('categories'))
#             if categories:
#                 for category in categories:
#                     product.categories.add(category)
#             return redirect('my_products')


#     form = ProductForm()

#     context = {
#         'form': form,
#     }
#     return render(request, 'portal/product_new.html', context)