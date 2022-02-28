from pyStack import *


class Queue(Stack):
    """a class for saving queue and give you queue data structure
    """

    def put(self, value):
        """put a new element to queue

        Args:
            value (any): the new element value
        """
        if not self.length:
            self.first.data = value
        else:
            node = self.first
            for i in range(self.length - 1):
                node = node.link
            node.link = Node(value)
        self.length += 1

    def show_error(self):
        """show an error

        Raises:
            IndexError: when you get from empty queue this error raise
        """
        raise IndexError("can't 'get' from empty queue")
