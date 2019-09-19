from django.contrib import admin
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.core.mail import send_mail
import inspect
from django.utils.safestring import mark_safe
from django.urls import reverse

from order_management.models import Order as order_management_Order
from .models import RecordToBeApproved

from django.utils import timezone

def approve_records(modeladmin, request, queryset):
    """Approve records"""

    now_time = timezone.now()
    success_message = False
    warning_message = False
    
    # Collection records, except oligo
    collections_approval_records = queryset.filter(content_type__app_label='collection_management')

    for approval_record in collections_approval_records.exclude(content_type__model='oligo'):
        obj = approval_record.content_object
        if request.user.id in obj.formz_projects.all().values_list('project_leader__id', flat=True):
            model = obj._meta.model
            if approval_record.activity_type=='created':
                if obj.last_changed_approval_by_pi==False:
                    model.objects.filter(id=obj.id).update(created_approval_by_pi=True, last_changed_approval_by_pi=True, approval_by_pi_date_time=now_time, approval_user=request.user)
                else:
                    model.objects.filter(id=obj.id).update(created_approval_by_pi=True, approval_by_pi_date_time=now_time, approval_user=request.user)
            elif approval_record.activity_type=='changed':
                model.objects.filter(id=obj.id).update(last_changed_approval_by_pi=True, approval_by_pi_date_time=now_time, approval_user=request.user)
            approval_record.delete()
            success_message = True
        else:
            warning_message = True
    
    # Oligos
    oligo_approval_records = collections_approval_records.filter(content_type__model='oligo')
    if oligo_approval_records:
        if request.user.labuser.is_principal_investigator:
            model = oligo_approval_records[0].content_object._meta.model
            for oligo_approval_record in oligo_approval_records:
                obj = oligo_approval_record.content_object
                if oligo_approval_record.activity_type=='created':
                    if obj.last_changed_approval_by_pi==False:
                        model.objects.filter(id=obj.id).update(created_approval_by_pi=True, last_changed_approval_by_pi=True, approval_by_pi_date_time=now_time)
                    else:
                        model.objects.filter(id=obj.id).update(created_approval_by_pi=True, approval_by_pi_date_time=now_time)
                elif oligo_approval_record.activity_type=='changed':
                    model.objects.filter(id=obj.id).update(last_changed_approval_by_pi=True, approval_by_pi_date_time=now_time)
            oligo_approval_records.delete()
            success_message = True
        else:
            messages.error(request, 'You are not allowed to approve oligos')
    
    #Orders
    order_approval_records = queryset.filter(content_type__app_label='order_management')
    if order_approval_records:
        if request.user.labuser.is_principal_investigator:
            model = order_approval_records[0].content_object._meta.model
            order_ids = order_approval_records.values_list('object_id', flat=True)
            model.objects.filter(id__in=order_ids).update(created_approval_by_pi=True)
            order_approval_records.delete()
            success_message = True
        else:
            messages.error(request, 'You are not allowed to approve orders')
    
    if success_message:
        messages.success(request, 'The records have been approved')

    if warning_message:
        messages.warning(request, 'Some/all of the records you have selected were not approved because you are not listed as a project leader for them')

    return HttpResponseRedirect(".")
approve_records.short_description = "Approve records"

def notify_user_edits_required(modeladmin, request, queryset):
    """Notify a user that a collection record must be edited"""

    queryset = queryset.filter(content_type__app_label='collection_management')

    if queryset.filter(message=''):
        messages.error(request, 'Some of the records you have selected do not have a message. Please add a message to them, and try again')
        return HttpResponseRedirect(".")
    else:
        user_ids= set(queryset.values_list('activity_user', flat=True).distinct())
        now_time = timezone.now()
        for user_id in user_ids:
            user = User.objects.get(id=user_id)
            records = [(str(rec.content_type.name).capitalize(), str(rec.content_object), rec.message) for rec in queryset.filter(activity_user__id=user_id)]

            records_str = ''
            for rec in records:
                records_str = records_str + '\t'.join(rec).strip() + '\n'

            message = """Dear {},

            {} has flagged some of your records to be amended. See below.

            {}
            Regards,
            The Ulrich lab intranet
            """
            
            message = inspect.cleandoc(message).format(user.first_name, request.user, records_str)

            send_mail('Some records that you have created/changed need your attention', 
                    message, 
                    'system@imbc2.imb.uni-mainz.de',
                    [user.email],
                    fail_silently=False,)
        messages.success(request, 'Users have been notified of required edits')
        queryset.update(message_date_time=now_time, edited=False)
        return HttpResponseRedirect(".")
