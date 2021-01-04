from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('collection_management', '0018_auto_20201203_1122'),
    ]

    operations = [
        migrations.RenameField(
            model_name='historicaloligo',
            old_name='order_date',
            new_name='requested_date',
        ),
        migrations.RenameField(
            model_name='oligo',
            old_name='order_date',
            new_name='requested_date',
        ),
    ]