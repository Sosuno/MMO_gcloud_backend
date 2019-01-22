import webapp2

class EnqueueActionsHandler(webapp2.RequestHandler):
    def post(self):
        thingstodo = None # get things to do

        def update_db_state():
            # execute the actions
            
        update_db_state()


app = webapp2.WSGIApplication([
    ('/update_counter', EnqueueActionsHandler)
], debug=True)