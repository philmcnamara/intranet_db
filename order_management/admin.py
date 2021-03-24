#################################################
#    DJANGO 'CORE' FUNCTIONALITIES IMPORTS      #
#################################################

from django.contrib import admin
from django.core.mail import send_mail
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import models
from django.http import HttpResponse
from django.db.models.functions import Length
from django.core.exceptions import PermissionDenied
from django.utils.translation import ugettext as _
from django import forms


from django_project.private_settings import SITE_TITLE
from django_project.private_settings import SERVER_EMAIL_ADDRESS
from django_project.private_settings import ORDER_APPROVAL_EMAIL_ADDRESSES
from django_project.private_settings import ORDER_MANAGER_EMAIL_ADDRESSES
from django_project.private_settings import ALLOWED_HOSTS

#################################################
#        ADDED FUNCTIONALITIES IMPORTS          #
#################################################

# Advanced search functionalities from DjangoQL
from djangoql.admin import DjangoQLSearchMixin
from djangoql.schema import DjangoQLSchema, StrField
from collection_management.admin import SearchFieldOptUsername, SearchFieldOptLastname

# Object history tracking from django-simple-history
from collection_management.admin import SimpleHistoryWithSummaryAdmin

# Import/Export functionalities from django-import-export
from import_export.admin import ExportActionModelAdmin

# Background tasks
from background_task import background

# Mass update
from adminactions.mass_update import MassUpdateForm, get_permission_codename,\
    ActionInterrupted, adminaction_requested, adminaction_start, adminaction_end

# jsmin
from jsmin import jsmin

import xlrd
import csv
import copy

# Modify approval records
from record_approval.models import RecordToBeApproved

#################################################
#                OTHER IMPORTS                  #
#################################################

from .models import OrderExtraDoc
from .models import Order
from .models import MsdsForm
from .models import SupplierOption

import datetime
import time
import inspect

# delete button
from django.contrib.auth.models import Permission
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

#################################################
#         CUSTOM MASS UPDATE FUNCTION           #
#################################################

