from nautobot.apps.jobs import register_jobs
from .hello_jobs import HelloJobs HelloJobsGit

register_jobs(HelloJobs, HelloJobsGit)
