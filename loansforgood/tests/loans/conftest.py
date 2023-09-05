import pytest
from apps.loans.choices import ProposalStatus
from rest_framework.test import APIClient

from .factories import ProposalFactory, ProposalFieldFactory


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def proposal():
    return ProposalFactory()


@pytest.fixture
def proposal_field():
    return ProposalFieldFactory()


@pytest.fixture
def valid_proposal_data():
    return {"status": ProposalStatus.PENDING, "custom_data": {"key": "value"}}


@pytest.fixture
def valid_proposal_field_data():
    return {
        "name": "some_name",
    }


@pytest.fixture
def valid_proposal_field_value_data(proposal, proposal_field):
    return {
        "proposal": proposal.id,
        "proposal_field": proposal_field.id,
        "value": "some_value",
    }


@pytest.fixture
def valid_proposal_task_data():
    return {
        "proposal_id": "some_id",
        "document": "some_document",
        "name": "some_name",
    }
