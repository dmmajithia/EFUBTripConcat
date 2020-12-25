from threading import Thread, Timer
from concurrent.futures import Future

# 'call_with_future' & 'threaded' related source from - 
# https://stackoverflow.com/questions/19846332/python-threading-inside-a-class
def call_with_future(fn, future, args, kwargs):
	try:
		result = fn(*args, **kwargs)
		future.set_result(result)
	except Exception as exc:
		future.set_exception(exc)

def threaded(fn):
	# To wait on a @threaded function, call {return_obj}.result()
	def wrapper(*args, **kwargs):
		future = Future()
		Thread(target=call_with_future, args=(fn, future, args, kwargs)).start()
		return future
	return wrapper


# https://stackoverflow.com/a/48741004/13956685
class RepeatTimer(Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)