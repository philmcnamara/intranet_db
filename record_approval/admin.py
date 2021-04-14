from django.contrib import admin
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.core.mail import send_mail
import inspect
import datetime
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.utils.text import capfirst

from order_management.models import Order
from collection_management.models import ScPombeStrain, Oligo
from .models import RecordToBeApproved
from django.contrib.contenttypes.models import ContentType

from django_project.private_settings import SITE_TITLE
from django_project.private_settings import SERVER_EMAIL_ADDRESS
from django_project.private_settings import APPROVAL_EMAIL_ADDRESSES
from django_project.private_settings import ALLOWED_HOSTS
from admin_comments.admin import CommentInline

from django.utils import timezone


def approve_records(modeladmin, request, queryset):
    """Approve records"""

    now_time = timezone.now()
    success_message = False
    
    # Collection records, except oligo
    collections_approval_records = queryset.filter(content_type__app_label='collection_management')

    for approval_record in collections_approval_records.exclude(content_type__model='oligo'):
        obj = approval_record.content_object
        if request.user.groups.filter(name='Approval manager').exists():
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
            messages.error(request, "You are not allowed to approve changes")
    
    # Oligos
    oligo_approval_records = collections_approval_records.filter(content_type__model='oligo')
    if oligo_approval_records:
        if request.user.groups.filter(name='Approval manager').exists():
            model = oligo_approval_records[0].content_object._meta.model
            for oligo_approval_record in oligo_approval_records:
                obj = oligo_approval_record.content_object
                if obj.status == "submitted":
                    obj.status="approved"
                obj.save()
            oligo_approval_records.delete()
            success_message = True
        else:
            messages.error(request, 'You are not allowed to approve oligos')
    
    #Orders
    order_approval_records = queryset.filter(content_type__app_label='order_management')
    if order_approval_records:
        if request.user.groups.filter(name='Approval manager').exists():
            model = order_approval_records[0].content_object._meta.model
            order_ids = order_approval_records.values_list('object_id', flat=True)
            for order in model.objects.filter(id__in=order_ids):
                if order.urgent == True and order.urgent_email == False:
                    message = """Dear Order Manager,

                    {} {}'s urgent order for {} has been approved. Please place the order at your earliest convenience.

                    Best,

                    Site Admin

                    """.format(request.user.first_name, request.user.last_name, order.part_name)

                    message = inspect.cleandoc(message)
                    
                    try:
                        send_mail('New urgent order approved', 
                        message, 
                        SERVER_EMAIL_ADDRESS,
                        ORDER_MANAGER_EMAIL_ADDRESSES,
                        fail_silently=False)
                        messages.success(request, 'The order manager has been notified that an urgent order has been approved')
                        order.urgent_email=True
                        order.save()
                    except:
                        print("email failed to send")
            model.objects.filter(id__in=order_ids).update(status="approved")
            for i in model.objects.filter(id__in=order_ids):
                i.save()
            order_approval_records.delete()
            success_message = True
        else:
            messages.error(request, 'You are not allowed to approve orders')
    
    if success_message:
        messages.success(request, 'The records have been approved')

    return HttpResponseRedirect(".")
approve_records.short_description = "Approve records"


def mark_orders_cancelled(modeladmin, request, queryset):
    '''Change the status of selected orders to cancelled'''
    order_approval_records = queryset.filter(content_type__app_label='order_management')
    if request.user.groups.filter(name='Approval manager').exists():
        for record in order_approval_records:
            obj = record.content_object
            obj.status="cancelled"
            obj.save()
            record.delete()

        if queryset.filter(content_type__app_label='collection_management').count() > 0:
            messages.warning(request, "Some of the selected items were not orders and have not been changed")
    else:
        messages.warning(request, "You are not allowed to cancel orders")

mark_orders_cancelled.short_description = "Cancel selected orders"

class ContentTypeFilter(admin.SimpleListFilter):

    title = 'record type'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'record_type'

    def lookups(self, request, model_admin):
        """Show only models for which records to be approved exist"""
        
        list_of_models = []
        for content_type_id in RecordToBeApproved.objects.all().values_list('content_type__id', 'content_type__model').distinct().order_by('content_type__model').values_list('content_type__id', flat=True):
            content_type_obj = ContentType.objects.get(id=content_type_id)
            list_of_models.append((str(content_type_id), capfirst(content_type_obj.model_class()._meta.verbose_name)))

        return tuple(list_of_models)

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """

        if self.value():
            return queryset.filter(content_type=int(self.value()))
        else:
            return queryset

class RecordToBeApprovedPage(admin.ModelAdmin):
    
    list_display = ('id', 'titled_content_type', 'record_link', 'coloured_activity_type', 'activity_user', 'last_changed_date_time', 'history_link' )
    list_display_links = ('id', )
    list_per_page = 50
    ordering = ['-object_id']
    actions = [approve_records, mark_orders_cancelled]
    list_filter = (ContentTypeFilter, 'activity_type', )
    inlines = [CommentInline,]

    def get_readonly_fields(self, request, obj=None):
        
        # Specifies which fields should be shown as read-only and when
        if obj:
            return ['content_type', 'object_id', 'content_object', 'activity_type', 'activity_user', 'created_date_time',]
        else:
            return ['created_date_time',]

    def get_queryset(self, request):
        
        qs = super(RecordToBeApprovedPage, self).get_queryset(request)

        # show PI and superuser everything
        if request.user.labuser.is_principal_investigator or request.user.is_superuser:
            return qs

        # show approval manager all unapproved orders by excluding collection management items
        elif request.user.groups.filter(name="Approval manager").exists():
            return qs.filter(content_type__app_label='collection_management').exclude(content_type__model='scpombestrain')

        else:
            return RecordToBeApproved.objects.filter(activity_user__username=request.user.username)

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

        return capfirst(str(instance.content_type))

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


    def save_model(self, request, obj, form, change):
        if obj.content_type.model == "order":
            name = Order.objects.get(id=obj.object_id).name
            
        elif obj.content_type.model == "oligo":
            name = Oligo.objects.get(id=obj.object_id).name

        elif obj.content_type.model == "scpombestrain":
            name = ScPombeStrain.objects.get(id=obj.object_id).strain_name

        if name is not None:
            message = "There is a new comment on {}. You can find all pending approval records here: https://{}/record_approval/recordtobeapproved/".format(name, ALLOWED_HOSTS[0])
            
            message = inspect.cleandoc(message)

            # If the approval manager leaves the comment, notify the requester
            if request.user.groups.filter(name="Approval manager").exists():
                recipient = User.objects.get(username=obj.activity_user)
                send_mail('New comment on {}'.format(name), message, SERVER_EMAIL_ADDRESS, [recipient.email] ,fail_silently=False,)
                messages.success(request, '{} has been notified of your new comment'.format(recipient.username))

            # otherwise, notify the approval manager
            else:
                send_mail('New comment on {}'.format(name), message, SERVER_EMAIL_ADDRESS, APPROVAL_EMAIL_ADDRESSES,fail_silently=False,)
                messages.success(request, 'The approval manager been notified of your new comment')

        obj.last_changed_date_time=datetime.datetime.now()
        obj.save()
