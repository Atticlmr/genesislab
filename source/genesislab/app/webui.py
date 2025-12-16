

"""
最小 MJPEG 推流服务器
运行：  python app.py
然后浏览器打开 http://localhost:8888
"""
import genesis as gs
import tornado.ioloop
import tornado.web
import tornado.gen
import cv2
import numpy as np
from threading import Thread
import time

# ---------- 1. 初始化 Genesis ----------
gs.init()
scene = gs.Scene(show_viewer=False)
scene.add_entity(gs.morphs.Plane())
franka = scene.add_entity(gs.morphs.MJCF(file='xml/franka_emika_panda/panda.xml'))
cam = scene.add_camera(res=(640, 480))
scene.build()

# ---------- 2. 全局帧缓存 ----------
frame = None
lock = Thread()

def capture_loop():
    global frame
    while True:
        rgb, _ = cam.render()          # (H,W,3) uint8
        with lock:
            frame = rgb
        time.sleep(0.03)               # ~30 fps

Thread(target=capture_loop, daemon=True).start()

# ---------- 3. MJPEG 流 Handler ----------
class StreamHandler(tornado.web.RequestHandler):
    async def get(self):
        self.set_header('Content-Type', 'multipart/x-mixed-replace; boundary=frame')
        while True:
            if frame is None:
                await tornado.gen.sleep(0.01)
                continue
            with lock:
                _, jpeg = cv2.imencode('.jpg', frame[:,:,::-1])  # BGR↔RGB
            self.write(b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')
            await self.flush()

# ---------- 4. 静态首页 ----------
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')

# ---------- 5. 路由 ----------
def make_app():
    return tornado.web.Application([
        (r'/', MainHandler),
        (r'/stream', StreamHandler),
    ], static_path='.', template_path='.')

if __name__ == '__main__':
    app = make_app()
    app.listen(8888)
    print('👉 打开浏览器 http://localhost:8888')
    tornado.ioloop.IOLoop.current().start()