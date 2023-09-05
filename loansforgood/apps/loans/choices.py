from django.db.models import TextChoices


class ProposalStatus(TextChoices):
    PENDING = "PENDING", "Pending"
    APPROVED = "APPROVED", "Approved"
    REJECTED = "REJECTED", "Rejected"
    PENDING_HUMAN_APPROVAL = "PENDING_HUMAN_APPROVAL", "Pending Human Approval"


class ProposalFieldTypes(TextChoices):
    STR = "STR", "STR"
    INT = "INT", "INT"
    DATE = "DATE", "DATE"
    DATETIME = "DATETIME", "DATETIME"
    DECIMAL = "DECIMAL", "DECIMAL"
