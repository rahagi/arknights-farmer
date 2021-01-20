import threading
import ctypes

class FarmerThread():

    THREAD = None

    @classmethod
    def create(self, target, args=(), kwargs={}):
        self.THREAD = threading.Thread(
            target=target,
            args=args,
            kwargs=kwargs,
            name="FarmerThread"
        )
        return self.THREAD
    
    @classmethod
    def get_id(self): 
        for id, thread in threading._active.items(): 
            if thread is self.THREAD:
                return id

    @classmethod
    def raise_exception(self, exception):
        # https://gist.github.com/liuw/2407154
        try:
            tid = ctypes.c_long(self.get_id())
            ret = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exception))
            if ret > 1:
                ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, 0)
        except TypeError:
            return
            
