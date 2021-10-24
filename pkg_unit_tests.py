"""
Owner: Noctsol
Contributors: N/A
Date Created: 2021-10-18

Summary:
    Unit tests for this package.

"""



# Local import
from src.quikenv import main as qui

# Pre-installed
import unittest
import os



class PkgTest(unittest.TestCase):
    """ Unit tests """
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName=methodName)
        self.env_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), ".env")
        self.empty_env_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "ref/empty.env")
        self.key = "yoursecret1"

    def test_load_empty(self):
        """Checks that load() function fails with empty string"""
        env = qui.Quikenv("")
        with self.assertRaises(ValueError):
            env.load()

    def test_load_none(self):
        """Checks that load() function fails with NONE"""
        env = qui.Quikenv(None)
        with self.assertRaises(ValueError):
            env.load()

    def test_lazyload(self):
        """Checks that the lazy_load() function finds the .env file"""
        env = qui.Quikenv.lazy_load()
        self.assertTrue(isinstance(env.get(self.key), str))

    def test_lazyload_nofile(self):
        """Checks that the lazy_load() function errors out when no .env file is found"""
        os.chdir("../")
        with self.assertRaises(qui.EnvFileNotExist):
            qui.Quikenv.lazy_load()

    def test_proper_load(self):
        """Check that the peroper_load() function finds the env file and can get a env var"""
        env = qui.Quikenv.proper_load(self.env_file_path)
        self.assertTrue(isinstance(env.get(self.key), str))

    def test_get(self):
        """Checks that we successfully retrieve a environment variable"""
        env = qui.Quikenv(self.env_file_path)
        env.load()
        self.assertTrue(isinstance(env.get(self.key), str))

    def test_get_nonexistent(self):
        """Checks that error is returned if no variable does not exist"""
        env = qui.Quikenv.proper_load(self.empty_env_path)
        with self.assertRaises(qui.EnvVarNotExistError):
            env.get("nonexistent")

    def test_get_empty(self):
        """Checks that error is returned if we get an empty value for a variable"""
        env = qui.Quikenv.proper_load(self.env_file_path)
        with self.assertRaises(qui.EnvVarEmptyError):
            env.get("theempty")


if __name__ == '__main__':
    unittest.main()
