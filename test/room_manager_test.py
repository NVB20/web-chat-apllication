import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from room_manager import generate_room_code, rooms, ROOM_CODE_LENGTH


class TestGenerateRoomCode(unittest.TestCase):
    def setUp(self):
        # Ensure rooms is empty before each test
        rooms.clear()

    def test_generate_room_code(self):
        room_code = generate_room_code(ROOM_CODE_LENGTH)
        self.assertEqual(len(room_code), ROOM_CODE_LENGTH)
        self.assertTrue(all(c.isalpha() and c.isupper() for c in room_code))
        
    def test_generate_unique_room_codes(self):
        num_tests = 1000
        generated_codes = set()
        
        for _ in range(num_tests):
            room_code = generate_room_code(ROOM_CODE_LENGTH)
            self.assertNotIn(room_code, generated_codes)
            generated_codes.add(room_code)
            
    def test_generate_room_code_with_existing_rooms(self):
        existing_room_code = "EXISTING"
        rooms[existing_room_code] = {}  # Simulate an existing room
        
        room_code = generate_room_code(ROOM_CODE_LENGTH)
        self.assertNotEqual(room_code, existing_room_code)

if __name__ == '__main__':
    unittest.main()
