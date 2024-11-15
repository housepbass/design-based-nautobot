"""Module for syncing git to Nautobot."""
import os
import logging
from time import sleep
from pynautobot import api

logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)

nb = api(url=os.environ["NAUTOBOT_URL"], token=os.environ["NAUTOBOT_TOKEN"], verify=False)

sync_repo_job = nb.extras.jobs.get(name="Git Repository: Sync")
jobs_repo = nb.extras.git_repositories.get(name="Jobs Repo")

job_run = nb.extras.jobs.run(job_id=sync_repo_job.id, data={"repository": jobs_repo.id})
result = nb.extras.job_results.get(job_run.job_result.id)

job_statuses = ["PENDING", "FAILURE", "COMPLETED", "CANCELLED", "CREATED", "SUCCESS"]

while result.status.value not in job_statuses:
    result = nb.extras.job_results.get(job_run.job_result.id)
    logging.info("Git Sync is running...")
    sleep(1)


logging.info("Git Sync Job completed with status `%s`", result.status.value)
