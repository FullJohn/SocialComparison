from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse

from SocialComp.models import PostModel, QueryModel
from SocialComp.serializers import PostSerializer, QuerySerializer

# Create your views here.
@csrf_exempt
def postAPI(request, id=0):
    if request.method=='GET':
        posts = PostModel.objects.all()
        post_serializer = PostSerializer(posts, many=True)
        return JsonResponse(post_serializer.data, safe=False)
    
    elif request.method == 'POST':
        post_data = JSONParser().parse(request)
        post_serializer = PostSerializer(data = post_data)
        if post_serializer.is_valid():
            post_serializer.save()
            return JsonResponse("Added Post Successfully", safe=False)
        return JsonResponse("Failed to Add Post", safe=False)

    elif request.method == 'DELETE':
        post = PostModel.objects.get(PostId = id)
        post.delete()
        return JsonResponse("Deleted Post Successfully", safe=False)

    """
    May implement later, for now don't need to update values
    elif request.method == 'PUT':
    """

@csrf_exempt
def queryAPI(request, id=0):
    if request.method == 'GET':
        query = QueryModel.objects.all()
        query_serializer = QuerySerializer(query, many=True)
        return JsonResponse(query_serializer.data, safe=False)

    elif request.method == 'POST':
        query_data = JSONParser().parse(request)
        query_serializer = QuerySerializer(data = query_data)
        if query_serializer.is_valid():
            query_serializer.save()
            return JsonResponse("Added Query Successfully", safe=False)
        return JsonResponse("Failed to Add Query", safe=False)

    elif request.method == 'DELETE':
        query = QueryModel.objects.get(QueryId = id)
        query.delete()
        return JsonResponse("Deleted Query Successfully", save=False)

