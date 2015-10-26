#!/bin/usr/python2.7
__author__ = 'BrennanVanderLaan'

import tornado
import tornado.web
import tornado.ioloop
from tornado.tcpserver import TCPServer
import json


class VersionHandler(tornado.web.RequestHandler):
    def get(self):
        response = {'version': '0.0.1',
                    'last_build': "N/A"}
        self.write(response)

class HandleUpdate(tornado.web.RequestHandler):
    def post(self):
        print "Got webhook post!"
        try:
            data = json.loads(self.request.body)
            print "Event type: " + str(self.request.headers.get("X-Github-Event"))
            print data
        except Exception as e:
            print e
            raise e


app = tornado.web.Application([
    (r'/webhook', HandleUpdate)
])

if __name__ == "__main__":
    print "Starting up..."
    app.listen(8081)
    tornado.ioloop.IOLoop.instance().start()