notify_user_edits_required.short_description = "Notify users of required edits"

def approve_all_new_orders(modeladmin, request, queryset):
    """Approve all new orders """

    if request.user.labuser.is_principal_investigator:
        orders = order_management_Order.objects.filter(created_approval_by_pi=False)
        if orders:
            orders.update(created_approval_by_pi=True)
            RecordToBeApproved.objects.filter(content_type__app_label='order_management').delete()
            messages.success(request, 'New orders have been approved')
        else:
            messages.warning(request, 'No new orders to approve')
    else:
        messages.error(request, 'You are not allowed to approve orders')

    return HttpResponseRedirect(".")

approve_all_new_orders.short_description = "Approve all new orders"

class RecordToBeApprovedPage(admin.ModelAdmin):
    
    list_display = ('id', 'titled_content_type', 'record_link', 'coloured_activity_type', 'activity_user', 'history_link', 'message', 'message_sent','edited', )
    list_display_links = ('id', )
    list_per_page = 50
    ordering = ['content_type', '-activity_type', 'object_id']
    actions = [approve_records, notify_user_edits_required, approve_all_new_orders]
    
    def get_readonly_fields(self, request, obj=None):
        
        # Specifies which fields should be shown as read-only and when
        
        if obj:
            return ['content_type', 'object_id', 'content_object', 'activity_type', 'activity_user',
                    'message_date_time', 'edited', 'created_date_time',]
        else:
            return ['created_date_time',]

    def changelist_view(self, request, extra_context=None):
        
        # Set queryset of action approve_all_new_orders

        if 'action' in request.POST and request.POST['action'] == 'approve_all_new_orders':
            if not request.POST.getlist(admin.ACTION_CHECKBOX_NAME):
                post = request.POST.copy()
                for u in order_management_Order.objects.all():
                    post.update({admin.ACTION_CHECKBOX_NAME: str(u.id)})
                request._set_post(post)
        return super(RecordToBeApprovedPage, self).changelist_view(request, extra_context=extra_context)

    def get_queryset(self, request):
        
        qs = super(RecordToBeApprovedPage, self).get_queryset(request)

        # If user is approval manager show only collection items, not orders

        if request.user.labuser.is_principal_investigator or request.user.is_superuser or request.user.groups.filter(name='Lab manager').exists():
            return qs
        elif request.user.groups.filter(name='Approval manager').exists():
            return qs.filter(content_type__app_label='collection_management')

    def record_link(self, instance):
        '''Custom link to a record field for changelist_view'''

        url = reverse("admin:{}_{}_change".format(instance.content_object._meta.app_label, instance.content_object._meta.model_name), args=(instance.content_object.id,))
        record_name = str(instance.content_object)
        record_name =  record_name[:50] + "..." if len(record_name) > 50 else record_name 
       
        return mark_safe('<a href="{}" target="_blank">{}</a>'.format(url, record_name))

    record_link.short_description = 'Record'

    def history_link(self, instance):
        '''Custom link to a record's history field for changelist_view'''

        url = reverse("admin:{}_{}_history".format(instance.content_object._meta.app_label, instance.content_object._meta.model_name), args=(instance.content_object.id,))

        return mark_safe('<a href="{}" target="_blank">{}</a>'.format(url, 'History',))
    history_link.short_description = 'History'

    def titled_content_type(self, instance):
        '''Custom link to a record's history field for changelist_view'''

        return str(instance.content_type).title()

    titled_content_type.short_description = 'Record type'
    titled_content_type.admin_order_field = 'content_type'

    def coloured_activity_type(self, instance):
        '''changew_view column to show created activity_type in red'''
        
        if instance.activity_type == 'created':
            return mark_safe('<span style="color:red;">created</span>')
        elif instance.activity_type == 'changed':
            return mark_safe('<span>changed</span>')

    coloured_activity_type.short_description = 'Activity type'
    coloured_activity_type.admin_order_field = 'activity_type'

    def message_sent(self, instance):
        '''changew_view column to show whether a message has been sent or not'''

        if instance.message_date_time:
            return True
        else:
            return False
    message_sent.boolean = True
    message_sent.short_description = "Message sent?"