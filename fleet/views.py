from django.shortcuts import render

# Cette fonction sert juste à afficher ta page HTML
def map_view(request):
    return render(request, 'fleet/map.html')