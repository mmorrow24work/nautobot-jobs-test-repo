from nautobot.apps.jobs import register_jobs
from .hello_jobs import HelloJobs
from .HelloJobsGit import HelloJobsGit
from .file_upload2 import FileUpload, FileUpload_2
from .file_upload3 import FileUpload_3

register_jobs(HelloJobs, HelloJobsGit, FileUpload, FileUpload_2, FileUpload_3)
