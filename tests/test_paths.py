import unittest
import platform
from platform_utils import paths


class TestModulePath(unittest.TestCase):

    def test_module_path(self):
        self.assertTrue(paths.module_path().endswith('tests'))


class TestCrossPlatformPaths(unittest.TestCase):
    
    def test_app_data_path(self):
        """Test that app_data_path returns a valid path"""
        result = paths.app_data_path("test_app")
        self.assertIsInstance(result, str)
        self.assertIn("test_app", result)
    
    def test_documents_path(self):
        """Test that documents_path returns a valid path"""
        result = paths.documents_path()
        self.assertIsInstance(result, str)
        self.assertTrue(len(result) > 0)
    
    def test_get_applications_path(self):
        """Test that get_applications_path works cross-platform"""
        result = paths.get_applications_path()
        if platform.system() == "Windows":
            # On Windows, should return Program Files path
            self.assertIsInstance(result, str)
            self.assertIn("Program Files", result)
        else:
            # On non-Windows, should return None
            self.assertIsNone(result)
