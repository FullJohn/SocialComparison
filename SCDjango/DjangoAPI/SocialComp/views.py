
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from rest_framework.utils import json

from SocialComp.models import PostModel, QueryModel
from SocialComp.serializers import PostSerializer, QuerySerializer

from .collection import collections


# Create your views here.
@csrf_exempt
def postAPI(request,id=0):
    
    
    jsonData = JSONParser().parse(request)
    get_posts = jsonData.get('getPosts')
    
    if request.method=='GET' or get_posts==True:
        queryId = jsonData.get('queryId')
        if queryId == "all":
            posts = PostModel.objects.all()
        else:
            posts = PostModel.objects.filter(QueryId=queryId)
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
        print(query_data, type(query_data))
        query_serializer = QuerySerializer(data = query_data)
        if query_serializer.is_valid():
            query_serializer.save()
            
            queryId = query_serializer['QueryId'].value
    
            return JsonResponse({'message':"Added Query Successfully", 'redirect': True, 'queryId': queryId}, safe=False)

        return JsonResponse({'message':"Please fill out all the forms", 'redirect': False}, status=500, safe=False)

    elif request.method == 'DELETE':
        query = QueryModel.objects.get(QueryId = id)
        query.delete()
        return JsonResponse("Deleted Query Successfully", safe=False)


@csrf_exempt
def runQuery(request):

    if request.method == 'POST':
        query_id = int(JSONParser().parse(request).get('queryId'))
        query = QueryModel.objects.get(QueryId = query_id)
        platform = query.platform
        brands = [query.brand1, query.brand2, query.brand3]
        date_range = [query.startDate, query.endDate]
        collections.run_collection(platform, brands, date_range, query_id)
        return JsonResponse({'message':"Success", 'redirect': True}, safe=False)
