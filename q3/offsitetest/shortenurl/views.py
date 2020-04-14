# Create your views here.
from rest_framework import viewsets, status
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from django.shortcuts import redirect
import json


from shortenurl.models import Url
from shortenurl.serializers import UrlSerializer
from shortenurl.handler import Handler


# Create your views here.
class UrlViewSet(viewsets.ModelViewSet):
    queryset = Url.objects.all()
    serializer_class = UrlSerializer
    parser_classes = (JSONParser,)
    

    def getorgurl(request, **kwargs):
        path=request.path.replace("/","")
        originalurl=Handler.get_originalurl(path)
        print(originalurl)
        #return JsonResponse({'url': originalurl}, status=200)
        return redirect(originalurl)

    def shortenurl(request, **kwargs):
        client_ip = request.environ.get('REMOTE_ADDR')
        print(client_ip)
        handler.ratelimit(ip)
        value=handler.checkRate(client_ip)
        print(value)
        json_body = json.loads(request.body)
        originalurl=json_body['url'].strip()
        path=Handler.short_url(originalurl)
        print(path)
        shorturl=Handler.get_full_url(request, path)
        return JsonResponse({'url': originalurl, 'shortenUrl': shorturl}, status=201, content_type="'application/json")
