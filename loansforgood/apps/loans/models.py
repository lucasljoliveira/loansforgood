from django.db import models

from .choices import ProposalFieldTypes, ProposalStatus


class Proposal(models.Model):
    id = models.AutoField(primary_key=True)

    custom_data = models.JSONField()
    status = models.CharField(
        max_length=30, choices=ProposalStatus.choices, default=ProposalStatus.PENDING
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"Proposal {self.id}"

    class Meta:
        constraints = [
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_status_valid",
                check=models.Q(status__in=ProposalStatus.values),
            )
        ]


class ProposalField(models.Model):
    id = models.AutoField(primary_key=True)

    name = models.CharField(max_length=100)
    type = models.CharField(
        choices=ProposalFieldTypes.choices,
        default=ProposalFieldTypes.STR,
        max_length=50,
    )
    required = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        constraints = [
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_type_valid",
                check=models.Q(type__in=ProposalFieldTypes.values),
            )
        ]


class ProposalFieldValue(models.Model):
    id = models.AutoField(primary_key=True)

    proposal = models.ForeignKey(
        Proposal, related_name="field_value", on_delete=models.DO_NOTHING
    )
    proposal_field = models.ForeignKey(
        ProposalField, related_name="fields", on_delete=models.DO_NOTHING
    )
    value = models.CharField(max_length=255, default="")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("proposal", "proposal_field")

    def __str__(self) -> str:
        return f"ID: {str(self.id)}"
