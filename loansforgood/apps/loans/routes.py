from rest_framework import routers

from .views import ProposalFieldView, ProposalView

router = routers.DefaultRouter()
router.register(r"proposals", ProposalView, basename="proposals")
router.register(r"proposal-fields", ProposalFieldView, basename="proposal-fields")