def mass_update(modeladmin, request, queryset):
    """
        mass update queryset
        From adminactions.mass_update. Modified to allow specifiying a custom form
    """

    import json
    from collections import defaultdict

    from django.contrib.admin import helpers
    from django.core.exceptions import ObjectDoesNotExist
    from django.db.models import ForeignKey, fields as df
    from django.db.transaction import atomic
    from django.forms.models import (InlineForeignKeyField,
                                    ModelMultipleChoiceField, construct_instance,
                                    modelform_factory, )
    from django.http import HttpResponseRedirect
    from django.shortcuts import render
    from django.utils.encoding import smart_text

    def not_required(field, **kwargs):
        """ force all fields as not required"""
        kwargs['required'] = False
        return field.formfield(**kwargs)

    def _doit():
        errors = {}
        updated = 0
        for record in queryset:
            for field_name, value_or_func in list(form.cleaned_data.items()):
                if callable(value_or_func):
                    old_value = getattr(record, field_name)
                    setattr(record, field_name, value_or_func(old_value))
                else:
                    setattr(record, field_name, value_or_func)
            if clean:
                record.clean()
            record.save()
            updated += 1
        if updated:
            messages.info(request, _("Updated %s records") % updated)

        if len(errors):
            messages.error(request, "%s records not updated due errors" % len(errors))
        adminaction_end.send(sender=modeladmin.model,
                             action='mass_update',
                             request=request,
                             queryset=queryset,
                             modeladmin=modeladmin,
                             form=form,
                             errors=errors,
                             updated=updated)

    opts = modeladmin.model._meta
    perm = "{0}.{1}".format(opts.app_label, get_permission_codename('adminactions_massupdate', opts))
    if not (request.user.groups.filter(name='Lab manager').exists() or request.user.groups.filter(name='Order manager').exists()):
        messages.error(request, _('Sorry, your account does not have that permission.'))
        return

    try:
        adminaction_requested.send(sender=modeladmin.model,
                                   action='mass_update',
                                   request=request,
                                   queryset=queryset,
                                   modeladmin=modeladmin)
    except ActionInterrupted as e:
        messages.error(request, str(e))
        return

    # Allows to specify a custom mass update Form in ModelAdmin
    mass_update_form = getattr(modeladmin, 'mass_update_form', MassUpdateForm)

    MForm = modelform_factory(modeladmin.model, form=mass_update_form,
                              exclude=('pk',),
                              formfield_callback=not_required)
    grouped = defaultdict(lambda: [])
    selected_fields = []
    initial = {'_selected_action': request.POST.getlist(helpers.ACTION_CHECKBOX_NAME),
               'select_across': request.POST.get('select_across') == '1',
               'action': 'mass_update'}

    if 'apply' in request.POST:
        form = MForm(request.POST)
        if form.is_valid():
            try:
                adminaction_start.send(sender=modeladmin.model,
                                       action='mass_update',
                                       request=request,
                                       queryset=queryset,
                                       modeladmin=modeladmin,
                                       form=form)
            except ActionInterrupted as e:
                messages.error(request, str(e))
                return HttpResponseRedirect(request.get_full_path())

            # need_transaction = form.cleaned_data.get('_unique_transaction', False)
            validate = True
            clean = False

            if validate:
                with atomic():
                    _doit()

            else:
                values = {}
                for field_name, value in list(form.cleaned_data.items()):
                    if isinstance(form.fields[field_name], ModelMultipleChoiceField):
                        messages.error(request, "Unable to mass update ManyToManyField without 'validate'")
                        return HttpResponseRedirect(request.get_full_path())
                    elif callable(value):
                        messages.error(request, "Unable to mass update using operators without 'validate'")
                        return HttpResponseRedirect(request.get_full_path())
                    elif field_name not in ['_selected_action', '_validate', 'select_across', 'action',
                                            '_unique_transaction', '_clean']:
                        values[field_name] = value
                queryset.update(**values)

            return HttpResponseRedirect(request.get_full_path())
    else:
        initial.update({'action': 'mass_update', '_validate': 1})
        # form = MForm(initial=initial)
        prefill_with = request.POST.get('prefill-with', None)
        prefill_instance = None
        try:
            # Gets the instance directly from the queryset for data security
            prefill_instance = queryset.get(pk=prefill_with)
        except ObjectDoesNotExist:
            pass

        form = MForm(initial=initial, instance=prefill_instance)

    for el in queryset.all()[:10]:
        for f in modeladmin.model._meta.fields:
            if f.name not in form._no_sample_for:
                if isinstance(f, ForeignKey):
                    filters = {"%s__isnull" % f.remote_field.name: False}
                    grouped[f.name] = [(a.pk, str(a)) for a in
                                       f.related_model.objects.filter(**filters).distinct()]
                elif hasattr(f, 'flatchoices') and f.flatchoices:
                    grouped[f.name] = dict(getattr(f, 'flatchoices')).keys()
                elif hasattr(f, 'choices') and f.choices:
                    grouped[f.name] = dict(getattr(f, 'choices')).keys()
                elif isinstance(f, df.BooleanField):
                    grouped[f.name] = [("True", True), ("False", False)]
                else:
                    value = getattr(el, f.name)
                    target = [str(value), value]
                    if value is not None and target not in grouped[f.name] and len(grouped) <= 10:
                        grouped[f.name].append(target)

                    initial[f.name] = initial.get(f.name, value)
    adminForm = helpers.AdminForm(form, modeladmin.get_fieldsets(request), {}, [], model_admin=modeladmin)
    media = modeladmin.media + adminForm.media
    dthandler = lambda obj: obj.isoformat() if isinstance(obj, datetime.date) else str(obj)
    tpl = 'adminactions/mass_update.html'
    ctx = {'adminform': adminForm,
           'form': form,
           'action_short_description': mass_update.short_description,
           'title': u"%s (%s)" % (
               mass_update.short_description.capitalize(),
               smart_text(modeladmin.opts.verbose_name_plural),
           ),
           'grouped': grouped,
           'fieldvalues': json.dumps(grouped, default=dthandler),
           'change': True,
           'selected_fields': selected_fields,
           'is_popup': False,
           'save_as': False,
           'has_delete_permission': False,
           'has_add_permission': False,
           'has_change_permission': True,
           'opts': modeladmin.model._meta,
           'app_label': modeladmin.model._meta.app_label,
           # 'action': 'mass_update',
           # 'select_across': request.POST.get('select_across')=='1',
           'media': mark_safe(media),
           'selection': queryset}
    ctx.update(modeladmin.admin_site.each_context(request))

    return render(request, tpl, context=ctx)

mass_update.short_description = _("Mass update selected orders")

#################################################
#                 ORDER INLINES                 #
#################################################

class OrderExtraDocInline(admin.TabularInline):
    """Inline to view existing extra order documents"""

    model = OrderExtraDoc
    verbose_name_plural = "Existing extra docs"
    extra = 0
    fields = ['get_doc_short_name', 'description']
    readonly_fields = ['get_doc_short_name', 'description']

    def has_add_permission(self, request):
        
        # Prevent users from adding new objects with this inline
        return False
    
    def get_doc_short_name(self, instance):
        '''Returns the url of an order document as a HTML <a> tag with 
        text View'''
        if instance.name:
            return mark_safe('<a href="{}">View</a>'.format(instance.name.url))
        else:
            return ''
    get_doc_short_name.short_description = 'Document'

class AddOrderExtraDocInline(admin.TabularInline):
    """Inline to add new extra order documents"""

    model = OrderExtraDoc
    verbose_name_plural = "New extra docs"
    extra = 0
    fields = ['name','description']

    def has_change_permission(self, request, obj=None):
        
        # Prevent users from changing existing objects with this inline
        return False

    def get_readonly_fields(self, request, obj=None):
        '''Defines which fields should be shown as read-only under which conditions'''

        # If user is not a Lab or Order Manager set the name and description attributes as read-only
        if obj:
            if not (request.user.is_superuser or request.user.groups.filter(name='Lab manager').exists() or request.user.groups.filter(name='Order manager').exists()):
                return ['name','description']
            else:
                return []
        else:
            return []

    def get_queryset(self, request):
        return OrderExtraDoc.objects.none()

