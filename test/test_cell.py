import unittest
from game.cell import Cell, State

class CellTest(unittest.TestCase):
    def test_cell_can_be_created(self):   
        my_cell = Cell()
        self.assertEqual(type(my_cell), Cell, 'Could not create variable of type Cell.')
    
    def test_cell_clear(self):
        my_cell = Cell()
        my_cell.is_bomb = True
        my_cell.state = State.FLAGGED
        # Before clear should not be equivalen to a new cell.
        self.assertNotEqual(my_cell, Cell())
        my_cell.clear()
        # After clear should be equivalent to a new cell.
        self.assertEqual(my_cell, Cell())

    def test_cell_default_values(self):
        my_cell = Cell()
        self.assertEqual(my_cell.state, State.DEFAULT, "Cell should have State.Default for default state.")
        self.assertEqual(my_cell.is_bomb, False, "Cell should have is_bomb set to False by default.")
    
    def test_cell_constructor_parameters(self):
        my_cell_default = Cell(True, State.DEFAULT)
        my_cell_flagged = Cell(False, State.FLAGGED)
        my_cell_open = Cell(True, State.OPEN)

        self.assertEqual(my_cell_default.state, State.DEFAULT, "Cell should have state of State.DEFAULT.")
        self.assertEqual(my_cell_flagged.state, State.FLAGGED, "Cell should have state of State.FLAGGED.")
        self.assertEqual(my_cell_open.state, State.OPEN, "Cell should have state of State.OPEN.")

        self.assertEqual(my_cell_default.is_bomb, True, "Cell did not keep value set for is_bomb.")
        self.assertEqual(my_cell_flagged.is_bomb, False, "Cell did not keep value set for is_bomb.")

    def test_cell_toggle_flag(self):
        my_cell = Cell()
        # should not change.
        my_cell.state = State.OPEN 
        my_cell.toggle_flag()
        self.assertEqual(my_cell.state, State.OPEN)
        # should change to default.
        my_cell.state = State.FLAGGED
        my_cell.toggle_flag()
        self.assertEqual(my_cell.state, State.DEFAULT)
        # should change to flagged.
        my_cell.state = State.DEFAULT
        my_cell.toggle_flag()
        self.assertEqual(my_cell.state, State.FLAGGED)


if __name__ == '__main__':
    unittest.main()
