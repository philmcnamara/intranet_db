#################################################
#    DJANGO 'CORE' FUNCTIONALITIES IMPORTS      #
#################################################

from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import force_text
from django.contrib.contenttypes.fields import GenericRelation

#################################################
#        ADDED FUNCTIONALITIES IMPORTS          #
#################################################

from simple_history.models import HistoricalRecords
import os
import time
from decimal import Decimal
from record_approval.models import RecordToBeApproved
from django_project.private_settings import LAB_ABBREVIATION_FOR_FILES

#################################################
#                CUSTOM CLASSES                 #
#################################################

class SaveWithoutHistoricalRecord():

    def save_without_historical_record(self, *args, **kwargs):
        """Allows inheritance of a method to save an object without
        saving a historical record as described in  
        https://django-simple-history.readthedocs.io/en/2.7.2/querying_history.html?highlight=save_without_historical_record"""

        self.skip_history_when_saving = True
        try:
            ret = self.save(*args, **kwargs)
        finally:
            del self.skip_history_when_saving
        return ret

#################################################
#             ORDER SUPPLIER MODEL              #
#################################################

class SupplierOption(models.Model):
    
    name = models.CharField("name", max_length=255, unique=True, blank=False)
    status = models.BooleanField("deactivate?", help_text="Check it, if you want to HIDE this supplier from the 'Add new order' form ", default=False)
    
    class Meta:
        ordering = ["name",]

    def __str__(self):
        return self.name
    
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        
        super(SupplierOption, self).save(force_insert, force_update, using, update_fields)

#################################################
#             GHS CODE MODEL                    #
#################################################

class GHSCode(models.Model):
    code = models.CharField("code", max_length=255, unique=True, blank=False)
    description = models.TextField("description")

    class Meta:
        ordering = ["code"]
    
    def __str__(self):
        return self.code + " - " + self.description

#################################################
#               MSDS FORD MODEL                 #
#################################################

class MsdsForm(models.Model):
    
    name = models.FileField("file name", help_text = 'max. 2 MB', upload_to="order_management/msdsform/", unique=True, blank=False)
    
    created_date_time = models.DateTimeField("created", auto_now_add=True, null=True)
    last_changed_date_time = models.DateTimeField("last changed", auto_now=True, null=True)

    class Meta:
        verbose_name = 'MSDS form'
    
    def __str__(self):
        return os.path.splitext(os.path.basename(str(self.name)))[0]

    def clean(self):

        errors = []
        file_size_limit = 2 * 1024 * 1024
        
        if self.name:
            
            # Check if file is bigger than 2 MB
            if self.name.size > file_size_limit:
                errors.append(ValidationError('File too large. Size cannot exceed 2 MB.'))
            
            # Check if file has extension
            try:
                file_ext = self.name.name.split('.')[-1].lower()
            except:
                errors.append(ValidationError('Invalid file format. File does not have an extension'))

        if len(errors) > 0:
            raise ValidationError(errors)

#################################################
#                 ORDER MODEL                   #
#################################################

ORDER_STATUS_CHOICES = (
('unsubmitted', 'unsubmitted'),
('submitted', 'submitted'),
('approved', 'approved'),
('arranged', 'arranged'), 
('delivered', 'delivered'),
('cancelled', 'cancelled'))

HAZARD_LEVEL_PREGNANCY_CHOICES = (('none', 'none'), 
('yellow', 'yellow'), 
('red', 'red'))

ITEM_CATEGORY_CHOICES = (
('Animal Care', 'Animal Care'),
('Antibodies', 'Antibodies'),
('Cells', 'Cells'),
('Chemicals', 'Chemicals'),
('Consumables', 'Consumables'),
('Enzymes', 'Enzymes'),
('Furniture', 'Furniture'),
('Glassware', 'Glassware'),
('IT', 'IT'),
('Lab Equipment', 'Lab Equipment'),
('Office Supplies', 'Office Supplies'),
('Radioactivity', 'Radioactivity')
)

