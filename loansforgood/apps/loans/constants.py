from .choices import ProposalStatus

NEXT_PROPOSAL_STATUS_MAPPING = {
    ProposalStatus.PENDING: [
        ProposalStatus.PENDING_HUMAN_APPROVAL,
        ProposalStatus.REJECTED,
    ],
    ProposalStatus.PENDING_HUMAN_APPROVAL: [
        ProposalStatus.APPROVED,
        ProposalStatus.REJECTED,
    ],
}
