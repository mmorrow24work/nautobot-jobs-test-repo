from nautobot.apps.jobs import register_jobs
from .hello_jobs import HelloJobs
from .HelloJobsGit import HelloJobsGit
from .HelloJobsGit import file_upload

register_jobs(HelloJobs, HelloJobsGit, FileUpload)