class Order(models.Model, SaveWithoutHistoricalRecord):
    
    supplier = models.ForeignKey(SupplierOption, on_delete=models.PROTECT, null=True, blank=False)
    part_name = models.CharField("part name", max_length=255, null=True, blank=False)
    supplier_part_no = models.CharField("supplier Part-No", max_length=255, blank=False)
    part_category = models.CharField("Item Category", max_length=255, choices=ITEM_CATEGORY_CHOICES, blank=False, null=False)
    url = models.URLField("URL", max_length=1000, blank=True)
    internal_order_no = models.CharField("internal order number", max_length=255, blank=True)
    part_description = models.TextField("part description", help_text="Please include units that correspond to the quantity", blank=False)
    quantity = models.IntegerField("quantity", blank=False, null=True)
    price = models.DecimalField("price (VAT-exclusive)", null=True, decimal_places=2, max_digits=10, blank=True)
    price_vat = models.DecimalField("price (VAT-inclusive)", null=True, decimal_places=2, max_digits=10, blank=True)
    status = models.CharField("status", max_length=255, choices=ORDER_STATUS_CHOICES, default="submitted", blank=False)
    urgent = models.BooleanField("is this an urgent order?", default=False)
    delivery_alert = models.BooleanField("delivery notification?", default=True)
    primary_location = models.CharField("primary location", help_text="Please update with item's location after it arrives",
                                         max_length=255, blank=True)
    backup_location = models.CharField("backup location", max_length=255, blank=True)
    comment =  models.TextField("comments", blank=True)
    order_manager_created_date_time = models.DateTimeField("created in OrderManager", blank=True, null=True)
    delivered_date = models.DateField("delivered", blank=True, default=None, null=True)
    supplier_order_number = models.CharField("Supplier Order Number", max_length=255, blank=True, null=True)
    cas_number = models.CharField("CAS number", max_length=255, blank=True)
    ghs_codes = models.ManyToManyField("GHSCode", related_name='order_ghs_codes', blank=True)
    msds_form = models.ForeignKey(MsdsForm, on_delete=models.PROTECT, blank=True, null=True)
    hazard_level_pregnancy = models.CharField("Hazard level for pregnancy", max_length=255, choices=HAZARD_LEVEL_PREGNANCY_CHOICES, default='none', blank=True)
    approval_email = models.BooleanField(default=False, null=True)
    delivery_email = models.BooleanField(default=False, null=True)
    urgent_email = models.BooleanField(default=False, null=True)
    cloned = models.BooleanField(default=False, null=True)
    reorderable = models.BooleanField("Reorderable", default=True, null=False)

    created_date_time = models.DateTimeField("created", auto_now_add=True, null=True)
    last_changed_date_time = models.DateTimeField("last changed", auto_now=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)
    created_approval_by_pi = models.BooleanField(default=False, null=True)
    approval = GenericRelation(RecordToBeApproved)
    history_ghs_codes = models.TextField("ghs codes", blank=True)
    history = HistoricalRecords()

    class Meta:
        verbose_name = 'order'
    
    def __str__(self):
         return "{} - {}".format(self.id, self.part_name)
    
    def save_without_historical_record(self, *args, **kwargs):
        """Allows inheritance of a method to save an object without
        saving a historical record as described in  
        https://django-simple-history.readthedocs.io/en/2.7.2/querying_history.html?highlight=save_without_historical_record"""

        self.skip_history_when_saving = True
        try:
            ret = self.save(*args, **kwargs)
        finally:
            del self.skip_history_when_saving
        return ret
    
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        
        # Remove airquote, new-line and hash characters from specific fields
        #self.supplier = self.supplier.strip().replace("'","").replace('"',"").replace('\n'," ").replace('#'," ")
        self.supplier_part_no = self.supplier_part_no.strip().replace("'","").replace('"',"").replace('\n'," ").replace('#'," ")
        self.part_description = self.part_description.strip().replace("'","").replace('"',"").replace('\n'," ").replace('#'," ")
        if self.price:
            self.price_vat = self.price * Decimal(1.19)
        self.cas_number = self.cas_number.strip().replace("'","").replace('"',"").replace('\n'," ").replace('#'," ")

        super(Order, self).save(force_insert, force_update, using, update_fields)

#################################################
#           ORDER EXTRA DOC MODEL               #
#################################################

class OrderExtraDoc(models.Model):
    
    name = models.FileField("file name", help_text = 'max. 2 MB', upload_to="temp/", blank=False)
    description = models.CharField("description", max_length=255, blank=False)
    order = models.ForeignKey(Order, on_delete=models.PROTECT, null=True)
    
    created_date_time = models.DateTimeField("created", auto_now_add=True)
    last_changed_date_time = models.DateTimeField("last changed", auto_now=True)

    class Meta:
        verbose_name = 'order extra document'
    
    def __str__(self):
         return str(self.id)

    RENAME_FILES = {
        'name': 
        {'dest': 'order_management/orderextradoc/', 
        'keep_ext': True}
        }

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        
        # Rename a file of any given name to  ordocXX_date-uploaded_time-uploaded.ext,
        # after the corresponding entry has been created

        rename_files = getattr(self, 'RENAME_FILES', None)
        
        if rename_files:
            
            super(OrderExtraDoc, self).save(force_insert, force_update, using, update_fields)
            force_insert, force_update = False, True
            
            for field_name, options in rename_files.items():
                field = getattr(self, field_name)
                
                if field:
                    
                    # Create new file name
                    file_name = force_text(field)
                    name, ext = os.path.splitext(file_name)
                    ext = ext.lower()
                    keep_ext = options.get('keep_ext', True)
                    final_dest = options['dest']
                    
                    if callable(final_dest):
                        final_name = final_dest(self, file_name)
                    else:
                        final_name = os.path.join(final_dest, "ordoc" + LAB_ABBREVIATION_FOR_FILES + str(self.order.id) + "_" + time.strftime("%Y%m%d") + "_" + time.strftime("%H%M%S") + "_" + str(self.id))
                        if keep_ext:
                            final_name += ext
                    
                    # Essentially, rename file
                    if file_name != final_name:
                        field.storage.delete(final_name)
                        field.storage.save(final_name, field)
                        field.close()
                        field.storage.delete(file_name)
                        setattr(self, field_name, final_name)
        
        super(OrderExtraDoc, self).save(force_insert, force_update, using, update_fields)

    def clean(self):

        errors = []
        file_size_limit = 2 * 1024 * 1024
        
        if self.name:
            
            # Check if file is bigger than 2 MB
            if self.name.size > file_size_limit:
                errors.append(ValidationError('File too large. Size cannot exceed 2 MB.'))
            
            # Check if file has extension
            try:
                file_ext = self.name.name.split('.')[-1].lower()
            except:
                errors.append(ValidationError('Invalid file format. File does not have an extension'))

        if len(errors) > 0:
            raise ValidationError(errors)