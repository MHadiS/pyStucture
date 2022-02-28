class Node:
    """a class to make data structures
    """

    def __init__(self, data):
        self.data = data  # a to store in the node
        self.link = None  # the next node


class Stack:
    """a class for saving stack and give you stack data structure
    """

    def __init__(self):
        """Define needed variables for other methods
        """
        self.first = Node(None)
        self.length = 0

    def put(self, value):
        """put a new element in the stack

        Args:
            value (any): the new value you want to put in stack
        """
        if not self.length:
            self.first.data = value
        else:
            new_node = Node(value)
            new_node.link = self.first
            self.first = new_node
        self.length += 1

    def push(self, value):
        self.put(value)

    def get(self):
        """give you the first element and remove it

        Returns:
            any: the first element 
        """
        value = self.first.data
        if not self.length:
            self.show_error()
        elif self.length == 1:
            self.first.data = None
        else:
            self.first = self.first.link
        self.length -= 1
        return value

    def pop(self):
        self.get()

    def clear(self):
        """clear the stack
        """
        del self.first
        self.length = 0
        self.first = Node(None)

    def is_empty(self):
        """check the stack is empty or not

        Returns:
            boolean: if it was True, the stack is empty
        """
        return not self.length

    def show_error(self):
        """show stack overflow error

        Raises:
            IndexError: this happened when you pop from and empty stack
        """
        raise IndexError("Stack overflow")

    def show(self):
        """print the stack values
        """
        green = "\033[92m text \033[00m"
        red = "\033[91m text \033[00m"
        yellow = "\033[93m text \033[00m"
        cyan = "\033[96m text \033[00m"
        print(red.replace("text", "("))
        node = self.first
        for i in range(self.length):
            type_ = type(node.data)
            if type_ == int or type_ == float:
                print(yellow.replace("text", f"\t{node.data},"))
            elif type_ == str:
                print(green.replace("text", f"\t'{node.data}',"))
            elif type_ == list or type_ == tuple or type_ == set or type_ == dict:
                print(cyan.replace("text", f"\t{node.data},"))
            else:
                print(f"\t{node},")
            node = node.link
        print(red.replace("text", ")\n"))

    def count(self, value):
        n = 0
        node = self.first
        for i in range(self.length):
            if node.data == value:
                n += 1
            node = node.link
        return n
