from django.shortcuts import render
from notas.models import Notas, Categoria


def notas(request):
    notas = Notas.objects.all()
    return render(request, "notas/notas.html", {"notas": notas})


def categoria(request, categoria_id):
    categoria = Categoria.objects.get(id=categoria_id)  
    notas = Notas.objects.filter(categorias=categoria)  
    return render(request, "notas/categoria.html", {"categoria": categoria, "notas": notas})
