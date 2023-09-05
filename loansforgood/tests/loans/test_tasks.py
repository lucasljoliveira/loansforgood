from unittest.mock import Mock, patch

import pytest
from apps.loans.tasks import AutomaticProposalEvaluationTask
from django.conf import settings
from django.test import TestCase
from rest_framework import status

from .factories import ProposalFactory

pytestmark = pytest.mark.django_db


class TestPerformTask(TestCase):
    def test_perform_task(self):
        proposal = ProposalFactory()
        valid_proposal_task_data = {
            "proposal_id": proposal.id,
            "document": "some_document",
            "name": "some_name",
        }

        url = settings.LOAN_PROCESSOR_URL

        mock_response = Mock(status_code=status.HTTP_200_OK)
        mock_response.json.return_value = {"approved": True}

        with patch("requests.post", return_value=mock_response) as post_mock:
            result = AutomaticProposalEvaluationTask.perform_task(
                **valid_proposal_task_data
            )

            post_mock.assert_called_once_with(
                url=url,
                json={
                    "document": valid_proposal_task_data["document"],
                    "name": valid_proposal_task_data["name"],
                },
                headers={"Content-Type": "application/json"},
            )

            assert result
