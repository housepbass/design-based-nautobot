"""Tests module."""

from unittest import TestCase
from nautobot.extras.models.jobs import Job
from nautobot.apps.testing import (
    TransactionTestCase,
    create_job_result_and_run_job,
)

# Get all design jobs that are grouped into the "Design Builder" category
# except for the app provided Job.
DESIGN_JOBS = Job.objects.filter(grouping="Design Builder").exclude(name="Decommission Design Deployments")

class RunJobTestCase(TransactionTestCase, TestCase):
    """Test Class."""

    def setUp(self) -> None:
        """Run setup tasks."""
        super().setUp()

    def test_design_jobs(self):
        """Verify Jobs run successfully."""
        for design_job in DESIGN_JOBS:
            with self.subTest(design_job=design_job):
                job_result = create_job_result_and_run_job(
                    module=design_job.module_name,
                    name=design_job.class_path.split(".")[-1],
                    deployment_name=design_job.name,
                    dryrun=False,
                )
                self.assertEqual("SUCCESS", job_result.status, job_result.traceback)
