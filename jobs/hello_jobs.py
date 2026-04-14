from nautobot.apps.jobs import Job

name = "Jobs Collection from https://github.com/mmorrow24work/nautobot-jobs-test-repo"

class HelloJobs(Job):

    class Meta: 
        name = "Hello Jobs from Git Repo"

    def run(self):
        self.logger.debug("This is from the Git repo.")
