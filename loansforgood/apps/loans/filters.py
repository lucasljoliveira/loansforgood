from django_filters import FilterSet

from .models import Proposal


class ProposalFilter(FilterSet):
    class Meta:
        model = Proposal
        fields = {"status": ["exact"]}
