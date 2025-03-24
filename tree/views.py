from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from .models import Person
from .forms import PersonForm
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core.exceptions import ValidationError
import logging
from django.middleware.csrf import get_token
from django.http import JsonResponse
from .serializers import PersonSerializer

logger = logging.getLogger(__name__)

# API views
class PersonAPIViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    search_fields = ['first_name', 'last_name', 'middle_name']

    def create(self, request, *args, **kwargs):
        try:
            logger.info(f"Creating person with data: {request.data}")
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            logger.info(f"Person created successfully: {serializer.data}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            logger.error(f"Validation error while creating person: {e}")
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error creating person: {e}")
            return Response({'detail': 'Ошибка при создании записи'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, *args, **kwargs):
        try:
            logger.info(f"Updating person {kwargs.get('pk')} with data: {request.data}")
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            logger.info(f"Person updated successfully: {serializer.data}")
            return Response(serializer.data)
        except ValidationError as e:
            logger.error(f"Validation error while updating person: {e}")
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error updating person: {e}")
            return Response({'detail': 'Ошибка при обновлении записи'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['post'])
    def update_relations(self, request, pk=None):
        try:
            person = self.get_object()
            parents = request.data.get('parents', [])
            children = request.data.get('children', [])
            spouse = request.data.get('spouse')

            # Проверяем существование родителей и детей
            existing_parents = Person.objects.filter(id__in=parents)
            existing_children = Person.objects.filter(id__in=children)

            if len(existing_parents) != len(parents):
                missing_parents = set(parents) - set(existing_parents.values_list('id', flat=True))
                return Response(
                    {'detail': f'Родители с ID {missing_parents} не найдены'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if len(existing_children) != len(children):
                missing_children = set(children) - set(existing_children.values_list('id', flat=True))
                return Response(
                    {'detail': f'Дети с ID {missing_children} не найдены'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Проверяем существование супруга
            if spouse:
                try:
                    existing_spouse = Person.objects.get(id=spouse)
                    # Проверяем, не является ли супруг самим человеком
                    if existing_spouse.id == person.id:
                        return Response(
                            {'detail': 'Человек не может быть супругом самому себе'},
                            status=status.HTTP_400_BAD_REQUEST
                        )
                except Person.DoesNotExist:
                    return Response(
                        {'detail': f'Супруг с ID {spouse} не найден'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                existing_spouse = None

            # Очищаем существующие связи
            person.parents.clear()
            person.children.clear()
            person.spouse = None

            # Устанавливаем новые связи
            person.parents.set(existing_parents)
            person.children.set(existing_children)
            person.spouse = existing_spouse

            serializer = self.get_serializer(person)
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Error updating relations: {e}")
            return Response(
                {'detail': 'Ошибка при обновлении связей'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

# Template views
class PersonListView(ListView):
    model = Person
    template_name = 'tree/person_list.html'
    context_object_name = 'persons'
    paginate_by = 12

    def get_queryset(self):
        queryset = Person.objects.all()
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(
                first_name__icontains=q
            ) | queryset.filter(
                last_name__icontains=q
            )
        return queryset

class PersonDetailView(DetailView):
    model = Person
    template_name = 'tree/person_detail.html'
    context_object_name = 'person'

class PersonCreateView(CreateView):
    model = Person
    form_class = PersonForm
    template_name = 'tree/person_form.html'
    success_url = reverse_lazy('person_list')

    def form_valid(self, form):
        messages.success(self.request, 'Человек успешно добавлен.')
        return super().form_valid(form)

class PersonUpdateView(UpdateView):
    model = Person
    form_class = PersonForm
    template_name = 'tree/person_form.html'
    success_url = reverse_lazy('person_list')

    def form_valid(self, form):
        messages.success(self.request, 'Информация успешно обновлена.')
        return super().form_valid(form)

class TreeView(ListView):
    model = Person
    template_name = 'tree/tree_view.html'
    context_object_name = 'persons'

def tree_view(request):
    return render(request, 'tree/tree.html')

@api_view(['GET'])
def get_csrf_token(request):
    return JsonResponse({'csrfToken': get_token(request)}) 