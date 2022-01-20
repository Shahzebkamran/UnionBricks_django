from django.contrib.admin.options import ModelAdmin
from api.forms import CustomUserCreationForm
from django.contrib import admin
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from api.models import Architect, Cart, Design, Item, Meeting, Order, OrderPayment, DesignPayment, MeetingPayment, Project, User


# Register your models here.
admin.site.site_title = "Unicon-Admin"
admin.site.site_header = "Unicon Admin Panel"
admin.site.index_title = "Welcome to admin panel"


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    model = User
    list_display = ('email', 'username', 'id',
                    'last_login', 'is_admin', 'is_staff')
    search_fields = ('email', 'username',)
    readonly_fields = ('date_joined', 'last_login')
    filter_horizontal = ()
    list_filter = ('first_name', 'email', 'last_login')
    fieldsets = ()

    add_fieldsets = (
        (None, {
            'classes': ('wide,'),
            'fields': ('email', 'username', 'password1', 'password2')}

         ),
    )


admin.site.register(User, CustomUserAdmin)


class ItemAdmin(ModelAdmin):
    model = Item
    list_display = ('name', 'id', 'type', 'price', 'stock')
    search_fields = ('name',)
    list_filter = ('price', 'stock',)


admin.site.register(Item, ItemAdmin)


class CartAdmin(ModelAdmin):
    model = Cart
    list_display = ('user_id', 'id',  'date')
    list_filter = ('items',)
    search_fields = ('user_id',)


admin.site.register(Cart, CartAdmin)


class OrderAdmin(ModelAdmin):
    model = Order
    list_display = ('user_id', 'id',  'date_placed', 'ship_date', 'status')
    list_filter = ('items', 'user_id', 'status')
    search_fields = ('user_id',)


admin.site.register(Order, OrderAdmin)


class OrderPaymentAdmin(ModelAdmin):
    model = OrderPayment
    list_display = ('id', 'order_id', 'amount',
                    'status', 'date')
    list_filter = ('date', 'status')
    search_fields = ('order_id',)


admin.site.register(OrderPayment, OrderPaymentAdmin)


class DesignPaymentAdmin(ModelAdmin):
    model = DesignPayment
    list_display = ('id', 'design_id', 'amount',
                    'status', 'date')
    list_filter = ('date', 'status')
    search_fields = ('design_id',)


admin.site.register(DesignPayment, DesignPaymentAdmin)


class MeetingPaymentAdmin(ModelAdmin):
    model = MeetingPayment
    list_display = ('id', 'meeting_id', 'amount',
                    'status', 'date')
    list_filter = ('date', 'status')
    search_fields = ('meeting_id',)


admin.site.register(MeetingPayment, MeetingPaymentAdmin)


class MeetingAdmin(ModelAdmin):
    model = Meeting
    list_display = ('id', 'time', 'title', 'client_id',
                    'client_name', 'status', 'fee')
    list_filter = ('status', 'client_name')
    search_fields = ('client_name',)


admin.site.register(Meeting, MeetingAdmin)


class DesignAdmin(ModelAdmin):
    model = Design
    list_display = ('id', 'client_id',
                    'client_name', 'arch_id', 'cost', 'status')
    list_filter = ('status', 'client_id')
    search_fields = ('date_placed',)


admin.site.register(Design, DesignAdmin)


class ArchitectAdmin(ModelAdmin):
    model = Architect
    list_display = ('email', 'username', 'id', 'experience', 'education')
    search_fields = ('email', 'username', 'experience', 'education',)
    readonly_fields = ('date_joined', 'last_login')
    filter_horizontal = ()
    list_filter = ('first_name', 'email', 'experience', 'education',)


admin.site.register(Architect, ArchitectAdmin)


class ProjectAdmin(ModelAdmin):
    model = Project
    list_display = ('id', 'title', 'client_id',
                    'client_name', 'percentage', 'cost', 'start_date', 'comp_date')
    list_filter = ('client_id', 'title', 'percentage',)
    search_fields = ('client_name', 'title',)


admin.site.register(Project, ProjectAdmin)
