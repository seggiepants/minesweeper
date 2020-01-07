import unittest
from game.cell import Cell, State
from game.grid import Grid, GameState

class CellTest(unittest.TestCase):
    def test_grid_can_be_created(self):   
        my_grid = Grid(10, 20)
        self.assertEqual(type(my_grid), Grid, 'Could not create variable of type Grid.')
    
    def test_grid_equal(self):
        my_grid = Grid(3, 3)
        # width
        self.assertNotEqual(my_grid, Grid(2, 3))
        # height
        self.assertNotEqual(my_grid, Grid(3, 2))
        
        # check game state.
        my_grid._state = GameState.WIN
        self.assertNotEqual(my_grid, Grid(3, 3))
        my_grid._state = GameState.PLAYING # back to normal

        # same size both default
        self.assertEqual(my_grid, Grid(3, 3))
        my_grid.get(0, 0).is_bomb = True
        # Not default state anymore
        self.assertNotEqual(my_grid, Grid(3, 3))
    
    def test_grid_clear(self):
        my_grid = Grid(3, 3)
        self.assertEqual(my_grid, Grid(3, 3))
        my_grid.get(0, 0).is_bomb = True
        my_grid.get(1, 1).state = State.FLAGGED
        my_grid.get(2, 2).state = State.OPEN
        # Not default anymore so not equal default.
        self.assertNotEqual(my_grid, Grid(3, 3))
        my_grid.clear()
        # reset should be equal again.
        self.assertEqual(my_grid, Grid(3, 3))
    
    def test_grid_keeps_parameters(self):   
        my_grid = Grid(10, 20)
        self.assertEqual(my_grid.width, 10, 'Grid did not save passed in width.')
        self.assertEqual(my_grid.height, 20, 'Grid did not save passed in height.')
    
    def test_grid_has_width_height_read_only(self):
        my_grid = Grid(10, 20)
        with self.assertRaises(AttributeError, msg='width should be read only.'):
            my_grid.width = 42
        
        with self.assertRaises(AttributeError, msg='height should be read only.'):
            my_grid.height = 42
    
    def test_grid_has_game_state_read_only(self):
        my_grid = Grid(3, 3)
        with self.assertRaises(AttributeError, msg='state should be read only'):
            my_grid.state = GameState.WIN
    
    def test_access_grid_out_of_bounds(self):
        my_grid = Grid(10, 20)

        with self.assertRaises(ValueError, msg='Should not be able to access grid outside of bounds.'):
            # Row too small
            _ = my_grid.get(0, -1)
        
        with self.assertRaises(ValueError, msg='Should not be able to access grid outside of bounds.'):
            # Row too big - 1
            _ = my_grid.get(0, 20)
        
        with self.assertRaises(ValueError, msg='Should not be able to access grid outside of bounds.'):
            # Row too big - 2
            _ = my_grid.get(0, 21)
        
        with self.assertRaises(ValueError, msg='Should not be able to access grid outside of bounds.'):
            # Column too small
            _ = my_grid.get(-1, 0)
        
        with self.assertRaises(ValueError, msg='Should not be able to access grid outside of bounds.'):
            # Column too big - 1
            _ = my_grid.get(10, 0)
        
        with self.assertRaises(ValueError, msg='Should not be able to access grid outside of bounds.'):
            # Column too big - 2
            _ = my_grid.get(11, 0)

    def test_access_grid_in_bounds(self):
        my_grid = Grid(10, 20)

        self.assertEqual(my_grid.get(0, 0).state, State.DEFAULT, "Cannot access grid at 0, 0")
        self.assertEqual(my_grid.get(9, 0).state, State.DEFAULT, "Cannot access grid at 9, 0")
        self.assertEqual(my_grid.get(0, 19).state, State.DEFAULT, "Cannot access grid at 0, 19")
        self.assertEqual(my_grid.get(9, 19).state, State.DEFAULT, "Cannot access grid at 9, 19")
        self.assertEqual(my_grid.get(4, 9).state, State.DEFAULT, "Cannot access grid at 4, 9")
    
    def test_bomb_count(self):
        my_grid = Grid(3, 3)
        my_grid.get(0, 0).is_bomb = True
        # make sure we see a bomb in the top left corner
        self.assertEqual(my_grid.get_bomb_count(1, 1), 1, "Incorrect Bomb Count.")
        # only bomb skipped if that is the cell we are testing.
        self.assertEqual(my_grid.get_bomb_count(0, 0), 0, "Incorrect Bomb Count.")
        # make sure we see a bomb in the top right corner
        my_grid.get(2, 0).is_bomb = True
        self.assertEqual(my_grid.get_bomb_count(1, 1), 2, "Incorrect Bomb Count.")
        # make sure we see a bomb in the bottom_left  corner
        my_grid.get(0, 2).is_bomb = True
        self.assertEqual(my_grid.get_bomb_count(1, 1), 3, "Incorrect Bomb Count.")
        # make sure we see a bomb in the bottom right corner
        my_grid.get(2, 2).is_bomb = True
        self.assertEqual(my_grid.get_bomb_count(1, 1), 4, "Incorrect Bomb Count.")
        # test the rest of the edges
        # make sure we see a bomb in the top right corner
        my_grid.get(1, 0).is_bomb = True
        my_grid.get(0, 1).is_bomb = True
        my_grid.get(2, 1).is_bomb = True
        my_grid.get(1, 2).is_bomb = True
        self.assertEqual(my_grid.get_bomb_count(1, 1), 8, "Incorrect Bomb Count.")
        # go off the edge on the bottom right
        my_grid.get(1, 1).is_bomb = True
        self.assertEqual(my_grid.get_bomb_count(2, 2), 3, "Incorrect Bomb Count.")

    def test_toggle_flagged(self):
        my_grid = Grid(3, 3)

        # should not change if state != playing
        my_grid._state = GameState.LOSE
        my_grid.toggle_flagged(0, 0)
        self.assertEqual(my_grid.get(0, 0).state, State.DEFAULT)

        # should change if playing
        my_grid._state = GameState.PLAYING
        my_grid.toggle_flagged(0, 0)
        self.assertEqual(my_grid.get(0, 0).state, State.FLAGGED)
        my_grid.toggle_flagged(0, 0)
        self.assertEqual(my_grid.get(0, 0).state, State.DEFAULT)

        # Didn't mix up row and column did we?
        my_grid._state = GameState.PLAYING
        my_grid.toggle_flagged(1, 0)
        self.assertEqual(my_grid.get(1, 0).state, State.FLAGGED)
        my_grid.toggle_flagged(1, 0)
        self.assertEqual(my_grid.get(1, 0).state, State.DEFAULT)


        # should not change if open.
        my_grid.get(0, 0).state = State.OPEN
        my_grid.toggle_flagged(0, 0)
        self.assertEqual(my_grid.get(0, 0).state, State.OPEN)

        # should throw an error if out of bounds.
        with self.assertRaises(ValueError, msg='Should not be able to access grid outside of bounds.'):
            my_grid.toggle_flagged(-1, 0)
            my_grid.toggle_flagged(0, -1)
            my_grid.toggle_flagged(3, 0)
            my_grid.toggle_flagged(0, 3)
            my_grid.toggle_flagged(3, 3)

    def test_get_count_bombs(self):
        my_grid = Grid(3, 3)
        self.assertEqual(my_grid.get_count_bombs(), 0)
        my_grid.get(0, 0).is_bomb = True
        self.assertEqual(my_grid.get_count_bombs(), 1)
        my_grid.get(2, 2).is_bomb = True
        self.assertEqual(my_grid.get_count_bombs(), 2)
        for j in range(3):
            for i in range(3):
                my_grid.get(i, j).is_bomb = True
        self.assertEqual(my_grid.get_count_bombs(), 9)
        my_grid.get(1, 1).is_bomb = False
        self.assertEqual(my_grid.get_count_bombs(), 8)

    def test_get_count_remaining_to_open(self):
        my_grid = Grid(3, 3)
        self.assertEqual(my_grid.get_count_remaining_to_open(), 9)
        my_grid.get(1, 1).is_bomb = True
        self.assertEqual(my_grid.get_count_remaining_to_open(), 8)
        my_grid.get(2, 2).state = State.OPEN
        self.assertEqual(my_grid.get_count_remaining_to_open(), 7)
        for j in range(3):
            for i in range(3):
                my_grid.get(i, j).state = State.OPEN
        self.assertEqual(my_grid.get_count_remaining_to_open(), 0)

    def test_seed_grid(self):
        my_grid = Grid(10, 20)
        my_grid.seed_grid(10)
        self.assertEqual(my_grid.get_count_bombs(), 10)

        with self.assertRaises(TypeError, msg='Num_Bombs needs to be an integer.'):
            my_grid.seed_grid(1.1)
            my_grid.seed_grid(True)
            my_grid.seed_grid('stuff')
            my_grid.seed_grid([1, 2, 3])
        
        with self.assertRaises(ValueError, msg='Too many bombs.'):
            my_grid.seed_grid(300)

        with self.assertRaises(ValueError, msg='Too many bombs.'):
            my_grid.seed_grid(200)
        
        my_grid.seed_grid(199)
        self.assertEqual(my_grid.get_count_bombs(), 199)

        my_grid.seed_grid(0)
        self.assertEqual(my_grid.get_count_bombs(), 0)
    
    def string_to_grid(self, data):
        """Return a grid that matches the state given by
        the list of strings in data.
        ' ' => Unopened grid square not a bomb
        'x' => Unopend grid square that is a bomb
        '/' => Flagged grid square not a bomb
        '*' => Flagged grid square that is a bomb
        '_' => Opened grid square that is not a bomb
        'X' => Opened grid square that is a bomb
        """
        height = len(data)
        width = len(data[0])
        my_grid = Grid(width, height)
        for j in range(height):
            for i in range(width):
                ch = data[j][i]
                if ch == ' ':
                    my_grid.get(i, j).is_bomb = False
                    my_grid.get(i, j).state = State.DEFAULT
                elif ch == 'x':
                    my_grid.get(i, j).is_bomb = True
                    my_grid.get(i, j).state = State.DEFAULT
                elif ch == '/':
                    my_grid.get(i, j).is_bomb = False
                    my_grid.get(i, j).state = State.FLAGGED
                elif ch == '*':
                    my_grid.get(i, j).is_bomb = True
                    my_grid.get(i, j).state = State.FLAGGED
                elif ch == '_':
                    my_grid.get(i, j).is_bomb = False
                    my_grid.get(i, j).state = State.OPEN
                elif ch == 'X':
                    my_grid.get(i, j).is_bomb = True
                    my_grid.get(i, j).state = State.OPEN

        return my_grid

        
    def grid_to_string(self, grid):
        """Return a grid that matches the state given by
        the list of strings in data.
        ' ' => Unopened grid square not a bomb        
        'x' => Unopend grid square that is a bomb
        '/' => Flagged grid square not a bomb
        '*' => Flagged grid square that is a bomb
        '_' => Opened grid square that is not a bomb and does not have neighboring bombs.
        '1' to '8' => Opened grid square that has neighboring bombs
        'X' => Opened grid square that is a bomb
        """
        results = []
        for j in range(grid.height):
            row = ''
            for i in range(grid.width):
                is_bomb = grid.get(i, j).is_bomb
                state = grid.get(i, j).state
                neighbor_bombs = grid.get_bomb_count(i, j)

                if is_bomb == False and state == State.DEFAULT:
                    ch = ' '
                elif is_bomb == True and state == State.DEFAULT:
                    ch = 'x'
                elif is_bomb == False and state == State.FLAGGED:
                    ch = '/'
                elif is_bomb == True and state == State.FLAGGED:
                    ch = '*'
                elif is_bomb == False and state == State.OPEN:
                    if neighbor_bombs == 0:
                        ch = '_'
                    else:
                        ch = str(neighbor_bombs)
                elif is_bomb == True and state == State.OPEN:
                    ch = 'X'

                row = row + ch
            results.append(row)
        return results

    def test_open(self):
        my_grid = Grid(3, 3)

        # Don't open if the game isn't playing
        my_grid._state = GameState.WIN
        my_grid.open(0, 0)
        expected = ['   ', '   ', '   ']
        self.assertEqual(expected, self.grid_to_string(my_grid))
        my_grid._state = GameState.PLAYING

        # Empty grid will expose everything on click.
        my_grid.open(1, 1)
        expected = ['___', '___', '___']
        self.assertEqual(expected, self.grid_to_string(my_grid))

        # Empty grid with a bomb in the middle.
        my_grid.clear()        
        expected = ['   ', ' X ', '   ']
        my_grid.get(1, 1).is_bomb = True
        my_grid.open(1, 1)
        self.assertEqual(expected, self.grid_to_string(my_grid))

        # New game with two bombs nothing opened
        my_grid.clear()        
        expected = ['  x', '   ', 'x  ']
        my_grid.get(2, 0).is_bomb = True
        my_grid.get(0, 2).is_bomb = True
        self.assertEqual(expected, self.grid_to_string(my_grid))

        # Same grid open at 1, 0
        my_grid.open(1, 0)
        expected = [' 1x', '   ', 'x  ']
        self.assertEqual(expected, self.grid_to_string(my_grid))

        # Same grid open at 1, 0
        my_grid.open(0, 0)
        expected = ['_1x', '1  ', 'x  ']
        self.assertEqual(expected, self.grid_to_string(my_grid))

        my_grid = Grid(4, 4)
        my_grid.get(0, 1).is_bomb = True
        my_grid.get(1, 3).is_bomb = True
        my_grid.open(2, 1)
        expected = [' 1__', 'x1__', '  1_', ' x1_']
        self.assertEqual(expected, self.grid_to_string(my_grid))

        my_grid = Grid(3, 4)
        my_grid.get(1, 1).is_bomb = True
        my_grid.get(2, 2).is_bomb = True
        my_grid.open(0, 3)
        expected = ['   ', ' x ', '1 x', '_1 ']
        self.assertEqual(expected, self.grid_to_string(my_grid))

        


        
if __name__ == '__main__':
    unittest.main()
