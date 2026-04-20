from nautobot.apps.jobs import register_jobs
from .hello_jobs import HelloJobs
from .HelloJobsGit import HelloJobsGit
from .file_upload2 import FileUpload, FileUpload_2

register_jobs(HelloJobs, HelloJobsGit, FileUpload, FileUpload_2)
