from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Cette fonction sert juste à afficher ta page HTML
def map_view(request):
    return render(request, 'fleet/map.html')

@login_required # permet la redirection vers Login quand on n'est pas connecté
def map_view(request):
    return render(request, 'fleet/map.html')