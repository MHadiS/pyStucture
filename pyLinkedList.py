from pyStack import Node


class LinkedList:
    """a class for saving linked list and give you linked list data structure
        you can define a linked list like this: NAME = LinkedList()
    """

    def __init__(self):
        """Define needed variables for other methods
        """
        self.root = Node(None)  # the first node
        self.length = 0  # length of linked list

    def get_obj(self, index: int):
        """get the node object in specific index

        Args:
            index (int): index of the node object

        Returns:
            Node: the node object
        """
        if self.length == 1:
            return self.root
        else:
            node = self.root
            for i in range(index):
                node = node.link
            return node

    def is_empty(self):
        """check the list is empty or not

        Returns:
            boolean: if it was True, the linked list is empty
        """
        return not self.length

    def get(self, index: int):
        """get value of a node object

        Args:
            index (int): index of node object

        Returns:
            any: the data of the node object
        """
        return self.get_obj(index).data

    def put(self, new_element):
        """put a new element in list

        Args:
            new_element (any): the new element
        """
        if self.root.data is None:
            self.root.data = new_element
        else:
            last_element = self.get_obj(self.length - 1)
            last_element.link = Node(new_element)
        self.length += 1

    def show(self):
        """print the list values
        """
        green = "\033[92m text \033[00m"
        red = "\033[91m text \033[00m"
        yellow = "\033[93m text \033[00m"
        cyan = "\033[96m text \033[00m"
        elements = [self.get(i) for i in range(self.length)]
        print(red.replace("text", "("))
        for element in elements:
            type_ = type(element)
            if type_ == int or type_ == float:
                print(yellow.replace("text", f"\t{element},"))
            elif type_ == str:
                print(green.replace("text", f"\t'{element}',"))
            elif type_ == list or type_ == tuple or type_ == set or type_ == dict:
                print(cyan.replace("text", f"\t{element},"))
            else:
                print(f"\t{element},")
        print(red.replace("text", ")\n"))

    def count(self, value):
        """count how many elements like value exist

        Args:
            value (any): the value you want to count

        Returns:
            int: a number to show how many times the value repeated
        """
        number = 0
        for i in range(self.length):
            element = self.get(i)
            if element == value:
                number += 1
        return number

    def clear(self):
        """
        empty the list
        """
        del self.root
        self.root = Node(None)
        self.length = 0

    def pop(self, index: int = -1):
        """remove and return the index

        Args:
            index (int): index of element you want to remove. Defaults to -1.

        Raises:
            IndexError: if the index was out of range

        Returns:
            any: value of removed element
        """
        if self.length == 0:
            raise IndexError("pop from empty stack")
        if index == -1:
            index = self.length - 1
        value = self.get(index)
        before = self.get_obj(index - 1)
        after = self.get_obj(index + 1)
        before.link = after
        self.length -= 1
        return value
