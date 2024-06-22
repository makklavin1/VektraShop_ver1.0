from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'user', 'status', 'created_at', 'updated_at']
    list_filter = ['status', 'created_at']
    search_fields = ['order_number', 'user__username']
    inlines = [OrderItemInline]
    actions = ['mark_as_in_progress', 'mark_as_awaiting_pickup', 'mark_as_completed']

    def mark_as_in_progress(self, request, queryset):
        queryset.update(status='in_progress')
    mark_as_in_progress.short_description = "Mark selected orders as In Progress"

    def mark_as_awaiting_pickup(self, request, queryset):
        queryset.update(status='awaiting_pickup')
    mark_as_awaiting_pickup.short_description = "Mark selected orders as Awaiting Pickup"

    def mark_as_completed(self, request, queryset):
        for order in queryset:
            order.status = 'completed'
            order.save()
            order.complete_order()  # Вызов метода для создания записи в истории покупок
    mark_as_completed.short_description = "Mark selected orders as Completed"
