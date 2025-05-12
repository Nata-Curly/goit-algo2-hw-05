import mmh3


class BloomFilter:
    def __init__(self, size, num_hashes):
        """
        Initializes a BloomFilter with the specified size and number of hash functions.

        :param size: The size of the bit array.
        :param num_hashes: The number of hash functions to use.
        :ivar size: The size of the bit array.
        :ivar num_hashes: The number of hash functions to use.
        :ivar bit_array: The bit array used to store the presence of elements.
        """

        self.size = size
        self.num_hashes = num_hashes
        self.bit_array = [0] * size

    def add(self, item):
        for i in range(self.num_hashes):
            index = mmh3.hash(item, i) % self.size
            self.bit_array[index] = 1

    def contains(self, item):
        for i in range(self.num_hashes):
            index = mmh3.hash(item, i) % self.size
            if self.bit_array[index] == 0:
                return False
        return True
