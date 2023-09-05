from rest_framework import mixins, status
from rest_framework.viewsets import GenericViewSet

from .filters import ProposalFilter
from .models import Proposal, ProposalField, ProposalFieldValue
from .serializers import ProposalFieldSerializer, ProposalSerializer
from .tasks import AutomaticProposalEvaluationTask


class ProposalView(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = Proposal.objects.all()
    serializer_class = ProposalSerializer
    filterset_class = ProposalFilter
    search_fields = ["status"]

    def send_background_task(self, result):
        id = result.data.get("id")
        document = result.data.get("custom_data").get("document")
        name = result.data.get("custom_data").get("name")

        return AutomaticProposalEvaluationTask.perform_task.delay(id, document, name)

    def create_proposal_field_values(self, result):
        custom_data = result.data.get("custom_data")
        proposal_id = result.data.get("id")
        proposal_fields = ProposalField.objects.all()

        for key, value in custom_data.items():
            proposal_field = proposal_fields.get(name=key)
            ProposalFieldValue.objects.create(
                proposal_id=proposal_id,
                proposal_field_id=proposal_field.id,
                value=value,
            )

    def create(self, request, *args, **kwargs):
        result = super().create(request, *args, **kwargs)

        self.create_proposal_field_values(result)

        if result.status_code == status.HTTP_201_CREATED:
            self.send_background_task(result)

        return result


class ProposalFieldView(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = ProposalField.objects.all()
    serializer_class = ProposalFieldSerializer
