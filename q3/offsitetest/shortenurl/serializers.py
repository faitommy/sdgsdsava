from rest_framework import serializers
from shortenurl.models import Url

class UrlSerializer(serializers.ModelSerializer):

   class Meta:
       model = Url
       fields = ('shortenurl','gurl')

