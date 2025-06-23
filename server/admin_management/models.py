from django.db import models
from django.core.validators import MinValueValidator


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Customers(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    customer_id = models.CharField(db_column='CustomerID', max_length=255, blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(db_column='CustomerName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    address = models.CharField(db_column='Address', max_length=255, blank=True, null=True)  # Field name made lowercase.
    phone_number = models.CharField(db_column='PhoneNumber', max_length=255, blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(db_column='EMail', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'customers'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Inventory(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    code = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    in_stock = models.IntegerField(blank=True, null=True)
    to_shop = models.IntegerField(blank=True, null=True, validators=[MinValueValidator(1)])
    normal_price = models.FloatField(blank=True, null=True)
    retail_price = models.FloatField(blank=True, null=True)
    wholesale_price = models.FloatField(blank=True, null=True)
    moq_whole_sale = models.IntegerField(blank=True, null=True)
    item_inventory_price = models.FloatField(blank=True, null=True)
    defective_units = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'inventory'


class InventoryRestock(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    code = models.CharField(db_column='Code', max_length=255, blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(max_length=255, blank=True, null=True)
    bill_date = models.DateField(blank=True, null=True)
    bill_number = models.CharField(max_length=255, blank=True, null=True)
    supplier = models.CharField(max_length=255, blank=True, null=True)
    new_stock = models.CharField(max_length=255, blank=True, null=True)
    observations = models.TextField(blank=True, null=True)
    user = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'inventory_restock'



class PayingMethods(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    payingmethod = models.CharField(db_column='PayingMethod', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'paying_methods'


class SalesChannel(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    saleschannel = models.CharField(db_column='SalesChannel', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'sales_channel'


class TokenBlacklistBlacklistedtoken(models.Model):
    id = models.BigAutoField(primary_key=True)
    blacklisted_at = models.DateTimeField()
    token = models.OneToOneField('TokenBlacklistOutstandingtoken', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'token_blacklist_blacklistedtoken'


class TokenBlacklistOutstandingtoken(models.Model):
    id = models.BigAutoField(primary_key=True)
    token = models.TextField()
    created_at = models.DateTimeField(blank=True, null=True)
    expires_at = models.DateTimeField()
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    jti = models.CharField(unique=True, max_length=255)

    class Meta:
        managed = False
        db_table = 'token_blacklist_outstandingtoken'


class Userlist(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    username = models.CharField(db_column='UserName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    pw = models.CharField(db_column='PW', max_length=255, blank=True, null=True)  # Field name made lowercase.
    usertype = models.CharField(db_column='UserType', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'userlist'

class BusinessContext(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    name = models.CharField(max_length=30)
    rif = models.CharField(max_length=30)
    direction = models.CharField(max_length=50)
    telephone = models.CharField(max_length=50)
    iva = models.DecimalField(max_digits=4, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'business_context'

class Invoices(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    document_id = models.CharField(max_length=255, blank=True, null=True)
    document_date = models.DateTimeField(blank=True, null=True)
    document_type = models.CharField(max_length=255, blank=True, null=True)
    product_code = models.CharField(max_length=255, blank=True, null=True)
    product_name = models.CharField(max_length=255, blank=True, null=True)
    product_quantity = models.IntegerField(blank=True, null=True)
    product_cost = models.FloatField(blank=True, null=True)
    product_discount = models.FloatField(blank=True, null=True)
    unitary_sub_total = models.FloatField(blank=True, null=True)
    product_tax = models.FloatField(blank=True, null=True)
    customer_id = models.CharField(max_length=255, blank=True, null=True)
    sales_channel = models.CharField(max_length=255, blank=True, null=True)
    paying_method = models.CharField(max_length=255, blank=True, null=True)
    logged_user = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'invoices'