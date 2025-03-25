class Node:
    def __init__(self, data):
        self.data = data  
        self.next = None
        self.prev = None

class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.current = None  

    def add(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = self.tail = self.current = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node

    def delete(self, data):
        current = self.head
        while current:
            if current.data == data:
                if current.prev:
                    current.prev.next = current.next
                else:
                    self.head = current.next
                if current.next:
                    current.next.prev = current.prev
                else:
                    self.tail = current.prev
                if self.current == current:
                    self.current = current.next if current.next else current.prev
                return True
            current = current.next
        return False
    
    def previous(self):
        if self.current and self.current.prev:
            self.current = self.current.prev
            return self.current.data
        return None

    def next(self):
        if self.current and self.current.next:
            self.current = self.current.next
            return self.current.data
        return None

    def get_list(self):
        songs = []
        current = self.head
        while current:
            songs.append(current.data)
            current = current.next
        return songs
