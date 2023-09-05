import requests
from celery import shared_task
from django.conf import settings
from rest_framework import status

from .choices import ProposalStatus
from .models import Proposal


class AutomaticProposalEvaluationTask:
    @shared_task
    def perform_task(proposal_id, document, name):
        url = settings.LOAN_PROCESSOR_URL
        json = {"document": document, "name": name}
        headers = {"Content-Type": "application/json"}
        result = requests.post(url=url, json=json, headers=headers)

        if result.status_code == status.HTTP_200_OK:
            data_result = result.json()

            is_approved = data_result.get("approved")
            new_status = (
                ProposalStatus.PENDING_HUMAN_APPROVAL
                if is_approved
                else ProposalStatus.REJECTED
            )

            return Proposal.objects.filter(pk=proposal_id).update(status=new_status)
