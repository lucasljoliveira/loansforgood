import factory
from apps.loans.models import Proposal, ProposalField, ProposalFieldValue


class ProposalFactory(factory.django.DjangoModelFactory):
    custom_data = {"key": "value"}

    class Meta:
        model = Proposal


class ProposalFieldFactory(factory.django.DjangoModelFactory):
    name = "name"

    class Meta:
        model = ProposalField


class ProposalFieldValueFactory(factory.django.DjangoModelFactory):
    proposal = factory.SubFactory(factory=ProposalFactory)
    proposal_field = factory.SubFactory(factory=ProposalFieldFactory)
    value = "some_value"

    class Meta:
        model = ProposalFieldValue
