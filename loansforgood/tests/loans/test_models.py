import pytest
from apps.loans.choices import ProposalFieldTypes, ProposalStatus
from apps.loans.models import Proposal, ProposalField, ProposalFieldValue
from django.db.utils import IntegrityError

pytestmark = pytest.mark.django_db


class TestProposal:
    def test_create(self):
        proposal = Proposal.objects.create(
            custom_data={"key": "value"},
            status=ProposalStatus.PENDING,
        )
        assert Proposal.objects.count() == 1
        assert proposal.id is not None
        assert proposal.created_at is not None
        assert proposal.updated_at is not None

    def test_defaults(self):
        proposal = Proposal.objects.create(custom_data={"key": "value"})
        assert proposal.status == ProposalStatus.PENDING

    def test_invalid_status(self):
        with pytest.raises(IntegrityError):
            Proposal.objects.create(
                custom_data={"key": "value"}, status="INVALIDSTATUS"
            )

    def test_updated_at(self):
        proposal = Proposal.objects.create(custom_data={"key": "value"})
        initial_updated_at = proposal.updated_at
        proposal.custom_data = {"key": "updated_value"}
        proposal.save()
        assert proposal.updated_at > initial_updated_at

    def test_str_method(self):
        proposal = Proposal.objects.create(custom_data={"key": "value"})
        assert str(proposal) == f"Proposal {proposal.id}"


class TestProposalField:
    def test_create(self):
        proposal_field = ProposalField.objects.create(
            name="some_field_name",
        )
        assert ProposalField.objects.count() == 1
        assert proposal_field.id is not None
        assert proposal_field.created_at is not None
        assert proposal_field.updated_at is not None

    def test_defaults(self):
        proposal_field = ProposalField.objects.create(
            name="some_field_name",
        )
        assert proposal_field.type == ProposalFieldTypes.STR

    def test_invalid_type(self):
        with pytest.raises(IntegrityError):
            ProposalField.objects.create(name="some_field_name", type="INVALIDTYPE")

    def test_updated_at(self):
        proposal_field = ProposalField.objects.create(name="some_field_name")
        initial_updated_at = proposal_field.updated_at
        proposal_field.name = "another_field_name"
        proposal_field.save()
        assert proposal_field.updated_at > initial_updated_at

    def test_str_method(self):
        proposal_field = ProposalField.objects.create(name="some_field_name")
        assert str(proposal_field) == proposal_field.name


class TestProposalFieldValue:
    def test_create(self, proposal, proposal_field):
        proposal_field = ProposalFieldValue.objects.create(
            value="some_field_value", proposal=proposal, proposal_field=proposal_field
        )
        assert ProposalFieldValue.objects.count() == 1
        assert proposal_field.id is not None
        assert proposal_field.created_at is not None
        assert proposal_field.updated_at is not None

    def test_create_error(self):
        with pytest.raises(IntegrityError):
            ProposalFieldValue.objects.create(value="some_field_value")

    def test_updated_at(self, proposal, proposal_field):
        proposal_field = ProposalFieldValue.objects.create(
            value="some_field_value", proposal=proposal, proposal_field=proposal_field
        )
        initial_updated_at = proposal_field.updated_at
        proposal_field.value = "another_field_value"
        proposal_field.save()
        assert proposal_field.updated_at > initial_updated_at

    def test_str_method(self, proposal, proposal_field):
        proposal_field = ProposalFieldValue.objects.create(
            value="some_field_value", proposal=proposal, proposal_field=proposal_field
        )
        assert str(proposal_field) == f"ID: {proposal_field.id}"
