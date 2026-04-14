from nautobot.apps.jobs import Job, register_jobs

class HelloJobsGit(Job):

    class Meta: 
        name = "Hello Jobs from Git Repo - HelloJobsGit.py"

    def run(self):
        self.logger.debug("This is from the Git repo - HelloJobsGit.py")


register_jobs(
    HelloJobsGit,
)
