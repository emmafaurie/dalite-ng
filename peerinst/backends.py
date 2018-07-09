from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import PermissionDenied

class CustomPermissionsBackend(ModelBackend):
    """A custom auth backend to validate object-level permissions."""

    def has_perm(self, user_obj, perm, obj=None):

        if obj:
            try:
                if obj.user == user_obj:
                    # Has permission for _this_ object; proceed with normal permissions check
                    return super(CustomPermissionsBackend, self).has_perm(user_obj, perm)
                else:
                    # Prevent any further authentication checks
                    raise PermissionDenied
                    return False
            except:
                if user_obj.is_staff:
                    return super(CustomPermissionsBackend, self).has_perm(user_obj, perm)
                else:
                    raise PermissionDenied
                    return False
        else:
            return super(CustomPermissionsBackend, self).has_perm(user_obj, perm)
