class TSPacket(object):
    def __init__(self, source=0, timestamp=0.0):
        self.source = source
        self.timestamp = timestamp

    @property
    def source(self):
        return self._source

    @source.setter
    def source(self, source):
        if source not in range(0,256):
            raise ValueError("Source ID must be integer between 0 and 255 (got: {})".format(source))
        self._source = source

    @property
    def timestamp(self):
        return self._timestamp

    @timestamp.setter
    def timestamp(self, timestamp):
        if not isinstance(timestamp, float):
            raise TypeError("Timestamp must be float (got: {})".format(type(timestamp)))
        self._timestamp = timestamp


class PublicationFrame(TSPacket):
    def __init__(self, dataobjectID=0, priority=6):
        super().__init__()
        self.dataobjectID = dataobjectID
        self._messageType = True
        self.priority = priority

    @property
    def messageType(self):
        return "Publication message"

    @property
    def dataobjectID(self):
        return self._dataobjectID

    @dataobjectID.setter
    def dataobjectID(self, dataobjectID):
        if not dataobjectID in range(0,65537):
            raise ValueError("Data object ID must be integer between 0 and 65536 (got: {}).".format(dataobjectID))
        self._dataobjectID = dataobjectID


class Single(PublicationFrame):
    SINGLE_FRAME_MASK = int.from_bytes(b'\x00\x00\x00\x00\x00\x00\x00\x80', 'little')
    SINGLE_ID_MASK = int.from_bytes(b'\x00\x00\x00\x03','little')

    def __init__(self, data=None, dataobjectID=0, priority=6, source=0, timestamp=0.0):
        super().__init__()
        self.data = data
        self.dataobjectID = dataobjectID
        self.priority = priority
        self.source = source
        self.timestamp = timestamp

    @property
    def identifier(self):
        id_prio = self._priority << 26
        id_doid = self._dataobjectID << 8
        id_raw = id_prio | self.SINGLE_ID_MASK | id_doid | self.source 
        return id_raw.to_bytes(4, 'big')

    @property
    def data(self):
        return self._data

    @property
    def priority(self):
        return self._priority

    @priority.setter
    def priority(self, priority):
        if priority not in [4,5,6]:
            raise ValueError("Priority must be 4, 5 or 6 for publication frame (got: {}).".format(priority))
        self._priority = priority

    @data.setter
    def data(self, data):
        if data is None:
            self._data = bytes()
        elif not isinstance(data, bytes):
            raise TypeError("Wrong data type. Must be bytes, not {}".format(type(data)))
        bits = int.from_bytes(data, byteorder='little')
        if (bits & self.SINGLE_FRAME_MASK) or (len(data) > 8):
            raise ValueError("Data too big for single frame. Msg can contain up to 63 Bits")
        self._data = data
