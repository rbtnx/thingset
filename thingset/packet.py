

class TSPacket(object):
    def __init__(self, priority=7, message_type=None, source=0, timestamp=0.0):
        self.priority = priority
        self.message_type = message_type
        self.source = source
        self.timestamp = timestamp

class PublicationFrame(TSPacket):
    def __init__(self, dataobjectId=0):
        self.dataobjectId = dataobjectId
        
class Single(PublicationFrame):
    def __init__(self, data=None):

        if data is None:
            self.data = bytearray()
        elif isinstance(data, bytearray):
            self.data = data
        else:
            try:
                self.data = bytearray(data)
            except TypeError:
                err = "Couldn't create message from {} ({})".format(data, type(data))
                raise TypeError(err)
