lis = []
class Channel:
    def __init__(self, name):
        self.name = name
        self.messages = []
    
    def add_message(self, m):
        self.messages.append(m)
    
    def print_info(self):
        print(f"Channel name: {self.name}")
        print()
        print("Messages:")
        for message in self.messages:
            print(message.sender, message.message)

class Message:
    def __init__(self, sender, message, date):
        self.sender = sender
        self.message = message
        self.date = date

    # def __repr__(self):
    #     return self.sender


def main():
    c1 = Channel(name="Chrome") 
    c2 = Channel(name="Carl") 
    m1 = Message("Bob", "Hello there!", "r")
    m2 = Message("Bob", "Hello there!", "r")
    m3 = Message("Bob", "Hello there!", "r")
    c1.add_message(m1)
    c1.add_message(m2)
    c1.add_message(m3)
    c1.print_info()
    lis.append(c1)
    lis.append(c2)
    c2.add_message(m1)
    
    for i in lis:
        print(i.messages)

if __name__ == "__main__":
    main()