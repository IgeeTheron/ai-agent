import unittest
import os
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from config import MAX_CHARS

class TestFunctions(unittest.TestCase):
    def setUp(self):
        self.working_directory = 'calculator'
        
        # This part ensures the lorem.txt file exists for testing
        self.lorem_path = os.path.join(self.working_directory, 'lorem.txt')
        if not os.path.exists(self.lorem_path):
            lorem_ipsum_text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. " * 300
            with open(self.lorem_path, "w") as f:
                f.write(lorem_ipsum_text)

    # --- Tests for get_files_info ---
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

    # --- New Tests for get_file_content ---
    def test_get_file_content_truncation(self):
        """Tests that a large file is read and truncated properly."""
        result = get_file_content(self.working_directory, 'lorem.txt')
        expected_suffix = f'[...File "lorem.txt" truncated at {MAX_CHARS} characters]'
        self.assertIsInstance(result, str)
        self.assertTrue(result.endswith(expected_suffix))
        self.assertEqual(len(result), MAX_CHARS + len(expected_suffix))

    def test_get_file_content_normal_file(self):
        """Tests reading a small, normal file."""
        file_path = 'main.py'
        with open(os.path.join(self.working_directory, file_path), 'r') as f:
            expected_content = f.read()
        result = get_file_content(self.working_directory, file_path)
        self.assertEqual(result, expected_content)
        
    def test_get_file_content_subdirectory_file(self):
        """Tests reading a normal file from a subdirectory."""
        file_path = 'pkg/calculator.py'
        with open(os.path.join(self.working_directory, file_path), 'r') as f:
            expected_content = f.read()
        result = get_file_content(self.working_directory, file_path)
        self.assertEqual(result, expected_content)

    def test_get_file_content_outside_boundary(self):
        """Tests an absolute path outside the working directory."""
        file_path = '/bin/cat'
        result = get_file_content(self.working_directory, file_path)
        expected_error = f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        self.assertEqual(result, expected_error)

    def test_get_file_content_non_existent_file(self):
        """Tests a path that points to a non-existent file."""
        file_path = 'pkg/does_not_exist.py'
        result = get_file_content(self.working_directory, file_path)
        expected_error = f'Error: File not found or is not a regular file: "{file_path}"'
        self.assertEqual(result, expected_error)

if __name__ == "__main__":
    unittest.main()