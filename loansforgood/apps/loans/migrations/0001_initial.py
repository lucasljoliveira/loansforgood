import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Proposal",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("custom_data", models.JSONField()),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("PENDING", "Pending"),
                            ("APPROVED", "Approved"),
                            ("REJECTED", "Rejected"),
                            ("PENDING_HUMAN_APPROVAL", "Pending Human Approval"),
                        ],
                        default="PENDING",
                        max_length=30,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="ProposalField",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=100)),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("STR", "STR"),
                            ("INT", "INT"),
                            ("DATE", "DATE"),
                            ("DATETIME", "DATETIME"),
                            ("DECIMAL", "DECIMAL"),
                        ],
                        default="STR",
                        max_length=50,
                    ),
                ),
                ("required", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="ProposalFieldValue",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("value", models.CharField(default="", max_length=255)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "proposal",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="field_value",
                        to="loans.proposal",
                    ),
                ),
                (
                    "proposal_field",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="fields",
                        to="loans.proposalfield",
                    ),
                ),
            ],
        ),
        migrations.AddConstraint(
            model_name="proposalfield",
            constraint=models.CheckConstraint(
                check=models.Q(
                    ("type__in", ["STR", "INT", "DATE", "DATETIME", "DECIMAL"])
                ),
                name="loans_proposalfield_type_valid",
            ),
        ),
        migrations.AddConstraint(
            model_name="proposal",
            constraint=models.CheckConstraint(
                check=models.Q(
                    (
                        "status__in",
                        ["PENDING", "APPROVED", "REJECTED", "PENDING_HUMAN_APPROVAL"],
                    )
                ),
                name="loans_proposal_status_valid",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="proposalfieldvalue",
            unique_together={("proposal", "proposal_field")},
        ),
    ]
