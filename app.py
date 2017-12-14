import sys
from io import StringIO
from tornado.ioloop import IOLoop
from tornado.web import Application,RequestHandler,url
import myutil


class MainHandler(RequestHandler):
    def get(self):
        self.render("index.html", res='')

    def post(self):
        stmt = self.get_body_argument('stmt')
        old_stdout = sys.stdout
        redirected_output = sys.stdout = StringIO()
        try:
            exec(stmt, globals())
            self.render('index.html', res=">>> "+stmt+"\n"+redirected_output.getvalue())
        except Exception as e:
            self.render('error.html', err=str(e))
        finally: # !
            sys.stdout = old_stdout


def make_app():
    return Application([url(r"/", MainHandler)])

if __name__ == "__main__":
    fs = myutil.FastStop()
    fs.enable()
    app = make_app()
    app.listen(8080)
    IOLoop.current().start()
