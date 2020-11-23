from django.db import models

# Create your models here.






# 公司企业数据
class CompanyBasicInformation(models.Model):
  id = models.IntegerField(primary_key = True)
  stock_code = models.CharField(max_length = 20)
  stock_name = models.CharField(max_length = 20)
  credit_code = models.CharField(max_length = 20)
  company_name = models.CharField(max_length = 100)
  found_date = models.CharField(max_length=20)
  business_code = models.CharField(max_length = 20)
  registered_capital = models.CharField(max_length = 20)
  legal_representative = models.CharField(max_length = 50)
  phone = models.CharField(max_length = 50)
  registered_address = models.CharField(max_length = 200)
  website = models.CharField(max_length = 100)
  profile = models.TextField()
  stock_type = models.CharField(max_length = 20,null=True)
  business_scope = models.TextField()
  listed = models.IntegerField(default= 0)
  deteled = models.IntegerField(default= 0)

  class Meta:
        ordering = ('id', 'credit_code')