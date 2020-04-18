import hashlib
import logging
import random
import redis
import time

from shortenurl.models import Url

try:
    redis = redis.Redis(host='redis', port=6379, db=0, decode_responses=True)
except NameError:
    redis = None


class Handler():

    @staticmethod
    def short_url(originalurl):

        db_obj = Handler._get_or_create_in_db(originalurl)
        return db_obj.shorturl

    @staticmethod
    def _get_or_create_in_db(originalurl):

        md5hash = hashlib.md5(originalurl.encode('utf-8')).hexdigest()
        shorturl = md5hash[-9:]
        obj, created = Url.objects.update_or_create(shorturl=shorturl, originalurl=originalurl, defaults={'originalurl':originalurl})

        # handle collisions, make 10 attempts
        # shift left through the md5 if the 9 character code chosen so far is taken by a different url
        max_tries = 1
        while obj.originalurl != originalurl and max_tries<=10:
            shorturl = md5hash[-9-max_tries:-max_tries]
            obj, created = Url.objects.update_or_create(shorturl=shorturl, originalurl=originalurl, defaults={'originalurl':originalurl})
            max_tries += 1

        return obj

    @staticmethod
    def get_originalurl(shorturl):

        # attempt to lookup  Redis cache
        originalurl = Handler.redis_get(shorturl)
        if originalurl:
            return originalurl

        # not in Redis, fetch from database
        url = None
        try:
            url = Url.objects.get(shorturl=shorturl)
            # cache the response
            Handler.redis_set(shorturl, url.originalurl)
        except Url.DoesNotExist:
            logging.error ("Invalid url code")
            return None

        return url.originalurl
        
    @staticmethod
    def get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip 
        
    @staticmethod   
    def checkRate(ip):
        if redis.llen(ip) == 0:
            print("First encounter")
            i = 1
            redis.lpush(ip,1) 
            redis.expire(ip,60)
        else:
            if redis.llen(ip) == 5:
                return False
            else:
                redis.lpush(ip,1)
        return True


    @staticmethod
    def get_full_url(request,path):
        return  request.scheme + "://" +  request.get_host() + "/" + path


    @staticmethod
    def redis_get(key):
        global redis
        if redis:
            return redis.get(key)
        else:
            return None

    @staticmethod
    def redis_set(key, value):
        global redis
        if redis:
            redis.set(key, value)

