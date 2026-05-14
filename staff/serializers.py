from rest_framework import serializers

from services.models import Service

from .models import StaffMember


class PublicStaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffMember
        fields = ('id', 'name')


class StaffMemberSerializer(serializers.ModelSerializer):
    # Write: list of service IDs; Read: list of service IDs
    services = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Service.objects.none(),  # overridden in __init__
    )

    class Meta:
        model = StaffMember
        fields = ('id', 'name', 'email', 'phone', 'is_active', 'services')
        read_only_fields = ('id',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Restrict service choices to the requesting user's business only.
        request = self.context.get('request')
        if request and hasattr(request.user, 'business'):
            self.fields['services'].child_relation.queryset = (
                Service.objects.filter(business=request.user.business)
            )
