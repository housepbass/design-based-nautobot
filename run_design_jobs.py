"""Module for running design jobs."""
import os
from time import sleep
from pynautobot import api

nb = api(url=os.environ["PROD_NAUTOBOT_URL"], token=os.environ["PROD_NAUTOBOT_TOKEN"], verify=False)

#TODO: Dynamically find all Design Jobs and run them if they've changed
design_job = nb.extras.jobs.get(name="Initial Data")

#TODO: Figure out how to generate deployment names, map them to Designs. Maybe just use the design name?
job_run = nb.extras.jobs.run(job_id=design_job.id, data={"dryrun": False, "deployment_name": "Initial Data"})
result = nb.extras.job_results.get(job_run.job_result.id)

job_statuses = ["PENDING", "FAILURE", "COMPLETED", "CANCELLED", "CREATED", "SUCCESS"]

while result.status.value not in job_statuses:
    result = nb.extras.job_results.get(job_run.job_result.id)
    print("Job is running...")
    sleep(1)

if result.status.value != "SUCCESS":
    msg = f"Design Job failed with traceback `{result.traceback}`"
    raise Exception(msg)

print(f"Job completed with status `{result.status.value}`")
# TODO: PRINT JOB LOGS