#################################################
#         ORDER IMPORT/EXPORT RESOURCE          #
#################################################

from import_export import resources

class OrderChemicalExportResource(resources.ModelResource):
    """Defines a custom export resource class for chemicals"""
    
    class Meta:
        model = Order
        fields = ('id','supplier__name', 'part_name', 'supplier_part_no', 'part_category', 'supplier_order_number',
        'part_description', 'quantity', "primary_location", "backup_location",
        "cas_number", 'reorderable', "ghs_pictogram", 'hazard_level_pregnancy')

class OrderExportResource(resources.ModelResource):
    """Defines a custom export resource class for orders"""
    
    class Meta:
        model = Order
        fields = ('id', 'internal_order_no', 'supplier__name', 'part_name', 'supplier_part_no', 'part_category', 'supplier_order_number', 'part_description', 'quantity', 
            'price', 'price_vat', 'status', 'primary_location', "backup_location", 'comment', 'url', 'delivered_date', 'cas_number', 'reorderable',
            'ghs_pictogram', 'hazard_level_pregnancy', 'created_date_time', 'order_manager_created_date_time', 
            'last_changed_date_time', 'created_by__username',)

#################################################
#                   ACTIONS                     #
#################################################

def change_order_status_to_arranged(modeladmin, request, queryset):
    """Change the status of selected orders from approved to arranged"""
    
    # Only Lab or Order Manager can use this action
    if not (request.user.groups.filter(name='Lab manager').exists() or request.user.groups.filter(name='Order manager').exists()):
        messages.error(request, 'Sorry, your account does not have that permission.')
        return
    else:
        for order in queryset.filter(status = "approved"):
            order.status = 'arranged'
            order.save()
change_order_status_to_arranged.short_description = "Change STATUS of selected to ARRANGED"
change_order_status_to_arranged.acts_on_all = True

def change_order_status_to_delivered(modeladmin, request, queryset):
    """Change the status of selected orders from approved to delivered"""
    
    # Only Lab Manager, Order Manager, or Order Receiver can use this action
    if not (request.user.groups.filter(name='Lab manager').exists() or request.user.groups.filter(name='Order manager').exists() or request.user.groups.filter(name="Order receiver")):
        messages.error(request, 'Sorry, your account does not have that permission.')
        return
    else:
        for order in queryset.filter(status = "arranged"):
            order.status = 'delivered'
            order.delivered_date = datetime.date.today()
            
            # If an order does not have a delivery date and its status changes
            # to 'delivered', set the date for delivered_date to the current
            # date. If somebody requested a delivery notification, send it and
            # set delivery_email to true to remember that an email has already been 
            # sent out
            if order.delivery_alert:
                if not order.delivery_email:
                    order.delivery_email = True
                    message = """Dear {},

                    your order #{} for {} : {} has just been delivered.

                    Regards,
                    The {}

                    """.format(order.created_by.first_name, order.pk, order.part_name, order.part_description, SITE_TITLE)
                    
                    message = inspect.cleandoc(message)
                    send_mail('Delivery notification', 
                    message, 
                    SERVER_EMAIL_ADDRESS,
                    [order.created_by.email],
                    fail_silently=True)
            order.save()

change_order_status_to_delivered.short_description = "Change STATUS of selected to DELIVERED"

def change_order_status_to_cancelled(modeladmin, request, queryset):
    """Change the status of selected orders to cancelled"""
    
    # Only Lab or Order Manager can use this action
    if not (request.user.groups.filter(name='Lab manager').exists() or request.user.groups.filter(name='Order manager').exists()):
        messages.error(request, 'Sorry, your account does not have that permission.')
        return
    else:
        for order in queryset:
            order.status = 'cancelled'
            order.save()
change_order_status_to_cancelled.short_description = "Change STATUS of selected to CANCELLED"
change_order_status_to_cancelled.acts_on_all = True


def change_order_status_to_approved(modeladmin, request, queryset):
    """Change the status of selected orders to approved"""
    
    # Only PI or designated staff can use this action
    if not (request.user.groups.filter(name='Approval Manager').exists()):
        messages.error(request, 'Sorry, your account does not have that permission.')
        return
    else:
        for order in queryset.filter(status = "submitted"):
            order.status = 'approved'
            record = RecordToBeApproved.objects.all().get(object_id=order.id)
            record.delete()
            # notify order manager for urgent orders to be placed right away
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
                    pass
            
            order.save()

change_order_status_to_approved.short_description = "Change STATUS of selected to APPROVED"

