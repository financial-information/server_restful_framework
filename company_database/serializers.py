from rest_framework import serializers

from company_database.models import CompanyBasicInformation,CompanyFinanceData




class CompanyBasicInformationSerializer(serializers.ModelSerializer):
  class Meta:
        model = CompanyBasicInformation
        fields = ('id', 'stock_code', 'stock_name', 'credit_code', 'company_name', 'found_date', 'business_code', 
          'registered_capital', 'legal_representative', 'phone', 'registered_address', 'website', 'profile', 'stock_type', 'industry_type','business_scope', 'listed',
          'deleted')



class CompanyFinanceDataSerializer(serializers.ModelSerializer):
  class Meta:
        model = CompanyFinanceData
        fields = '__all__'
