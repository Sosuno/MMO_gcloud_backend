from google.appengine.api import taskqueue
import webapp2

class EnqueueTaskHandler(webapp2.RequestHandler):
    def post(self):
        thingstodo = None  # get things to do

        task = taskqueue.add(
            url='/enqueue_actions',
            target='worker',
            params={'thingstodo': thingstodo})

        self.response.write(
            'Task {} enqueued, ETA {}.'.format(task.name, task.eta))