def export_chemicals(modeladmin, request, queryset):
    """Export all chemicals. A chemical is defined as an order
    which has a non-null ghs_pictogram field and is not used up"""

    queryset = Order.objects.exclude(status="used up").annotate(text_len=Length('ghs_pictogram')).filter(text_len__gt=0).order_by('-id')
    export_data = OrderChemicalExportResource().export(queryset)

    file_format = request.POST.get('format', default='none')

    if file_format == 'xlsx':
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="{}_{}_{}.xlsx'.format(queryset.model.__name__, time.strftime("%Y%m%d"), time.strftime("%H%M%S"))
        response.write(export_data.xlsx)
    elif file_format == 'tsv':
        response = HttpResponse(content_type='text/tab-separated-values')
        response['Content-Disposition'] = 'attachment; filename="{}_{}_{}.tsv'.format(queryset.model.__name__, time.strftime("%Y%m%d"), time.strftime("%H%M%S"))
        xlsx_file = xlrd.open_workbook(file_contents=export_data.xlsx)
        sheet = xlsx_file.sheet_by_index(0)
        wr = csv.writer(response, delimiter="\t")
        for rownum in range(sheet.nrows):
            row_values = [str(i).replace("\n", "").replace('\r', '').replace("\t", "") for i in sheet.row_values(rownum)]
            wr.writerow(row_values)
    return response
export_chemicals.short_description = "Export all chemicals"

def export_orders(modeladmin, request, queryset):
    """Export orders"""

    export_data = OrderExportResource().export(queryset)

    file_format = request.POST.get('format', default='none')

    if file_format == 'xlsx':
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="{}_{}_{}.xlsx'.format(queryset.model.__name__, time.strftime("%Y%m%d"), time.strftime("%H%M%S"))
        response.write(export_data.xlsx)
    elif file_format == 'tsv':
        response = HttpResponse(content_type='text/tab-separated-values')
        response['Content-Disposition'] = 'attachment; filename="{}_{}_{}.tsv'.format(queryset.model.__name__, time.strftime("%Y%m%d"), time.strftime("%H%M%S"))
        xlsx_file = xlrd.open_workbook(file_contents=export_data.xlsx)
        sheet = xlsx_file.sheet_by_index(0)
        wr = csv.writer(response, delimiter="\t")
        for rownum in range(sheet.nrows):
            row_values = [str(i).replace("\n", "").replace('\r', '').replace("\t", "") for i in sheet.row_values(rownum)]
            wr.writerow(row_values)
    return response
export_orders.short_description = "Export selected orders"

def copy_order(modeladmin, request, queryset):
    '''creates a copy of an order, which can be used as a template for a reorder'''
    for order in queryset:
        if order.reorderable:
            clone = copy.copy(order)
            clone.id = None
            clone.created_by = request.user
            clone.status = "unsubmitted"
            clone.save()
            clone.internal_order_no = "{}-{}".format(clone.pk, datetime.date.today().strftime("%y%m%d"))
            clone.approval_email=False
            clone.cloned=True
            clone.delivery_alert=True
            clone.urgent_email=False
            clone.urgent=False
            clone.comment=""
            clone.quantity=None
            clone.supplier_order_number=None
            clone.save()
        else:
            messages.warning(request, 'This order is not reorderable, see comment for alternative')
    copy_order.short_description = "Copy selected orders"

#################################################
#                 ORDER PAGES                   #
#################################################

class SearchFieldSupplierOption(StrField):
    """Create a list of unique supplier units for search"""

    model = SupplierOption
    name = 'supplier'
    suggest_options = True

    def get_options(self):
        return SupplierOption.objects.all().order_by('name').\
        values_list('name', flat=True)

    def get_lookup_name(self):
        return 'supplier__name'

class SearchFieldOptSupplier(StrField):
    """Create a list of unique supplier units for search"""

    model = Order
    name = 'supplier'
    suggest_options = True

    def get_options(self):
        return super(SearchFieldOptSupplier, self).\
        get_options().all().distinct()

class SearchFieldOptPartDescription(StrField):
    """Create a list of unique part description units for search"""

    model = Order
    name = 'part_description'
    suggest_options = True

    def get_options(self):
        return super(SearchFieldOptPartDescription, self).\
        get_options().all().distinct()

class SearchFieldOptAzardousPregnancy(StrField):
    """Create a list of unique Pregnancy hazard units for search"""

    model = Order
    name = 'hazard_level_pregnancy'
    suggest_options = True

class SearchFieldOptUsernameOrder(SearchFieldOptUsername):
    """Create a list of unique users' usernames for search"""

    id_list = Order.objects.all().values_list('created_by', flat=True).distinct()

class SearchFieldOptLastnameOrder(SearchFieldOptLastname):
    """Create a list of unique users' usernames for search"""

    id_list = Order.objects.all().values_list('created_by', flat=True).distinct()

class OrderQLSchema(DjangoQLSchema):
    '''Customize search functionality'''
    
    include = (Order, User, SupplierOption) # Include only the relevant models to be searched

    suggest_options = {
        Order: ['status', 'supplier', 'urgent'],
    }

    def get_fields(self, model):
        ''' Define fields that can be searched'''
        
        if model == Order:
            return ['id', SearchFieldOptSupplier(), 'part_name', 'supplier_part_no', 'part_category', 
            'internal_order_no', SearchFieldOptPartDescription(),
            'status', 'urgent', "primary_location", "backup_location", 'comment', 'delivered_date', 'cas_number', 'reorderable',
            'ghs_pictogram', SearchFieldOptAzardousPregnancy(), 'created_date_time', 'last_changed_date_time', 'created_by',]
        elif model == User:
            return [SearchFieldOptUsernameOrder(), SearchFieldOptLastnameOrder()]
        return super(OrderQLSchema, self).get_fields(model)

