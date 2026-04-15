from nautobot.apps.jobs import register_jobs
from .hello_jobs import HelloJobs
from .HelloJobsGit import HelloJobsGit
from .file_upload import FileUpload

register_jobs(HelloJobs, HelloJobsGit, FileUpload)
