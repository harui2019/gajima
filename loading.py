import threading
import time
from typing import (
    Union,
    Optional,
    Annotated,
    Callable,
    Generator,
    Iterable
)


class Gajima():
    """Another after another loading bar in Python, 
    are there any other Squidwards(X) python progressbar(O) ?

    - Why this name ?
        It's meaning "Don't leave" in Korean.
        Select this name because when I tested its main function,
        I was listening "TVXQ - Catch Me (Korean ver.)", and "Gajima" is its lyrics.
        So there is it.

    """
    

    def __init__(
        self,
        iterable: Iterable = range(1),
        prefix: str = '| ',
        desc: str = "Loading",
        finish_desc: str = "Completed",
        delay: Union[int, float] = 0.1,
        carousel: Union[tuple[str, any],
                        list[tuple[str, any]]] = ('dots', 15, 6),
        ANSIDecorator: str = "\u001b[1m",
        leave: bool = True,

    ):
        self.delay = delay
        self.prefix = prefix
        self.desc = desc
        self.finish_desc = finish_desc
        self.ANSIDecorator = ANSIDecorator
        self.leave = leave

        self.end = False
        self.threadLoading = None

        self.loading_carousel = []
        if not isinstance(carousel, list):
            carousel = [carousel]
            
        if not isinstance(iterable, Iterable):
            raise ValueError("Getting a not iterable object.")
        self.iterable = [v for v in iterable]
        self._cur_index = 0
        self._iter_len = len(self.iterable)

        carousel_dict = {
            'spinner': self.spinning_cursor,
            'dots': self.moving_dots,
        }
        for params in carousel:
            if not isinstance(params, tuple):
                params = (params, )
            if params[0] in carousel_dict:
                self.loading_carousel.append(
                    carousel_dict[params[0]](*params[1:]))
                
    def __iter__(self):
        # self._cur_index += 1
        while self._cur_index >= self._iter_len:
            raise StopIteration
        self._cur_index += 1
        return self

    def loading(self):
        cur = time.time()
        carousel_str = ''
        finished_desc = self.ANSIDecorator + self.finish_desc +"\u001b[0m"
        while not self.end:
            decorated_desc = self.ANSIDecorator + self.desc
            carousel_str = ' '
            for carousel in self.loading_carousel:
                carousel_str += next(carousel)+' '
            time.sleep(self.delay)
            print(self.prefix+decorated_desc +
                  carousel_str + "\u001b[0m"+f' - {round(time.time() - cur, 2)}s', end="\r")
            if self.end:
                break

        half_placeholder = (" "*(
            len(decorated_desc+carousel_str+"\u001b[0m")-len(finished_desc)))
        placeholder = (" "*len(
            self.prefix+f' - {round(time.time() - cur, 2)}s')
        ) + half_placeholder + " "*10
        print(placeholder, end="\r")
        if self.leave:
            print(self.prefix + finished_desc + half_placeholder + f' - {round(time.time() - cur, 2)}s')
        else:
            print(placeholder, end="\r")
            

    @staticmethod
    def spinning_cursor() -> Generator[str, None, None]:
        while 1:
            for cursor in '|/-\\':
                yield cursor

    @staticmethod
    def moving_dots(
        length: int = 10, 
        dots: int = 4
    ) -> Generator[str, None, None]:
        while 1:
            for i in range(length):
                dots_str_raw = ('.'*dots+' '*(length-dots))*2
                dots_str = dots_str_raw[length-i:2*length-i]
                yield dots_str

    def run(self):
        self.end = False
        self.threadLoading = threading.Thread(target=self.loading)
        self.threadLoading.start()

    def stop(self):
        if isinstance(self.threadLoading, threading.Thread):
            self.end = True
            self.threadLoading.join()
        else:
            print("Loading is not active.")
            
    def progressbar(self):
        cur = time.time()
        carousel_str = ''
        finished_desc = self.ANSIDecorator + self.finish_desc +"\u001b[0m"
        while not self.end:
            decorated_desc = self.ANSIDecorator + self.desc
            carousel_str = ' '
            for carousel in self.loading_carousel:
                carousel_str += next(carousel)+' '
            time.sleep(self.delay)
            print(self.prefix+decorated_desc +
                  carousel_str + "\u001b[0m"+f' - {round(time.time() - cur, 2)}s', end="\r")
            if self.end:
                break

        half_placeholder = (" "*(
            len(decorated_desc+carousel_str+"\u001b[0m")-len(finished_desc)))
        placeholder = (" "*len(
            self.prefix+f' - {round(time.time() - cur, 2)}s')
        ) + half_placeholder + " "*10
        print(placeholder, end="\r")
        if self.leave:
            print(self.prefix + finished_desc + half_placeholder + f' - {round(time.time() - cur, 2)}s')
        else:
            print(placeholder, end="\r")
            

    def __enter__(self):
        self.run()
        return self

    def __exit__(self, exception, exc_val, exc_tb):
        self.stop()
        if exception is not None:
            return False
