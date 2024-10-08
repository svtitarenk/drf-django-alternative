from rest_framework import permissions


class IsModer(permissions.BasePermission):
    message = 'You are not a member of group "moders".'

    """ Проверяет, является ли пользователь модератором. """

    def has_permission(self, request, view):
        return request.user.groups.filter(name="moders").exists()

    def __srt__(self):
        return f'{self.request.user.groups.filter(name="moders").exists()}'


# меняем название из документации на то, что от нас просят. IsOwner
class IsOwner(permissions.BasePermission):
        """
        Object-level permission to only allow owners of an object to edit it.
        Assumes the model instance has an `owner` attribute.
        """

        """ Проверяет, является ли пользователь владельцев объекта """

        def has_object_permission(self, request, view, obj):
            # мы проверяем, если владелец объекта равен request юзер, тогда возвращаем True
            if obj.owner == request.user:
                return True
            return False
