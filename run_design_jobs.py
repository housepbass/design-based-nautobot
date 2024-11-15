"""Module for running design jobs."""
import os
import logging
from time import sleep
from pynautobot import api

logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)

nb = api(url=os.environ["NAUTOBOT_URL"], token=os.environ["NAUTOBOT_TOKEN"], verify=False)

JOB_STATUSES = ["PENDING", "FAILURE", "COMPLETED", "CANCELLED", "CREATED", "SUCCESS"]

# Dynamically find all Design Jobs
DESIGN_JOBS = nb.extras.jobs.filter(grouping="Design Builder", name__nie="Decommission Design Deployments")

for design_job in DESIGN_JOBS:
    job_run = nb.extras.jobs.run(job_id=design_job.id, data={"dryrun": False, "deployment_name": design_job.name})
    result = nb.extras.job_results.get(job_run.job_result.id)

    while result.status.value not in JOB_STATUSES:
        result = nb.extras.job_results.get(job_run.job_result.id)
        logging.info("Design Job `%s` is running...", design_job.name)
        sleep(5)

    if result.status.value != "SUCCESS":
        msg = f"Design Job failed with traceback `{result.traceback}`"
        raise Exception(msg)

    logging.info("Design Job `%s` completed with status `%s`", design_job.name, result.status.value)
