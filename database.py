import logging
import os
import sqlite3

from settings import Settings

from colorama import Fore, init
init()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S', filename='dpbg.log', filemode='w')


class BotDatabase:

    def __init__(self, dpbg_config, settings=Settings) -> None:
        """
        Open the connection to the database.
        """
        self.settings = settings
        self.verbose = dpbg_config['VERBOSE']
        self.conn = sqlite3.connect(os.path.normpath(
            f'dist/{self.settings.read_val("database_name")}'))
        self.cursor = self.conn.cursor()
        return

    def create_tables(self) -> bool:
        """
        Create all the tables.
        """
        a = self.create_servers_table()
        if a:
            logging.info(f'Successfully created servers table')
        else:
            logging.error(f'Failed to create servers table')

        b = self.create_metrics_table()
        if b:
            logging.info(f'Successfully created metrics table')
        else:
            logging.error(f'Failed to create metrics table')

        c = self.create_links_table()
        if c:
            logging.info(f'Successfully created links table')
        else:
            logging.error(f'Failed to create links table')

        d = self.create_nsfw_table()
        if d:
            logging.info(f'Successfully created nsfw table')
        else:
            logging.error(f'Failed to create nsfw table')

        if a and b and c and d:
            return True
        else:
            return False

    def create_servers_table(self) -> bool:
        """
        Create a datable table for servers the bot is in.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        
        """
        sql = f'''CREATE TABLE IF NOT EXISTS Servers (
            server_id INTEGER NOT NULL PRIMARY KEY
        );'''
        return self.__exec_nonselect(sql)

    def create_metrics_table(self) -> bool:
        """
        Create a table for metrics.
        """
        sql = f'''CREATE TABLE IF NOT EXISTS Metrics (
            server_id INTEGER NOT NULL PRIMARY KEY, 
            '''
        categories = self.settings.read_val('categories')
        for category in categories.keys():
            sql += f'{category}_prev_link TEXT, \n\t'
        sql += 'FOREIGN KEY (server_id) REFERENCES Servers(server_id));'
        return self.__exec_nonselect(sql)

    def create_links_table(self) -> bool:
        """
        Create a database table for links.
        """
        sql = f'''CREATE TABLE IF NOT EXISTS Links (
            link_id INTEGER PRIMARY KEY,
            link_url TEXT,
            link_category TEXT,
            UNIQUE (link_url, link_category)
            );'''
        return self.__exec_nonselect(sql)

    def create_nsfw_table(self) -> bool:
        """
        Create a database for NSFW configuration
        """
        sql = f'''CREATE TABLE IF NOT EXISTS NSFWConfigs (
            server_id INTEGER NOT NULL PRIMARY KEY, 
            '''
        categories = self.settings.read_val('categories')
        for category in categories.keys():
            sql += f'do{category.lower().title()} BOOLEAN NOT NULL DEFAULT(TRUE), \n\t'
        sql += '''onlyNSFW BOOLEAN NOT NULL DEFAULT(TRUE), 
        FOREIGN KEY (server_id) REFERENCES Servers(server_id));'''
        return self.__exec_nonselect(sql)

    def insert_values_into_table(self, values=list) -> bool:
        """
        Insert the values into the table in the settings.json file.
        """
        if self.verbose:
            print(
                f'{Fore.LIGHTBLACK_EX}Inserting {values} into Links table{Fore.RESET}')
            logging.info(f'Inserting {values} into Links table')
        sql = f'INSERT INTO Links (link_url, link_category) VALUES (?, ?);'
        return self.__exec_nonselect(sql, values)

    def __exec_select(self, sql, params=None) -> bool:
        """
        Small Cursor.execution function for SELECT queries.
        """
        try:
            if params is None:
                self.cursor.execute(sql)
            else:
                self.cursor.execute(sql, params)
        except sqlite3.Error as e:
            logging.error(e)
            return False
        return True

    def __exec_nonselect(self, sql, params=None) -> bool:
        """
        Small Cursor.execution function for non-SELECT queries.
        """
        try:
            if params is None:
                self.cursor.execute(sql)
            else:
                self.cursor.execute(sql, params)
            self.conn.commit()
        except sqlite3.Error as e:
            logging.error(e)
            return False
        return True

    def __del__(self) -> None:
        """
        Close the connection to the database.
        """
        self.cursor.close()
        self.conn.close()
        return
