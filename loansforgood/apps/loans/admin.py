from django import forms
from django.contrib import admin

from .choices import ProposalStatus
from .models import Proposal, ProposalField, ProposalFieldValue


class ProposalFieldValueInline(admin.TabularInline):
    model = ProposalFieldValue
    can_delete = False
    extra = 0
    readonly_fields = ["proposal_field", "proposal", "value"]


class ProposalAdminForm(forms.ModelForm):
    class Meta:
        model = Proposal
        fields = "__all__"

    status = forms.ChoiceField(
        choices=[
            (ProposalStatus.APPROVED, "Aprovado"),
            (ProposalStatus.REJECTED, "Rejeitado"),
            (ProposalStatus.PENDING_HUMAN_APPROVAL, "Aguardando aprovação humana"),
        ]
    )

    def clean_status(self):
        cleaned_data = super().clean()
        status = cleaned_data.get("status")

        if status in [ProposalStatus.REJECTED, ProposalStatus.PENDING]:
            self.fields["status"].widget.attrs["readonly"] = True

        return status


class ProposalAdmin(admin.ModelAdmin):
    inlines = [
        ProposalFieldValueInline,
    ]
    form = ProposalAdminForm
    list_display = ("id", "status", "created_at", "updated_at")
    list_filter = ("status", "created_at", "updated_at")
    search_fields = ("status",)
    list_per_page = 20
    ordering = ("-created_at", "status")
    exclude = ["custom_data"]

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.status == ProposalStatus.REJECTED:
            return ["status"]

        return []


class ProposalFieldAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "type", "required", "created_at", "updated_at")
    list_filter = ("name", "type", "required", "created_at", "updated_at")
    search_fields = ("name", "type")
    list_per_page = 20
    ordering = ("-created_at", "name", "type")


admin.site.register(Proposal, ProposalAdmin)
admin.site.register(ProposalField, ProposalFieldAdmin)