class MyMassUpdateOrderForm(MassUpdateForm):
    
    _clean = None
    _validate = None

    class Meta:
        model = Order
        fields = ['supplier', 'part_name', 'supplier_part_no', 'part_category', 'internal_order_no', 'supplier_order_number', 
                  'part_description', 'quantity', 'price','price_vat', 'primary_location', "backup_location", 'comment', 'url', 
                  'cas_number', 'reorderable', 'ghs_pictogram', 'msds_form', 'hazard_level_pregnancy']
    
    def clean__validate(self):
        return True
    
    def clean__clean(self):
        return False

class OrderPage(DjangoQLSearchMixin, SimpleHistoryWithSummaryAdmin, admin.ModelAdmin):
    
    list_display = ('custom_internal_order_no', 'part_name', 'supplier', 'item_description', 'supplier_part_no', 
                    'quantity', 'trimmed_comment' ,'primary_location', 'reorderable', 'coloured_status', "created_by", 'last_changed_date_time',)
    list_display_links = ('custom_internal_order_no', )
    list_per_page = 25
    inlines = [OrderExtraDocInline, AddOrderExtraDocInline]
    djangoql_schema = OrderQLSchema
    mass_update_form = MyMassUpdateOrderForm
    actions = [copy_order, change_order_status_to_arranged, change_order_status_to_delivered, change_order_status_to_approved, change_order_status_to_cancelled,
               export_orders, export_chemicals, mass_update]
    search_fields = ['id', 'part_name', 'supplier__name', 'supplier_part_no', 'part_category', 'supplier_order_number',
                     'part_description', 'status', 'comment', 'created_by__username']
    
    def save_model(self, request, obj, form, change):
        
        # New orders
        if obj.pk == None:
            # If an order is new, assign the request user to it only if the order's created_by
            # attribute is not null

            try:
                obj.created_by
            except:
                obj.created_by = request.user

            obj.save()
            
            # Automatically create internal_order_number and add it to record
            obj.internal_order_no = "{}-{}".format(obj.pk, datetime.date.today().strftime("%y%m%d"))
            obj.save()
            
            # Delete first history record, which doesn't contain an internal_order_number, and change the newer history 
            # record's history_type from changed (~) to created (+). This gets rid of a duplicate history record created
            # when automatically generating an internal_order_number
            obj.history.last().delete()
            history_obj = obj.history.first()
            history_obj.history_type = "+"
            history_obj.save()
            
            # Add approval record
            if not request.user.labuser.is_principal_investigator:
                obj.approval.create(activity_type='created', activity_user=obj.history.latest().created_by)
                Order.objects.filter(id=obj.pk).update(created_approval_by_pi=True)
        
        # Existing orders
        else:
            # Users can edit their own orders before they are approved
            # after approval only lab managers or order managers can edit them
            order = Order.objects.get(pk=obj.pk)
            
            # If the status of an order changes to the following
            if obj.status != order.status:
                if not order.order_manager_created_date_time:
                    
                    # If an order's status changed from 'submitted' to any other, 
                    # set the date-time for order_manager_created_date_time to the
                    # current date-time
                    if obj.status in ['approved', 'arranged', 'delivered']:
                        obj.order_manager_created_date_time = timezone.now()
                
                # If an order does not have a delivery date and its status changes
                # to 'delivered', set the date for delivered_date to the current
                # date. If somebody requested a delivery notification, send it and
                # set delivery_email to true to remember that an email has already been 
                # sent out
                if not order.delivered_date:
                    if obj.status == "delivered":
                        obj.delivered_date = datetime.date.today()
                        if order.delivery_alert:
                            if not order.delivery_email:
                                obj.delivery_email = True
                                message = """Dear {},

                                your order #{} for {} has just been delivered.

                                """.format(obj.created_by.first_name, obj.pk, obj.part_description, SITE_TITLE)
                                
                                message = inspect.cleandoc(message)
                                try:
                                    send_mail('Delivery notification', 
                                    message, 
                                    SERVER_EMAIL_ADDRESS,
                                    [obj.created_by.email],
                                    fail_silently=False,)
                                    messages.success(request, 'Delivery notification was sent.')
                                except:
                                    messages.warning(request, 'Could not send delivery notification.')
            if obj.status == "unsubmitted":
                # Add approval record
                if not request.user.labuser.is_principal_investigator:
                    obj.approval.create(activity_type='created', activity_user=obj.history.latest().created_by)
                    Order.objects.filter(id=obj.pk).update(created_approval_by_pi=True)
                obj.status="submitted"
                obj.save()
            
            obj.save()
            
            # Delete order history for used-up or cancelled items
            if obj.status in ["used up", 'cancelled'] and obj.history.exists():
                obj_history = obj.history.all()
                obj_history.delete()
    
        # Notify order approval manager of new orders
        if obj.status == "submitted" and obj.approval_email == False:

            message = """Dear Order Approval Manager,

            {} {} has placed a new order for {} item {} - {}

            You can see all items pending approval here: https://{}/record_approval/recordtobeapproved/

            """.format(request.user.first_name, request.user.last_name, obj.supplier, obj.supplier_part_no, obj.part_description, ALLOWED_HOSTS[0])

            if obj.comment:
                message += "\nComment: {}".format(obj.comment)

            message = inspect.cleandoc(message)
            try:
                send_mail('New order placed', 
                message, 
                SERVER_EMAIL_ADDRESS,
                ORDER_APPROVAL_EMAIL_ADDRESSES,
                fail_silently=False,)
                messages.success(request, 'The order approval manager has been notified of your request')
                obj.approval_email=True
                obj.save()
            except:
                messages.warning(request, 'Your order was added to the order list. However, the approval request email failed to send.')


    def get_queryset(self, request):
        
        # Allows sorting of custom changelist_view fields by adding admin_order_field
        # property to said custom field, also excludes cancelled orders, to make things prettier"""

        qs = super(OrderPage, self).get_queryset(request)
        qs = qs.annotate(models.Count('id'), models.Count('part_description'), models.Count('status'))
        
        if not (request.user.groups.filter(name='Lab manager').exists() or request.user.groups.filter(name='Order manager').exists() or request.user.is_superuser):
            return qs.exclude(status='cancelled')
        else:
            return qs

    def get_readonly_fields(self, request, obj=None):
        # Specifies which fields should be shown as read-only and when
        always_readonly_fields = ['delivered_date', 'status', 'price_vat', 'order_manager_created_date_time','created_date_time', 'last_changed_date_time', 'created_by']
        cloned_readonly_fields = ['supplier', 'part_name', 'supplier_part_no', 'part_category', 'internal_order_no', 'part_description', 'primary_location', 'backup_location',
                                  'url', 'cas_number', 'ghs_pictogram', 'msds_form', 'hazard_level_pregnancy', 'reorderable', 'supplier_order_number']
        never_readonly_fields = ['quantity', 'price', 'urgent', 'delivery_alert', 'comment']
        if obj:
            # admin-level user
            if (request.user.groups.filter(name='Lab manager').exists() or request.user.groups.filter(name='Order manager').exists() or
                request.user.groups.filter(name='Approval manager').exists()):
                return always_readonly_fields

            # non-admin user that can edit the order
            elif self.can_change:
                # order is being marked for delivery
                if (obj.status == "arranged" or obj.status == "delivered") and request.user.groups.filter(name="Order receiver"):
                    # all fields are read-only EXCEPT primary/backup location
                    all_fields = always_readonly_fields + cloned_readonly_fields + never_readonly_fields
                    all_fields.remove("primary_location")
                    all_fields.remove("backup_location")
                    return all_fields

                # new order being created
                elif obj.created_by == request.user and (obj.status == "submitted" or obj.status == "unsubmitted"):
                    # all fields can be set
                    if obj.cloned == False:
                        return always_readonly_fields
                    # cloned order, only certain fields editable
                    else:
                        return always_readonly_fields + cloned_readonly_fields

                # order receiver viewing a different order
                else:
                    return always_readonly_fields + cloned_readonly_fields + never_readonly_fields

            # can't edit, return all fields as read-only
            else:
                return always_readonly_fields + cloned_readonly_fields + never_readonly_fields
        else:
            return ['order_manager_created_date_time', 'created_date_time',  'last_changed_date_time',]

    def add_view(self, request, extra_context=None):
        
        # Specifies which fields should be shown in the add view
        self.fields = ('supplier', 'part_name', 'supplier_part_no', 'part_category', 'url', 'supplier_order_number',
                       'part_description', 'quantity', 'price', 'urgent', 'delivery_alert', 'primary_location', 'backup_location',
                       'comment', 'cas_number', 'ghs_pictogram', 'msds_form', 'hazard_level_pregnancy', 'created_by')
        self.raw_id_fields = ['msds_form']
        self.autocomplete_fields = []
        return super(OrderPage,self).add_view(request, extra_context=extra_context)

    def change_view(self, request, object_id, extra_context=None):
        
        # Specifies which fields should be shown in the change view
        
        self.raw_id_fields = []
        self.autocomplete_fields = ['msds_form']
        self.can_change = False

        if object_id:
            extra_context = extra_context or {}
            order = Order.objects.get(id=object_id)
            delete_permission = Permission.objects.get(codename="delete_order")
            # Regular users can only edit their own orders before they are approved
            # Lab managers and order managers can edit all orders
            if (order.created_by == request.user and (order.status == "submitted" or order.status == "unsubmitted") or 
                request.user.groups.filter(name='Lab manager').exists() or request.user.groups.filter(name='Order manager').exists() or
                request.user.groups.filter(name="Order receiver")):
                self.can_change = True

                # add delete permission and refresh user permissions cache
                request.user.user_permissions.add(delete_permission)
                request.user = get_object_or_404(User, pk=request.user.id)

                extra_context = {'show_close': True,
                            'show_save_and_add_another': True,
                            'show_save_and_continue': True,
                            'show_save_as_new': False,
                            'show_save': True,
                            'show_delete': True,
                            }
            
            else:
                extra_context = {'show_close': True,
                            'show_save_and_add_another': False,
                            'show_save_and_continue': False,
                            'show_save_as_new': False,
                            'show_save': False
                            }

                # delete delete permission and refresh cache
                request.user.user_permissions.remove(delete_permission)
                request.user = get_object_or_404(User, pk=request.user.id)
                

        self.fields = ('supplier', 'part_name', 'supplier_part_no', 'part_category', 'url', 'internal_order_no', 'supplier_order_number',
                       'part_description', 'quantity', 'status', 'price', 'price_vat', 'urgent', 'delivery_alert', 'primary_location', 
                       'backup_location', 'reorderable', 'comment', 'cas_number', 'ghs_pictogram', 'msds_form', 'hazard_level_pregnancy', 
                       'created_date_time', 'order_manager_created_date_time', 'delivered_date', 'created_by')

        return super(OrderPage,self).change_view(request, object_id, extra_context=extra_context)
    
    def changelist_view(self, request, extra_context=None):
        
        # Set queryset of action export_chemicals to all orders

        if 'action' in request.POST and request.POST['action'] == 'export_chemicals':
            if not request.POST.getlist(admin.ACTION_CHECKBOX_NAME):
                post = request.POST.copy()
                for u in Order.objects.all():
                    post.update({admin.ACTION_CHECKBOX_NAME: str(u.id)})
                request._set_post(post)
        
        return super(OrderPage, self).changelist_view(request, extra_context=extra_context)

    def get_formsets_with_inlines(self, request, obj=None):
        
        # Remove AddOrderExtraDocInline from add/change form if user who
        # created an Order object is not the request user a Lab manager
        # or a superuser
        
        if obj:
            for inline in self.get_inline_instances(request, obj):
                if inline.verbose_name_plural == 'Existing extra docs':
                    yield inline.get_formset(request, obj), inline
                else:
                    if request.user.is_superuser or request.user.groups.filter(name='Lab manager').exists() or request.user.groups.filter(name='Order manager').exists():
                        yield inline.get_formset(request, obj), inline
        else:
            for inline in self.get_inline_instances(request, obj):
                if inline.verbose_name_plural == 'Existing extra docs':
                    continue
                else:
                    yield inline.get_formset(request, obj), inline
    
    def item_description(self, instance):
        '''Custom item description field for changelist_view'''

        part_description = instance.part_description.strip()
        part_description = part_description #[:50] + "..." if len(part_description) > 50 else part_description
        return part_description
        # if instance.status != "cancelled":  
        #     return part_description
        # else:
        #     return mark_safe('<span style="text-decoration: line-through;">{}</span>'.format(part_description))
    item_description.short_description = 'Part description'
    item_description.admin_order_field = 'part_description'

    # def supplier_and_part_no(self, instance):
    #     '''Custom supplier and part number field for changelist_view'''

    #     supplier = instance.supplier.strip() if instance.supplier.lower() != "none" else ""
    #     for string in ["GmbH", 'Chemie']:
    #         supplier = supplier.replace(string, "").strip()
    #     supplier_part_no = instance.supplier_part_no.strip() if instance.supplier_part_no  != "none" else ""
    #     if instance.status != "cancelled":  
    #         if supplier_part_no:
    #             return '{} - {}'.format(supplier, supplier_part_no)
    #         else:
    #             return '{}'.format(supplier)
    #     else:
    #         if supplier_part_no:
    #             return mark_safe('<span style="text-decoration: line-through;">{} - {}</span>'.format(supplier, supplier_part_no))
    #         else:
    #             return mark_safe('<span style="text-decoration: line-through;">{}</span>'.format(supplier))
    # supplier_and_part_no.short_description = 'Supplier - Part no.'

    def coloured_status(self, instance):
        '''Custom coloured status field for changelist_view'''

        status = instance.status
        
        if status == "unsubmitted":
            return mark_safe('<span style="width:100%; height:100%; background-color:#ff0000;">{}</span>'.format(status.capitalize()))
        elif status == "submitted":
            return mark_safe('<span style="width:100%; height:100%; background-color:#F5B041;">{}</span>'.format(status.capitalize()))
        elif status == "arranged":
            return mark_safe('<span style="width:100%; height:100%; background-color:#0099cc;">{}</span>'.format(status.capitalize()))
        elif status == "approved":
            return mark_safe('<span style="width:100%; height:100%; background-color:#00cc00;">{}</span>'.format(status.capitalize()))
        elif status == "delivered":
            return mark_safe('<span style="width:100%; height:100%; background-color:#D5D8DC;">{}</span>'.format(status.capitalize()))
        elif status == "cancelled":
            return mark_safe('<span style="width:100%; height:100%; background-color:#000000; color: white;">{}</span>'.format(status.capitalize()))
            
    coloured_status.short_description = 'Status'
    coloured_status.admin_order_field = 'status'

    def trimmed_comment(self, instance):
        '''Custom comment field for changelist_view'''

        comment = instance.comment
        if comment: 
            return comment[:65] + "..." if len(comment) > 65 else comment
        else:
            None
    trimmed_comment.short_description = 'Comments'
    
    def msds_link (self, instance):
        '''Custom comment field for changelist_view'''
        
        if instance.msds_form:
            return mark_safe('<a href="{0}">View</a>'.format(instance.msds_form.name.url))
        else:
            None
    msds_link.short_description = 'MSDS'

    def custom_internal_order_no (self, instance):
        '''Custom internal order no field for changelist_view'''

        if str(instance.internal_order_no).startswith(str(instance.id)):
            return mark_safe('<span style="white-space: nowrap;">{}</span>'.format(instance.internal_order_no))
        else:
            return str(instance.id)
    
    custom_internal_order_no.short_description = "ID"
    custom_internal_order_no.admin_order_field = 'id'

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        
        try:
            request.resolver_match.args[0]
        except:
            
            # Exclude certain users from the 'Created by' field in the order form

            if db_field.name == 'created_by':
                if request.user.is_superuser or request.user.groups.filter(name='Lab manager').exists() or request.user.groups.filter(name='Order manager').exists():
                    kwargs["queryset"] = User.objects.exclude(id__in=[1, 20, 36]).order_by('last_name')
                kwargs['initial'] = request.user.id

            # Sort supplier fields by name
            
            if db_field.name == "supplier":
                kwargs["queryset"] = SupplierOption.objects.exclude(status=True).order_by('name')

        return super(OrderPage, self).formfield_for_foreignkey(db_field, request, **kwargs)

