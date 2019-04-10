
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
    channels = {}
    c1 = Channel(name="Chrome") 
    c2 = Channel(name="Carl") 
    m1 = Message("Bob", "Hello there!", "r")
    m2 = Message("Bob", "Hello there!", "r")
    m3 = Message("Bob", "Hello there!", "r")
    c1.add_message(m1)
    c1.add_message(m2)
    c1.add_message(m3)
    c2.add_message(m1)
    channels[c1.name] = c1
    channels[c2.name] = c2
    print(channels)
    if c1.name in channels:
        print(True)

    a, b, c = 1, 2, 3
    print(a, b, c)  
    doc = {'c1': c1, 'c2':c2, 'c3': c1}
    channelList = []
    for i in doc:
        channelList.append(doc[i].name)
    print(channelList)
    print(channels[c1.name].messages[0].sender)
    for i in channels[c1.name].messages:
        print (i.message)
    
    print('d1' in doc)
if __name__ == "__main__":
    main()