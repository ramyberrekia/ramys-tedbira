from django.urls import path 
from . import views

app_name = 'recipes'

urlpatterns = [
	path('',views.recipes_list,name='get_recipes_view'),
	path('<int:id>/',views.recipe_detail,name='get_recipes_list'),
	path('search_by_ingredients/',views.ingredients_search ,name='search_by_ingredients'),
]