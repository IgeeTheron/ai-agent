import unittest
import os
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file
from config import MAX_CHARS

class TestFunctions(unittest.TestCase):
    def setUp(self):
        self.working_directory = 'calculator'
        
        # Ensure lorem.txt exists for testing
        lorem_path = os.path.join(self.working_directory, 'lorem.txt')
        if not os.path.exists(lorem_path):
            lorem_ipsum_text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. " * 300
            with open(lorem_path, "w") as f:
                f.write(lorem_ipsum_text)

    def tearDown(self):
        # Clean up files created during testing
        morelorem_path = os.path.join(self.working_directory, 'pkg/morelorem.txt')
        if os.path.exists(morelorem_path):
            os.remove(morelorem_path)
        
        # Clean up directories created during testing
        pkg_dir = os.path.join(self.working_directory, 'pkg')
        if os.path.exists(pkg_dir) and len(os.listdir(pkg_dir)) == 0:
            os.rmdir(pkg_dir)

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

    def test_get_file_content_normal_file(self):
        file_path = 'main.py'
        with open(os.path.join(self.working_directory, file_path), 'r') as f:
            expected_content = f.read()
        result = get_file_content(self.working_directory, file_path)
        self.assertEqual(result, expected_content)
        
    def test_get_file_content_subdirectory_file(self):
        file_path = 'pkg/calculator.py'
        with open(os.path.join(self.working_directory, file_path), 'r') as f:
            expected_content = f.read()
        result = get_file_content(self.working_directory, file_path)
        self.assertEqual(result, expected_content)

    def test_get_file_content_outside_boundary(self):
        file_path = '/bin/cat'
        result = get_file_content(self.working_directory, file_path)
        expected_error = f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        self.assertEqual(result, expected_error)

    def test_get_file_content_non_existent_file(self):
        file_path = 'pkg/does_not_exist.py'
        result = get_file_content(self.working_directory, file_path)
        expected_error = f'Error: File not found or is not a regular file: "{file_path}"'
        self.assertEqual(result, expected_error)

    def test_write_to_existing_file(self):
        file_path = 'lorem.txt'
        content = "wait, this isn't lorem ipsum"
        result = write_file(self.working_directory, file_path, content)
        expected = f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        self.assertEqual(result, expected)
        # Verify the content was actually written
        with open(os.path.join(self.working_directory, file_path), 'r') as f:
            self.assertEqual(f.read(), content)

    def test_write_to_new_file_in_subdir(self):
        file_path = 'pkg/morelorem.txt'
        content = "lorem ipsum dolor sit amet"
        result = write_file(self.working_directory, file_path, content)
        expected = f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        self.assertEqual(result, expected)
        # Verify the content was written
        with open(os.path.join(self.working_directory, file_path), 'r') as f:
            self.assertEqual(f.read(), content)

    def test_write_outside_boundary(self):
        file_path = '/tmp/temp.txt'
        content = "this should not be allowed"
        result = write_file(self.working_directory, file_path, content)
        expected = f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        self.assertEqual(result, expected)

    def test_run_python_file_main_usage(self):
        result = run_python_file(self.working_directory, "main.py")
        self.assertIn("STDOUT:", result)
        self.assertIn('Usage: python main.py "<expression>"', result)
        
    def test_run_python_file_with_args(self):
        result = run_python_file(self.working_directory, "main.py", ["3 + 5"])
        self.assertIn("STDOUT:", result)
        self.assertIn('"result": 8', result)
        
    def test_run_python_file_tests(self):
        result = run_python_file(self.working_directory, "tests.py")
        self.assertIn("STDERR:", result)
        self.assertIn("Ran", result)
        self.assertIn("OK", result)

    def test_run_python_file_outside_boundary(self):
        result = run_python_file(self.working_directory, "../main.py")
        expected_error = 'Error: Cannot execute "../main.py" as it is outside the permitted working directory'
        self.assertEqual(result, expected_error)
        
    def test_run_python_file_nonexistent_file(self):
        result = run_python_file(self.working_directory, "nonexistent.py")
        expected_error = 'Error: File "nonexistent.py" not found.'
        self.assertEqual(result, expected_error)

if __name__ == "__main__":
    unittest.main()
