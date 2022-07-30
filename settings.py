import json
import os


class Settings:

    def __init__(self, dpbg_config=dict) -> None:
        self.settings_path = dpbg_config['SETTINGS_PATH']
        self.settings_def_dict = dpbg_config['SETTINGS_DEF_DICT']
        self.def_settings = self.missing_settings_check()

    def write_val_to_settings(self, key, val):
        """
        Write the value to the settings.json file.
        """
        data = self.read()
        data[key] = val
        self.write(data)
        return

    def read_val(self, key):
        """
        Read the value from the settings.json file.
        """
        data = self.read()
        return data[key]

    def remove_key(self, key):
        """
        Remove the key from the settings.json file.
        """
        data = self.read()
        del data[key]
        self.write(data)
        return

    def missing_settings_check(self) -> bool:
        """
        Check if the settings.json file is missing.
        If it is, create a new one with the default values.
        """
        if not os.path.isfile(self.settings_path):
            with open(self.settings_path, 'w') as f:
                json.dump(self.settings_def_dict, f, indent=4)
            return True
        return False

    def read(self):
        """
        Read the settings.json file and return the contents.
        """
        with open(self.settings_path, 'r') as f:
            return json.load(f)

    def write(self, data):
        """
        Write the data to the settings.json file.
        """
        with open(self.settings_path, 'w') as f:
            json.dump(data, f, indent=4)
        return