#################################################
#                MSDS FORM PAGES                #
#################################################

class SearchFieldOptMsdsName(StrField):
    """Create a list of unique MSDS units for search"""

    model = MsdsForm
    name = 'name'
    suggest_options = True

    def get_options(self):
        return super(SearchFieldOptMsdsName, self).\
        get_options().all().distinct()

class MsdsFormQLSchema(DjangoQLSchema):
    '''Customize search functionality'''
    
    def get_fields(self, model):
        ''' Define fields that can be searched'''
        
        if model == MsdsForm:
            return ['id', SearchFieldOptMsdsName()]
        return super(MsdsFormQLSchema, self).get_fields(model)

class MsdsFormForm(forms.ModelForm):
    def clean_name(self):
        
        # Check if the name of a MSDS form is unique before saving
        
        qs = MsdsForm.objects.filter(name__icontains=self.cleaned_data["name"].name)
        if qs.exists():
            raise forms.ValidationError('A form with this name already exists.')
        else:
            return self.cleaned_data["name"]

class MsdsFormPage(DjangoQLSearchMixin, admin.ModelAdmin):
    
    list_display = ('id', 'pretty_file_name', 'view_file_link')
    list_per_page = 25
    ordering = ['name']
    djangoql_schema = MsdsFormQLSchema
    search_fields = ['id', 'name']
    form = MsdsFormForm
    
    def add_view(self,request,extra_context=None):
        self.fields = (['name',])
        return super(MsdsFormPage,self).add_view(request)

    def change_view(self,request,object_id,extra_context=None):
        self.fields = (['name',])
        return super(MsdsFormPage,self).change_view(request,object_id)

    def pretty_file_name(self, instance):
        '''Custom file name field for changelist_view'''
        from os.path import basename
        short_name = basename(instance.name.name).split('.')
        short_name = ".".join(short_name[:-1]).replace("_", " ")
        return(short_name)
    pretty_file_name.short_description = "File name"
    pretty_file_name.admin_order_field = 'name'

    def view_file_link(self, instance):
        '''Custom field which shows the url of a MSDS form as a HTML <a> tag with 
        text View'''
        return(mark_safe("<a href='{}'>{}</a>".format(instance.name.url, "View")))
    view_file_link.short_description = ""

