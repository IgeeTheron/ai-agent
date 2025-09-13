import unittest
from functions.get_files_info import get_files_info

class TestFunctions(unittest.TestCase):
    def setUp(self):
        self.working_directory = 'calculator'

    def test_list_current_directory(self):
        result = get_files_info(self.working_directory, ".")
        self.assertIsInstance(result, str)
        self.assertIn('- main.py: file_size=', result)
        self.assertIn('is_dir=False', result)
        self.assertIn('- tests.py: file_size=', result)
        self.assertIn('is_dir=False', result)
        self.assertIn('- pkg: file_size=', result)
        self.assertIn('is_dir=True', result)

    def test_list_subdirectory(self):
        result = get_files_info(self.working_directory, "pkg")
        self.assertIsInstance(result, str)
        self.assertIn('- calculator.py: file_size=', result)
        self.assertIn('is_dir=False', result)
        self.assertIn('- render.py: file_size=', result)
        self.assertIn('is_dir=False', result)

    def test_absolute_path_outside_boundary(self):
        result = get_files_info(self.working_directory, "/bin")
        expected_error = 'Error: Cannot list "/bin" as it is outside the permitted working directory'
        self.assertEqual(result, expected_error)

    def test_relative_path_outside_boundary(self):
        result = get_files_info(self.working_directory, "../")
        expected_error = 'Error: Cannot list "../" as it is outside the permitted working directory'
        self.assertEqual(result, expected_error)

    def test_path_is_not_a_directory(self):
        result = get_files_info(self.working_directory, "main.py")
        expected_error = 'Error: "main.py" is not a directory'
        self.assertEqual(result, expected_error)
        
    def test_non_existent_directory(self):
        result = get_files_info(self.working_directory, "non_existent_folder")
        expected_error = 'Error: The directory "non_existent_folder" was not found.'
        self.assertEqual(result, expected_error)

if __name__ == "__main__":
    unittest.main()