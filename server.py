import os

from tornado import websocket, web, ioloop
import tornado
import json

from serial import Serial

from interactive import generate_taxi_stream

serial = None
arduino_writer = None

def cost2bytes(cost):
    '''
    Convert a float to 4 bytes for the 7-segment display.

    0.01 -> "0000", 10.01 -> "1001", etc.
    '''
    return ("0000" + "%.2f" % cost).replace(".", "")[-4:]

## web app ####################################################################

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("web/index.html")

class SocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        self.stream = None
        global arduino_writer
        if not arduino_writer:
            arduino_writer = self

    def on_close(self):
        pass

    def on_message(self, msg):
        msg = json.loads(msg)
        if msg['cmd'] == 'start':
            csvs = [f for f in os.listdir("data") if f.endswith("csv")]
            csv = csvs[msg['id']]
            self.stream = generate_taxi_stream("data/%s" % csv)
            self.write_message(json.dumps({"ok": 1}))
        elif msg['cmd'] == 'next':
            next_row = next(self.stream)

            #write to websocket
            self.write_message(json.dumps(next_row))

            #write to arduino
            global arduino_writer, serial
            if arduino_writer == self and serial is not None:
                serial.write(cost2bytes(next_row['cost']))

app = tornado.web.Application([
    (r'/', IndexHandler),
    (r'/ws', SocketHandler),
], static_path="web/static")

if __name__ == '__main__':
    try:
        serial = Serial('/dev/cu.usbmodemfa131', 9600, timeout=1)
    except:
        pass

    app.listen(80)
    tornado.ioloop.IOLoop.instance().start()
