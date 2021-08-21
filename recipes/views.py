from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views import generic
import urllib.request
import json
from django.conf import settings
import requests
import random

def recipes_list(request):
    if request.method == 'POST':
        recipe = request.POST.get('recipe', None)
        API_KEY = random.choice(settings.API_KEY)
        rqs = requests.get(f"https://api.spoonacular.com/recipes/search?query={recipe}&apiKey={API_KEY}&number=9")
        json_data = rqs.json()
        data = {'results':[]}
        for i in range(len(json_data)-1):
            img_format = json_data['results'][0]['image'].split('.')
            datatemp = {
                'name': json_data['results'][0]['title'],
                'id': json_data['results'][0]['id'],
                'readyInMinutes': json_data['results'][0]['readyInMinutes'],
                'sourceUrl': json_data['results'][0]['sourceUrl'],
                'image': 'https://spoonacular.com/recipeImages/'+str(json_data['results'][0]['id'])+'-'+'636x393.'+img_format[1],
                }
            data['results'].append(datatemp)
        return render(request, 'recipes.html', {'data':json_data,'recipe':recipe})
    else:
        data = {}
        return render(request, 'landing.html', {'data':data,})

def recipe_detail(request, id):
    if request.method == 'POST':
        recipe = request.POST.get('recipe', None)
        API_KEY = random.choice(settings.API_KEY)
        rqs = requests.get(f"https://api.spoonacular.com/recipes/search?query={recipe}&apiKey={API_KEY}&number=9")
        json_data = rqs.json()
        data = {'results':[]}
        for i in range(len(json_data)-1):
            img_format = json_data['results'][0]['image'].split('.')
            datatemp = {
                'name': json_data['results'][0]['title'],
                'id': json_data['results'][0]['id'],
                'readyInMinutes': json_data['results'][0]['readyInMinutes'],
                'sourceUrl': json_data['results'][0]['sourceUrl'],
                'image': 'https://spoonacular.com/recipeImages/'+str(json_data['results'][0]['id'])+'-'+'636x393.'+img_format[1],
                }
            data['results'].append(datatemp)
        return render(request, 'recipes.html', {'data':json_data,'recipe':recipe})

        
    rqs = requests.get(f'https://api.spoonacular.com/recipes/{id}/information?includeNutrition=false&apiKey={settings.API_KEY}')

    json_data = rqs.json()
    data = {
        'title': json_data['title'],
        'readyInMinutes': json_data['readyInMinutes'],
        'image': json_data['image'],
        'ingredients': [],
        'instructions': [],
        'message': [],
        'instructions_url': []
    }
    
    for i in range(len(json_data['extendedIngredients'])-1):
        ingrediant_data = {
            'name': json_data['extendedIngredients'][i]['originalString'],
            'image': json_data['extendedIngredients'][i]['image'],
        }
        data['ingredients'].append(ingrediant_data)

    if len(json_data['analyzedInstructions']) != 0:
        for i in range(len(json_data['analyzedInstructions'][0]['steps']) -1):
            instructions_data = {
                'step': json_data['analyzedInstructions'][0]['steps'][i]['step']
            }  
            data['instructions'].append(instructions_data)
        sourceUrl = json_data['sourceUrl']
        data['message'].append('For more details and to know more about the recipe\'s instructions, check the official\'s recipe website ')
        data['instructions_url'].append(sourceUrl)

    else:
        sourceUrl = json_data['sourceUrl']
        data['message'].append('Please check the recipe\'s official website for the instructions.')
        data['instructions_url'].append(sourceUrl)

    return render(request, 'recipe_detail.html', {'data':data, 'instructions':data['instructions'],'instructions_url': data['instructions_url'][0],'message': data['message'][0]})


def ingredients_search(request):

    if request.method == 'POST':
        ingredients = request.POST.get('ingredients', None)
        ingredientsSplit = ingredients.split(' ')
        fullIngredients = ',+'.join(ingredientsSplit)
        iNGREDIANTS = ' '.join(ingredientsSplit)
        rqs = requests.get(f"https://api.spoonacular.com/recipes/findByIngredients?ingredients={fullIngredients}&apiKey={settings.API_KEY}&number=15")
        # json_data = json.loads(rqs)
        json_data = rqs.json()
        data = {'results':[]}
        for i in range(len(json_data)-1):
            img_format = json_data[i]['imageType']
            datatemp = {
                'title': json_data[i]['title'],
                'id': json_data[i]['id'],
                'image': str(json_data[i]['id'])+'-'+'636x393.'+img_format,
                }
            data['results'].append(datatemp)
        ingredient_search = True
        return render(request, 'recipes.html',{'data':data, 'ingredient_search':ingredient_search,'ingredientss':iNGREDIANTS})
    else:
        data = {}
        ingredient_search = True
        return render(request, 'ingredients_search.html', {'data':data,'ingredient_search':ingredient_search})


def handle_or_404(request, exception):
    return render(request, '404.html')

def handle_or_500(request):
    return render(request, '500.html')
