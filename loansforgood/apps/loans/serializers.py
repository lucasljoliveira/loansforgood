from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from .constants import NEXT_PROPOSAL_STATUS_MAPPING
from .models import Proposal, ProposalField, ProposalFieldValue


class ProposalSerializer(ModelSerializer):
    def validate(self, attrs):
        is_create = True if not self.instance else False
        new_status = attrs.get("status", None)
        old_status = self.instance.status if not is_create else None
        is_status_change = old_status != new_status

        if not is_create and new_status and is_status_change:
            valid_next_status = NEXT_PROPOSAL_STATUS_MAPPING.get(old_status, list())
            if not valid_next_status:
                raise ValidationError(
                    {"status": f"Instance status {old_status} cannot be changed"}
                )

            is_valid_next_status = (
                True if new_status not in valid_next_status else False
            )
            if is_valid_next_status:
                raise ValidationError(
                    {
                        "status": f"Value {new_status} is not a valid next status, options: {', '.join(valid_next_status)}"
                    }
                )

        return super().validate(attrs)

    class Meta:
        model = Proposal
        fields = "__all__"
        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )


class ProposalFieldSerializer(ModelSerializer):
    class Meta:
        model = ProposalField
        fields = "__all__"
        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )


class ProposalFieldValueSerializer(ModelSerializer):
    class Meta:
        model = ProposalFieldValue
        fields = "__all__"
        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )
