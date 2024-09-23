from django.urls import path
from rest_framework.routers import SimpleRouter

from dogs.views import (DogViewSet, BreedCreateAPIView,
                        BreedListAPIView, BreedUpdateAPIView,
                        BreedDestroyAPIView, BreedRetrieveAPIView)
from dogs.apps import DogsConfig

# проводим стандартные настройки. Указываем приложение, импортируем из dogs.apps.DogsConfig
app_name = DogsConfig.name

# присваиваем экземпляр класса
router = SimpleRouter()
# прописывем путь, по которому будет в пустом пути '', показываться DogsViewSet
router.register('', DogViewSet)


urlpatterns = [
    path('breeds/', BreedListAPIView.as_view(), name='breeds_list'),
    path('breeds/<int:pk>', BreedRetrieveAPIView.as_view(), name='breed_retrieve'),
    path('breeds/create/', BreedCreateAPIView.as_view(), name='breed_create'),
    path('breeds/<int:pk>/update/', BreedUpdateAPIView.as_view(), name='breed_update'),
    path('breeds/<int:pk>/delete/', BreedDestroyAPIView.as_view(), name='breed_delete')
    # path('api-auth/', include('rest_framework.urls')),  # для авторизации через API
]
# к urlpatterns добавляем наши urls
urlpatterns += router.urls
