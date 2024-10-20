from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView, \
    get_object_or_404

from dogs.models import Dog, Breed
from dogs.paginations import CustomPagination
from dogs.serializers import DogSerializer, BreedSerializer, DogDetailSerializer
from dogs.tasks import send_information_about_like
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

    @action(detail=True, methods=('post',))
    def likes(self, request, pk):
        """
            Описываем логику для likes. Если был лайк, то удаляем, если нет, тогда добавляем.
            получаем в serializer сохраненную собаку и передаем ее в Response

            Декоратор у нас называется @action (импортируем его из from rest_framework.decorators import action)
            В декоратор передаем параметр detail=True, потому что у нас страница будет одной собаки, а не списком.
            В декоратор передаем methods=('post',)

            :param pk: т.к. работать будем с одной собакой
            :param request: из запроса заберем user
            :return: Response с сохраненным лайком
            :imports: (from rest_framework.response import Response,
                from rest_framework.generics import get_object_or_404)

        """

        # опишем логику. Используем get_404, он вернет или объект или статус собака не найдена
        dog = get_object_or_404(Dog, pk=pk)
        # мы получили собаку, дальше проверяем
        if dog.likes.filter(pk=request.user.pk).exists():
            # если у нас лайк поставлен этим же пользователем, тогда мы этот лайк удаляем.
            dog.likes.remove(request.user)
        else:
            # если у нас пользователь не ставил лайк собаке, тогда мы ему добавляем лайк. Метод add
            dog.likes.add(request.user)
            # from dogs.tasks import send_information_about_like (здесь наша таска на отправку письма)
            send_information_about_like.delay(dog.owner.email)
        # получаем в serializer сохраненную собаку и передаем ее в Response
        serializer = self.get_serializer(dog)
        # from rest_framework.response import Response
        return Response(data=serializer.data)


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
