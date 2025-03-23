from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'persons', views.PersonAPIViewSet)

urlpatterns = [
    path('', views.PersonListView.as_view(), name='person_list'),
    path('person/<int:pk>/', views.PersonDetailView.as_view(), name='person_detail'),
    path('person/new/', views.PersonCreateView.as_view(), name='person_create'),
    path('person/<int:pk>/edit/', views.PersonUpdateView.as_view(), name='person_edit'),
    path('tree/', views.TreeView.as_view(), name='tree_view'),
    path('api/', include(router.urls)),
    path('api/persons/', views.PersonAPIViewSet.as_view({'get': 'list', 'post': 'create'}), name='person-list'),
    path('api/persons/<int:pk>/', views.PersonAPIViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='person-detail'),
    path('api/persons/<int:pk>/update_relations/', views.PersonAPIViewSet.as_view({'post': 'update_relations'}), name='person-update-relations'),
    path('tree/', views.tree_view, name='tree-view'),
] 