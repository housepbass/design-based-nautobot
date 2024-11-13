"""Initial data required for core sites."""
from nautobot.apps.jobs import register_jobs

from nautobot_design_builder.choices import DesignModeChoices
from nautobot_design_builder.design_job import DesignJob

from .context import InitialDesignContext


class InitialDesign(DesignJob):
    """Initialize the database with default values needed by the core site designs."""
    has_sensitive_variables = False

    class Meta:
        """Metadata needed to implement the backbone site design."""

        name = "Initial Data"
        commit_default = False
        design_files = [
            "designs/0001_initial.yaml.j2",
        ]
        version = "1.0.0"
        context_class = InitialDesignContext
        design_mode = DesignModeChoices.DEPLOYMENT

# Group all designs into the "Design Builder" Jobs section so unittests can discover them
name = "Design Builder"
register_jobs(InitialDesign)