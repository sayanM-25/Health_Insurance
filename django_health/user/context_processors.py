from .models import Tbl_user

def user_list(request):
    user = Tbl_user.objects.all()
    return {'user_list': user}