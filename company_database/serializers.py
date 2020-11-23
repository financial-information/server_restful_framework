from rest_framework import serializers

from company_database.models import CompanyBasicInformation




class CompanyBasicInformationSerializer(serializers.ModelSerializer):
  class Meta:
        model = CompanyBasicInformation
        fields = ('id', 'stock_code', 'stock_name', 'credit_code', 'company_name', 'found_date', 'business_code', 
          'registered_capital', 'legal_representative', 'phone', 'registered_address', 'website', 'profile', 'stock_type', 'business_scope', 'listed',
          'deteled')
