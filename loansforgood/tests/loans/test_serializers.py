import pytest
from apps.loans.choices import ProposalStatus
from apps.loans.serializers import (
    ProposalFieldSerializer,
    ProposalFieldValueSerializer,
    ProposalSerializer,
)
from rest_framework.exceptions import ValidationError

from .factories import ProposalFactory

pytestmark = pytest.mark.django_db


class TestProposalSerializer:
    def test_is_valid(self, valid_proposal_data):
        serializer = ProposalSerializer(data=valid_proposal_data)
        assert serializer.is_valid() is True

    @pytest.mark.parametrize(
        "old_status, next_status",
        [
            [ProposalStatus.PENDING, ProposalStatus.PENDING_HUMAN_APPROVAL],
            [ProposalStatus.PENDING, ProposalStatus.REJECTED],
            [ProposalStatus.PENDING_HUMAN_APPROVAL, ProposalStatus.REJECTED],
            [ProposalStatus.PENDING_HUMAN_APPROVAL, ProposalStatus.APPROVED],
        ],
    )
    def test_validate_status_change(self, old_status, next_status, valid_proposal_data):
        proposal = ProposalFactory(status=old_status)
        valid_proposal_data["status"] = next_status

        serializer = ProposalSerializer(instance=proposal, data=valid_proposal_data)
        assert serializer.is_valid() is True

    @pytest.mark.parametrize(
        "old_status, next_status",
        [
            [ProposalStatus.REJECTED, ProposalStatus.APPROVED],
            [ProposalStatus.APPROVED, ProposalStatus.REJECTED],
            [ProposalStatus.PENDING, "INVALID"],
            [ProposalStatus.PENDING_HUMAN_APPROVAL, "INVALID"],
        ],
    )
    def test_validate_invalid_status(
        self, old_status, next_status, valid_proposal_data
    ):
        proposal = ProposalFactory(status=old_status)
        valid_proposal_data["status"] = next_status

        serializer = ProposalSerializer(instance=proposal, data=valid_proposal_data)
        with pytest.raises(ValidationError) as excinfo:
            serializer.is_valid(raise_exception=True)
        assert "status" in excinfo.value.detail


class TestProposalFieldSerializer:
    def test_is_valid(self, valid_proposal_field_data):
        serializer = ProposalFieldSerializer(data=valid_proposal_field_data)
        assert serializer.is_valid() is True

    def test_is_invalid(self):
        invalid_proposal_field_data = {}
        serializer = ProposalFieldSerializer(data=invalid_proposal_field_data)
        with pytest.raises(ValidationError) as excinfo:
            serializer.is_valid(raise_exception=True)
        assert "name" in excinfo.value.detail


class TestProposalFieldValueSerializer:
    def test_is_valid(self, valid_proposal_field_value_data):
        serializer = ProposalFieldValueSerializer(data=valid_proposal_field_value_data)
        assert serializer.is_valid(raise_exception=True) is True

    def test_is_invalid(self):
        invalid_proposal_field_value_data = {}
        serializer = ProposalFieldValueSerializer(
            data=invalid_proposal_field_value_data
        )
        with pytest.raises(ValidationError) as excinfo:
            serializer.is_valid(raise_exception=True)
        assert "proposal" in excinfo.value.detail
        assert "proposal_field" in excinfo.value.detail
