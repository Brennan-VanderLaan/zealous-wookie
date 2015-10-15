__author__ = 'Brennan VanderLaan'

import tornado.web
import tornado.websocket
import tornado.options
import tornado.ioloop
import tornado.escape
import uuid

import os.path

from tornado.options import define, options

define("port", default=8080, help="Run on the given port", type=int)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/app/*/(.*)', tornado.web.StaticFileHandler, {"path": os.path.dirname(__file__)}),
            (r'/app/', FileServer),
            (r'/app/endpoints/chat', WebSocket)
        ]
        settings = {
            'cookie_secret': str(uuid.uuid4()),
            'template_path': os.path.join(os.path.dirname(__file__), "html_src"),
            'static_path': os.path.join(os.path.dirname(__file__), "scripts"),
            'xsrf_cookies': True
        }

        tornado.web.Application.__init__(self, handlers, **settings)


class FileServer(tornado.web.RequestHandler):
    def get(self):
        print "FileServer got request: " + str(self)
        self.render("index.html", messages=WebSocket.chatText)


class WebSocket(tornado.websocket.WebSocketHandler):
    waiters = set()
    chatText = []
    maxLength = 250


    def get_compression_options(self):
        return {}

    def open(self):
        WebSocket.waiters.add(self)

    def on_close(self):
        WebSocket.waiters.remove(self)

    @classmethod
    def update_chat(cls, chat):
        cls.chatText.append(chat)

        if len(cls.chatText) > cls.maxLength:
            cls.chatText = cls.chatText[(len(cls.chatText) / 2):]

    @classmethod
    def send_updates(cls, chat):
        print "Sending message to %d waiters" % len(cls.waiters)

        for waiter in cls.waiters:
            try:
                waiter.write_message(chat)
            except:
                print "Error sending message to waiter!"

    def on_message(self, message):
        print "Got message: " + str(message)

        parsed = tornado.escape.json_decode(message)
        chat = {
            "id": str(uuid.uuid4()),
            "body": parsed['body']
        }
        chat['html'] = tornado.escape.to_basestring(
            self.render_string("message.html", message=chat))

        WebSocket.update_chat(chat)
        WebSocket.send_updates(chat)

def main():
    tornado.options.parse_command_line()
    app = Application()
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    main()