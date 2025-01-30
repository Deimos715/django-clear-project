from django.shortcuts import render
from src.seo.models import MetaTag, Title

def index(request):
    current_url = request.path
    title = Title.objects.filter(url=current_url).first()
    metatag = MetaTag.objects.filter(url=current_url).first()

    return render(request, 'main/index.html',
                {'title': title,
                'metatag': metatag})
