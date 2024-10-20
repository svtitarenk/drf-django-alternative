from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView

from dogs.models import Dog, Breed
from dogs.paginations import CustomPagination
from dogs.serializers import DogSerializer, BreedSerializer, DogDetailSerializer
from users.permissions import IsModer, IsOwner


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
    pagination_class = CustomPagination

    # Сериализаторы нужны, чтобы обрабатывать данные из БД в формат, который мы будем выводить
    # serializer_class = DogSerializer

    # переопределяем и проверяем. Если у нас действие retrieve, то мы выводим DogDetailSerializer
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return DogDetailSerializer
        return DogSerializer

    def perform_create(self, serializer):
        dog = serializer.save()
        dog.owner = self.request.user
        dog.save()

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = (~IsModer,)
        elif self.action in ['update', 'retrieve']:
            self.permission_classes = (IsModer | IsOwner,)
        elif self.action == 'destroy':
            self.permission_classes = (IsOwner | ~IsModer,)  # не модератор и владелец
        return super().get_permissions()


# Делаем CRUD классы для пород
class BreedCreateAPIView(CreateAPIView):
    queryset = Breed.objects.all()
    serializer_class = BreedSerializer
    # permission_classes = (~IsModer,)  # проверка на то, что пользователь не модератор.
    # поскольку мы переопределили permission на уровне класса, то permission на уровне проекта уже не работает
    permission_classes = (~IsModer, IsAuthenticated)

    def perform_create(self, serializer):
        """ Присваиваем владельца собаке """
        breed = serializer.save()
        breed.owner = self.request.user
        breed.save()


class BreedListAPIView(ListAPIView):
    queryset = Breed.objects.all()
    serializer_class = BreedSerializer
    pagination_class = CustomPagination


class BreedRetrieveAPIView(RetrieveAPIView):
    queryset = Breed.objects.all()
    serializer_class = BreedSerializer
    permission_classes = (IsAuthenticated, IsModer | IsOwner,)


class BreedUpdateAPIView(UpdateAPIView):
    queryset = Breed.objects.all()
    serializer_class = BreedSerializer
    permission_classes = (IsAuthenticated, IsModer | IsOwner,)


class BreedDestroyAPIView(DestroyAPIView):
    queryset = Breed.objects.all()
    serializer_class = BreedSerializer
    permission_classes = (IsAuthenticated, IsOwner | ~IsModer,)
