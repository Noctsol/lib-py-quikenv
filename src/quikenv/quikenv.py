"""
Owner: Noctsol
Contributors: N/A
Date Created: 2021-10-24

Summary:
    Wrapper class around python-dotenv. I didn't like alot of things....
    - It loaded on all your custom variables from your file ON TOP OF the global environment variables on your operating system.
    - It felt very hacky having all these unnessary environment variable unrelated to your project
    - Getting environment variable required the use of dotenv and os.getenv(). Why not just put this functionality into one class?
        - There should have been a Get() function like in here

    - As a project, the project was easy to use, made sense, and was well-documented. I'm just lazy.

"""



# Pre-installed packages
from pathlib import Path
import os

# From PYPI
from dotenv import dotenv_values



class Quikenv():
    '''Wrapper class around python-dotenv. I didn't like alot of things....
    - It loaded on all your custom variables from your file ON TOP OF the global environment variables on your operating system.
    - It felt very hacky having all these unnessary environment variable unrelated to your project
    - Getting environment variable required the use of dotenv and os.getenv(). Why not just put this functionality into one class?
        - There should have been a Get() function like in here

    - As a project, the project was easy to use and made sense and was well-documented
    '''

    def __init__(self, env_file_path):
        self.env_file_path = env_file_path
        self.environment_variables = None


    ###################################### CLASS METHODS ######################################

    # Takes a given file path and return a Quikenv object loaded up already
    @classmethod
    def proper_load(cls, env_file_path):
        """Takes a given file path and return a Quikenv object loaded up already

        Args:
            env_file_path (string): file path of env file
        """
        quickenv_obj = cls(env_file_path)
        quickenv_obj.load()
        return quickenv_obj

    # Will automatically look for .env file to an extent and use first one found
    @classmethod
    def lazy_load(cls):
        """Will automatically look for .env file to an extent and use first one found.
        This function will look in the current directory and up to 2 directories up.
        It will throw an exception if no .env file is found
        """

        current_dir = os.getcwd()
        paths_searched = [current_dir]
        env_file_name = None

        # Looking for an env file
        for _ in range(2):
            # Get files in dir
            dir_lst = os.listdir(current_dir)

            # Check if .env in file
            for file in dir_lst:
                if ".env" in file:
                    env_file_name = file
                    break

            # End loop if file found or check new dir
            if env_file_name is not None:
                break
            else:
                current_dir = str(Path(current_dir).parent.absolute())
                paths_searched.append(current_dir)

        if env_file_name is None:
            raise EnvFileNotExist(paths_searched)

        # Load up quick env using file found
        env_file_path = os.path.join(current_dir, env_file_name)
        quikenv_obj = cls(env_file_path)
        quikenv_obj.load()

        return quikenv_obj


    ###################################### FUNCTIONS ######################################

    # Loads up environment variables
    def load(self):
        '''Loads up environment variables'''

        # Check that string is not empty
        if not self.env_file_path:
            raise ValueError("self.env_file_path cannot be empty or null")
        # Checks if path is valid
        elif not os.path.exists(self.env_file_path):
            raise EnvFileNotExist([self.env_file_path])

        # Loading up default environment variables from current environment
        self.environment_variables = dotenv_values(self.env_file_path)

        return True

    # Fetches a value from environment environment variables - set to error out if key does not exist
    def get(self, env_key_str):
        '''Loads up environment variables'''

        # Throw exception if you forget to set the environment - I don't want to make this automatic - should be explicit
        if self.environment_variables is None:
            raise EnvVarNotSet()

        # Tries to get value - throws error if it doesn't exist
        try:
            value = self.environment_variables[env_key_str]
        except KeyError as error:
            raise EnvVarNotExistError(env_key_str) from error

        # Check if value is null or empty
        if not value:
            raise EnvVarEmptyError(env_key_str)

        return value

############################ FUNCTIONS ############################

def lazy_load():
    return Quikenv.lazy_load()

def proper_load(file_path):
    return Quikenv.proper_load(file_path)

############################ EXCEPTIONS ############################
class EnvVarNotSet(Exception):
    '''Exception for when we didn't load'''

    def __init__(self):
        self.message = "Environment not set - please call Environment.load_env()"
        super().__init__(self.message)

class EnvVarNotExistError(Exception):
    '''Exception for when we call a nonexistent item'''

    def __init__(self, env_key):
        self.message = f"Environment variable key '{env_key}' not found"
        super().__init__(self.message)

class EnvVarEmptyError(Exception):
    '''Exception for when a environment var is empty or null'''

    def __init__(self, env_key):
        self.message = f"Environment variable key '{env_key}' has an empty or null value"
        super().__init__(self.message)

class EnvFileNotExist(Exception):
    '''Exception for when .env file is not found'''

    def __init__(self, path_list):
        paths_string = ", ".join(path_list)
        self.message = f"Create an env file please. Unable to find .env file in any of the following paths: {paths_string}"
        super().__init__(self.message)
