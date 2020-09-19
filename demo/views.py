from django.shortcuts import render, HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import json
from django.conf import settings
import redis

redis_instance = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)

@api_view(["GET", "POST"])
def manage_keys(request):
    if request.method == "GET":
        items = {}
        count = 0
        for key in redis_instance.keys("*"):
            items[key.decode("utf-8")] = redis_instance.get(key)
            count +=1
        return Response({
            "count": f"{count} keys found",
            "message": "success",
            "items": items
        }, status=status.HTTP_200_OK)
    if request.method == "POST":
        # key = list(request.data.keys())[0]
        # redis_instance.set(key, request.data[key])
        key = list(json.loads(request.body).keys())[0]
        redis_instance.set(key, json.loads(request.body)[key])
        return Response({
            "message": f"Successfully set {key} to {json.loads(request.body)[key]} "
        }, status = status.HTTP_200_OK)


@api_view(["GET","PATCH","DELETE"])
def manage_key(request, key=None):
    if request.method == "GET":
        if key:
            found = {}
            for i in redis_instance.keys("*"):
                if i.decode("utf-8") == key:
                    found[i.decode("utf-8")] = redis_instance.get(key)
                    return Response({ "found": True, "answer": found}, status = status.HTTP_200_OK)
            if found == {}:
                return Response({"found": False}, status = status.HTTP_400_BAD_REQUEST) 
        else:
            return Response({"message": "No keys provides"}, status = status.HTTP_400_BAD_REQUEST)

    if request.method == "DELETE":
        if key:
            found = None
            for i in redis_instance.keys("*"):
                if i.decode("utf-8") == key:
                    found = True
            if found:
                redis_instance.delete(key)
                return Response({"message": f"successfully deleted key: {key}"}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "That key hasn't been found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"message": "No keys provides"}, status = status.HTTP_400_BAD_REQUEST)

    if request.method == "PATCH":
        if key:
            body_key = (list((json.loads(request.body)).keys()))[0]
            for i in redis_instance.keys("*"):
                if i.decode("utf-8") == key:
                    redis_instance.set(key, json.loads(request.body)[body_key])
                    return Response({"message": f"successfull changed {key}'s' value to {(json.loads(request.body))[body_key]} "}, status= status.HTTP_200_OK)        
            return Response({"message": "Your requested key is not found"})    
        else:
            return Response({"message": "Key not provided"}, status = status.HTTP_400_BAD_REQUEST)