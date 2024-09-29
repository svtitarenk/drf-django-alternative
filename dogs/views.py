from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView

from dogs.models import Dog, Breed
from dogs.serializers import DogSerializer, BreedSerializer, DogDetailSerializer


class DogViewSet(ModelViewSet):
    queryset = Dog.objects.all()
    # добавляем сортировку
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    # указываем поля для фильтрации из django-filters (DjangoFilterBackend)
    # меняем список на кортеж [] -> ()
    filterset_fields = ('breed',)
    # добавялем поля для сортировки
    ordering_fields = ('date_born',)
    search_fields = ('name',)

    # Сериализаторы нужны, чтобы обрабатывать данные из БД в формат, который мы будем выводить
    # serializer_class = DogSerializer

    # переопределяем и проверяем. Если у нас действие retrieve, то мы выводим DogDetailSerializer
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return DogDetailSerializer
        return DogSerializer


# Делаем CRUD классы для пород
class BreedCreateAPIView(CreateAPIView):
    queryset = Breed.objects.all()
    serializer_class = BreedSerializer


class BreedListAPIView(ListAPIView):
    queryset = Breed.objects.all()
    serializer_class = BreedSerializer


class BreedRetrieveAPIView(RetrieveAPIView):
    queryset = Breed.objects.all()
    serializer_class = BreedSerializer


class BreedUpdateAPIView(UpdateAPIView):
    queryset = Breed.objects.all()
    serializer_class = BreedSerializer


class BreedDestroyAPIView(DestroyAPIView):
    queryset = Breed.objects.all()
    serializer_class = BreedSerializer
