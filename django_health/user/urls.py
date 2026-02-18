from django.urls import path
from .views import *
urlpatterns = [
    path('homepage/', homepage , name="homepage"),
    path('login/', user_login , name="login"),
    path('logout/', user_logout, name="logout"),
    path('admindash/', admindash , name="admindash"),
    path('dashboard/', dashboard , name="dashboard"),
    path('register/', register , name="register"),
    path('addplan/', add_plan , name="addplan"),
    path('update/<int:userid>/', update_plan, name='updateplan'),
    path('confirmdelete/<int:userid>/', delete_plan, name='confirmdelete'),

    path('changeprofile/', change_profile , name="changeprofile"),
    path('cart/', cart, name='cart'),
    path('addtocart/<int:plan_id>/', add_to_cart, name='addtocart'),
    path('removefromcart/<int:plan_id>/', remove_from_cart, name='removefromcart'),

    path('addfamily/', add_family_member, name='addfamily'),
    path('removefromfamily/<int:member_id>/', remove_family_member, name='removefromfamily'),

    path('invoice/<int:transaction_id>/', invoice, name='invoice'),
    path('payment/', create_payment, name='payment'),
    path('paymentexecute/', execute_payment, name='paymentexecute'),
    path('paymentcancel/', cancel_payment, name='paymentcancel'),
    path('transaction/', transaction_history, name='transaction'),
    path('admintran/', admin_tran, name='admintran'),
    path('expiredpolicy/', expired_policy, name='expiredpolicy'),
    path('aboutus/', about_us ,name='aboutus'),

    path('managecustomers/', manage_customers ,name='managecustomers'),
    path('manageinsurance/', manage_insurance ,name='manageinsurance'),
    path('expiredplans/', expired_plans ,name='expiredplans'),
    path('deactivate/<int:user_id>/', deactivate_user, name='deactivateuser'),





]