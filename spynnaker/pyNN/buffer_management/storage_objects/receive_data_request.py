

class ReceiveDataRequest(object):
    
    def __init__(self, chip_x, chip_y, chip_p, address_pointer, size):
        self._chip_x = chip_x
        self._chip_y = chip_y
        self._chip_p = chip_p
        self._address_pointer = address_pointer
        self._size = size
        
    @property
    def chip_x(self):
        return self._chip_x
    
    @property
    def chip_y(self):
        return self._chip_y
    
    @property
    def chip_p(self):
        return self._chip_p
    
    @property
    def address_pointer(self):
        return self._address_pointer
    
    @property
    def size(self):
        return self._size