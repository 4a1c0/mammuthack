
# Create your dictionary class 
class Games(dict): 
    # __init__ function 
    def __init__(self): 
        self = dict() 
          
    # Function to add key:value 
    def addChannel(self, channel): 
        self[channel] = []

    def addUser(self, channel, user):
        self[channel].append(user)

