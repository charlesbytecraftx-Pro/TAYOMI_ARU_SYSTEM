import csv
from django.contrib import admin
from django.db.models import Sum
from django.utils.html import format_html
from django.http import HttpResponse
from .models import ContributionType, Payment, Profile

# 1. Profile Admin (Ili uweze kuona namba za simu na picha za wanachama)
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'department', 'thumbnail')
    search_fields = ('user__username', 'phone_number')

    def thumbnail(self, obj):
        if obj.profile_pic:
            return format_html('<img src="{}" width="40" height="40" style="border-radius: 50%;" />', obj.profile_pic.url)
        return "No Image"
    thumbnail.short_description = 'Picha'

# 2. Contribution Type Admin
@admin.register(ContributionType)
class ContributionTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'base_amount', 'description')
    search_fields = ('name',)

# 3. Malipo (Payment) Admin yenye Export na Takwimu
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('member', 'contribution_type', 'amount', 'status', 'picha_ya_risiti', 'verified_by', 'date_paid')
    list_filter = ('status', 'contribution_type', 'date_paid', 'verified_by')
    search_fields = ('member__username', 'reference_number', 'contribution_type__name')
    list_editable = ('status',)
    ordering = ('-id',)
    readonly_fields = ('date_paid', 'verified_by', 'preview_receipt')
    
    # Action ya ku-export kwenda Excel (CSV)
    actions = ["export_as_csv"]

    def picha_ya_risiti(self, obj):
        if obj.receipt_image:
            return format_html('<img src="{}" style="width: 45px; height:45px; border-radius:5px;" />', obj.receipt_image.url)
        return "N/A"
    picha_ya_risiti.short_description = 'Picha'

    def preview_receipt(self, obj):
        if obj.receipt_image:
            return format_html('<a href="{0}" target="_blank"><img src="{0}" style="max-width: 300px; border: 2px solid #8e44ad;"/></a>', obj.receipt_image.url)
        return "Hakuna picha iliyopakiwa."
    preview_receipt.short_description = 'Uhakiki wa Risiti'

    def save_model(self, request, obj, form, change):
        if obj.status == 'Confirmed' and not obj.verified_by:
            obj.verified_by = request.user
        super().save_model(request, obj, form, change)

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)
        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response

        total_amount = qs.aggregate(total=Sum('amount'))['total'] or 0
        confirmed_amount = qs.filter(status='Confirmed').aggregate(total=Sum('amount'))['total'] or 0

        extra_context = extra_context or {}
        extra_context['total_amount'] = total_amount
        extra_context['confirmed_amount'] = confirmed_amount
        return super().changelist_view(request, extra_context=extra_context)

    # Function ya kutengeneza CSV
    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = ['member', 'contribution_type', 'amount', 'status', 'reference_number', 'date_paid']

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=Ripoti_ya_Malipo.csv'
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            writer.writerow([getattr(obj, field) for field in field_names])

        return response
    export_as_csv.short_description = "Pakua Ripoti (Excel/CSV)"

    fieldsets = (
        ('Taarifa za Mwanachama', {
            'fields': ('member', 'contribution_type', 'amount')
        }),
        ('Uthibitisho wa Malipo', {
            'fields': ('reference_number', 'receipt_image', 'preview_receipt', 'status', 'admin_comment', 'verified_by')
        }),
        ('Muda', {
            'fields': ('date_paid',)
        }),
    )
