from nautobot.apps.jobs import register_jobs
from .hello_jobs import HelloJobs,
from .HelloJobsGit import HelloJobsGit

register_jobs(HelloJobs, HelloJobsGit)
