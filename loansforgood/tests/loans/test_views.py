from unittest import mock

import pytest
from apps.loans.choices import ProposalStatus
from django.urls import reverse
from rest_framework import status

from .factories import ProposalFactory

pytestmark = pytest.mark.django_db


class TestProposalFieldView:
    def test_create(self, api_client, valid_proposal_field_data):
        url = reverse("proposal-fields-list")
        response = api_client.post(url, valid_proposal_field_data)
        assert response.status_code == status.HTTP_201_CREATED

    def test_read(self, api_client, proposal_field):
        url = reverse("proposal-fields-list")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 1

    def test_update(self, api_client, proposal_field, valid_proposal_field_data):
        updated_data = valid_proposal_field_data.copy()
        updated_data["name"] = "updated_name"
        url = reverse("proposal-fields-detail", args=[proposal_field.id])
        response = api_client.put(url, updated_data)
        assert response.status_code == status.HTTP_200_OK
        proposal_field.refresh_from_db()
        assert proposal_field.name == "updated_name"


class TestProposalView:
    @mock.patch("apps.loans.views.AutomaticProposalEvaluationTask", mock.Mock())
    def test_create(self, api_client, proposal_field, valid_proposal_data):
        valid_proposal_data["custom_data"] = {proposal_field.name: "some_value"}

        url = reverse("proposals-list")
        response = api_client.post(url, valid_proposal_data, format="json")
        assert response.status_code == status.HTTP_201_CREATED

    def test_read(self, api_client, proposal):
        url = reverse("proposals-list")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 1

    def test_update(self, api_client, proposal_field, valid_proposal_data):
        proposal = ProposalFactory(
            status=ProposalStatus.PENDING,
            custom_data={proposal_field.name: "some_value"},
        )

        updated_data = valid_proposal_data.copy()
        updated_data["status"] = ProposalStatus.PENDING_HUMAN_APPROVAL
        url = reverse("proposals-detail", args=[proposal.id])
        response = api_client.put(url, updated_data, format="json")
        assert response.status_code == status.HTTP_200_OK
        proposal.refresh_from_db()
        assert proposal.status == ProposalStatus.PENDING_HUMAN_APPROVAL
