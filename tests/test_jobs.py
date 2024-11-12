"""Tests module."""

from nautobot.apps.testing import (
    TransactionTestCase,
    create_job_result_and_run_job,
)

class RunJobTestCase(TransactionTestCase):
    """Test Class."""

    def setUp(self) -> None:
        """Run setup tasks."""
        super().setUp()

    def test_job(self):
        """Verify Job runs successfully."""
        job_result = create_job_result_and_run_job(
            module="initial_data",
            name="InitialDesign",
            dryrun=False,
        )
        self.assertEqual("SUCCESS", job_result.status, job_result.traceback)