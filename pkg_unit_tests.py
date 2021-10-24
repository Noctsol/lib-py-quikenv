"""
Owner: Noctsol
Contributors: N/A
Date Created: 2021-10-18

Summary:
    Unit tests for this package.

"""



# Local import
from src import quikenv

# Pre-installed
import unittest
import os



class PkgTest(unittest.TestCase):
    """ Unit tests """
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName=methodName)
        self.file_dir = os.path.abspath(__file__)
        self.root_dir = os.path.dirname(self.file_dir)
        self.env_file_path = os.path.join(self.root_dir, ".env")
        self.empty_env_path = os.path.join(self.root_dir, "ref/empty.env")
        self.key = "yoursecret1"

    def test_load_empty(self):
        """Checks that load() function fails with empty string"""
        env = quikenv.Quikenv("")
        with self.assertRaises(ValueError):
            env.load()

    def test_load_none(self):
        """Checks that load() function fails with NONE"""
        env = quikenv.Quikenv(None)
        with self.assertRaises(ValueError):
            env.load()

    def test_lazyload(self):
        """Checks that the lazy_load() function finds the .env file"""
        env = quikenv.ezload()
        self.assertTrue(isinstance(env.get(self.key), str))

    def test_lazyload_nofile(self):
        """Checks that the lazy_load() function errors out when no .env file is found"""
        os.chdir("../")
        with self.assertRaises(quikenv.EnvFileNotExist):
            quikenv.ezload()

    def test_proper_load(self):
        """Check that the peroper_load() function finds the env file and can get a env var"""
        env = quikenv.Quikenv.proper_load(self.env_file_path)
        self.assertTrue(isinstance(env.get(self.key), str))

    def test_get(self):
        """Checks that we successfully retrieve a environment variable"""
        env = quikenv.Quikenv(self.env_file_path)
        env.load()
        self.assertTrue(isinstance(env.get(self.key), str))

    def test_get_nonexistent(self):
        """Checks that error is returned if no variable does not exist"""
        env = quikenv.proper_load(self.empty_env_path)
        with self.assertRaises(quikenv.EnvVarNotExistError):
            env.get("nonexistent")

    def test_get_empty(self):
        """Checks that error is returned if we get an empty value for a variable"""
        env = quikenv.proper_load(self.env_file_path)
        with self.assertRaises(quikenv.EnvVarEmptyError):
            env.get("theempty")


if __name__ == '__main__':
    unittest.main()
