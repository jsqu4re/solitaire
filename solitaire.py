import sys
import numpy

## Helping Functions

def write_field(num_field: numpy.matrix, outfile):
    numpy.savetxt(outfile, num_field, fmt='%i', delimiter=" ")

def read_field(infile) -> numpy.matrix:
    return numpy.loadtxt(infile, dtype=numpy.int8, delimiter=" ")


## Classes

class Position:
    x = int(0)
    y = int(0)

    def __eq__(self, pos):
        return (self.x == pos.x and self.y == pos.y)

    def __str__(self):
        return "X: {}, Y: {}".format(self.x, self.y)


class Field:
    __field = numpy.matrix([[0, 0, 0],[0, 1, 0],[0, 0, 0]], dtype=numpy.int8)
    __target = numpy.matrix([[0, 0, 0],[0, 1, 0],[0, 0, 0]], dtype=numpy.int8)

    size = Position()
    
    def check_win(self) -> int:
        if (self.__field==self.__target).all():
            print ("win")
            return 1
        return 0

    def __check_move_on_field(self, old_position: Position, new_position: Position) -> int:
        # Move is on the board
        if(old_position.x >= 0 and old_position.y >= 0 and new_position.x >= 0 and new_position.y >= 0):
            if(old_position.x < self.size.x and old_position.y <  self.size.y and new_position.x < self.size.x and new_position.y < self.size.y):
                # Pegs are at the right places
                if(self.__field.item(old_position.x,old_position.y) == 1 and self.__field.item(new_position.x,new_position.y) == 0):
                        if(self.__field.item((old_position.x + new_position.x) / 2,(old_position.y + new_position.y) / 2) == 1):
                            return 1
        return 0

    def check_move(self, old_position: Position, new_position: Position) -> int:
        # Move is horizontal or vertical
        if (old_position.x == new_position.x or old_position.y == new_position.y):
            # Move is only over one peg
            if(abs(old_position.y - new_position.y) == 2 or abs(old_position.x - new_position.x) == 2):
                return self.__check_move_on_field(old_position, new_position)
        return 0

    def execute_move(self, old_position: Position, new_position: Position):
        self.__field[old_position.x,old_position.y] = 0
        self.__field[new_position.x,new_position.y] = 1
        self.__field[(old_position.x + new_position.x) // 2,(old_position.y + new_position.y) // 2] = 0

    def move(self, old_position: Position, new_position: Position) -> int:
        if(self.check_move(old_position,new_position)):
            self.execute_move(old_position,new_position)
            return 1
        return 0

    def get_size(self) -> Position:
        return self.__get_size(self.__field)

    def __get_size(self, field: numpy.matrix) -> Position:
        size = Position()
        size.x = field.shape[0]
        size.y = field.shape[1]
        return size
    
    def update_size(self):
        self.size = self.get_size()

    def check_integrity(self) -> int:
        size_field = self.__get_size(self.__field)
        size_target = self.__get_size(self.__target)

        if (size_target != size_field):
            return 0        
        return 1

    def set_target(self, num_field):
        self.__target = num_field
        self.update_size()

    def set_field(self, num_field):
        self.__field = num_field
        self.update_size()

    def get_field(self):
        return self.__field


    def get_target(self):
        return self.__target


## Test Area

def check_compare_win():
    field = Field()
    result = field.check_win()
    assert (result == 1)

def check_compare_lose():
    field = Field()
    field._Field__field = numpy.matrix([[0, 0, 0],[0, 0, 0],[0, 1, 0]], dtype=numpy.int8)
    result = field.check_win()
    assert (result == 0)


def check_integrity_win():
    field = Field()
    result = field.check_integrity()
    assert (result == 1)

def check_integrity_lose():
    field = Field()
    field._Field__field = numpy.matrix([[0, 0, 0],[0, 0, 0]], dtype=numpy.int8)
    result = field.check_integrity()
    assert (result == 0)

def check_write_and_read():
    field_write = Field()
    field_load = Field()
    field_load.set_field( numpy.matrix([[0, 0, 0],[0, 0, 0],[0, 0, 0]], dtype=numpy.int8))
    assert( (field_write.get_field() != field_load.get_field()).any() )
    write = field_write.get_field()
    write_field(write, "test.field")
    read = read_field("test.field")
    field_load.set_field(read)
    assert( (field_write.get_field() == field_load.get_field()).all() )

def selftest():
    check_compare_win()
    check_compare_lose()
    check_integrity_win()
    check_integrity_lose()
    check_write_and_read()



## Main

def main():
    print ("start")
    selftest()
    
    print ("done")


if __name__ == '__main__':
    sys.exit(main())