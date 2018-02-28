import socket
import struct

class CANsocket(object):
    FMT = '<IB3x8s'

    def __init__(self, interface):
        self.s = socket.socket(socket.PF_CAN, socket.SOCK_RAW, socket.CAN_RAW)
        self.s.bind((interface,))

    def receive(self):
        packet = self.s.recv(64)
        can_id, length, data = struct.unpack(self.FMT, packet)
        can_id &= socket.CAN_EFF_MASK
        return(can_id, data[:length])

    def send(self, can_id, data):
        can_id = can_id | socket.CAN_EFF_FLAG
        can_packet = struct.pack(self.FMT, can_id, len(data), data)
        self.s.send(can_packet)