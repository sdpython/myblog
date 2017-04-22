import threading, time

class MyThread(threading.Thread):
    def run(self):
        while True:
            time.sleep(1)
            
th = MyThread()
th.daemon=True
th.start()

#th._stop()
