from apps.loans.choices import ProposalFieldTypes
from apps.loans.models import ProposalField
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create proposal default custom fields"

    def handle(self, *args, **kwargs):
        ProposalField.objects.get_or_create(
            name="document", type=ProposalFieldTypes.STR
        )
        ProposalField.objects.get_or_create(name="name", type=ProposalFieldTypes.STR)
        self.stdout.write(
            self.style.SUCCESS("Proposal default fields created successfully!")
        )