#################################################
#            ORDER EXTRA DOC PAGES              #
#################################################

class OrderExtraDocPage(DjangoQLSearchMixin, admin.ModelAdmin):
    list_display = ('id','name',)
    list_display_links = ('id','name', )
    list_per_page = 25
    ordering = ['id']

    def has_module_permission(self, request):
        
        # Hide module from Admin
        return False

    def get_readonly_fields(self, request, obj=None):
        
        # Specifies which fields should be shown as read-only and when

        if obj:
            return ['name', 'order', 'created_date_time',]
    
    def add_view(self,request,extra_context=None):

        # Specifies which fields should be shown in the add view
        self.fields = (['name', 'order', 'created_date_time',])
        return super(OrderExtraDocPage,self).add_view(request)

    def change_view(self,request,object_id,extra_context=None):
        
        # Specifies which fields should be shown in the change view
        self.fields = (['name', 'order', 'created_date_time',])
        return super(OrderExtraDocPage,self).change_view(request,object_id)

#################################################
#           ORDER SUPPLIER PAGES                #
#################################################

class SupplierOptionPage(admin.ModelAdmin):
    
    list_display = ('name', 'status')
    list_display_links = ('name', )
    list_per_page = 25
    ordering = ['name']

# class HideStatus(CreateView):
#     def get_context_data(self, *args, **kwargs):
#         context = super(HideStatus, self).get_context_data(*args, **kwargs)
#         context['my_additional_context'] = my_object
#         return context