import json
import os

from database import BotDatabase
from generate_templates import GenerateTemplates
from link_grabber import LinkGrabber
from settings import Settings

from colorama import Fore, init
init()


def display_config(config) -> str:
    return f'''{Fore.LIGHTWHITE_EX}Discord Porn Bot Generator v1.0 by the-cult-of-integral
{Fore.CYAN}https://github.com/the-cult-of-integral/discord-porn-bot-generator

{Fore.LIGHTWHITE_EX}Currently running with the following config
-------------------------------------------
{Fore.CYAN}SETTINGS_PATH\t\t{Fore.LIGHTYELLOW_EX}{config['SETTINGS_PATH']}
{Fore.CYAN}SETTINGS_RUN_DEF_DICT\t{Fore.LIGHTYELLOW_EX}{str(config['SETTINGS_RUN_DEF_DICT']).lower()}
{Fore.CYAN}VERBOSE\t\t\t{Fore.LIGHTYELLOW_EX}{str(config['VERBOSE']).lower()}

{Fore.RESET}'''


def main() -> None:

    if not os.path.exists(f'{os.path.normpath("dist/")}'):
        os.mkdir(os.path.normpath('dist/'))
        os.mkdir(os.path.normpath('dist/cogs'))

    with open('dpbg_config.json', 'r') as f:
        config = json.load(f)

    settings = Settings(config)
    db = BotDatabase(config, settings)
    lg = LinkGrabber()
    gt = GenerateTemplates(settings)

    if not config['SETTINGS_RUN_DEF_DICT'] and settings.def_settings:
        print(f'{Fore.LIGHTBLUE_EX}Default settings created — please edit {Fore.YELLOW}settings.json{Fore.LIGHTBLUE_EX}, then run this program again{Fore.RESET}\n\nEnter anything to exit: ', end='')
        input()
        exit(0)
    else:
        if _ := db.create_tables():

            print(display_config(config))

            print(f'{Fore.LIGHTWHITE_EX}Enter a token for the generated bot to use: {Fore.GREEN}', end='')
            token = input()

            categories = settings.read_val('categories')

            for category, meta in categories.items():
                tag = meta[0]
                print(
                    f'\n{Fore.LIGHTMAGENTA_EX}Grabbing links for {Fore.YELLOW}{tag}{Fore.LIGHTMAGENTA_EX}...{Fore.RESET}')
                links = lg.grab_links(tag)
                print('')

                links = list(map(lambda x: x.file_url, links))

                print(
                    f'{Fore.LIGHTMAGENTA_EX}Inserting links for {Fore.YELLOW}{tag}{Fore.LIGHTMAGENTA_EX}...{Fore.RESET}')
                for link in links:
                    if not db.insert_values_into_table([link, category]):
                        print(
                            f'{Fore.LIGHTRED_EX}Failed to insert link: {link}{Fore.RESET}')
                        continue

            if gt.generate_template(os.path.normpath('templates/main.txt'), 'main', token):
                print(
                    f'\n{Fore.LIGHTYELLOW_EX}Successfully generated main.py{Fore.RESET}')
            else:
                print(
                    f'\n{Fore.LIGHTRED_EX}Failed to generate main.py{Fore.RESET}')
                return
            del token

            if gt.generate_template(os.path.normpath('templates/databases.txt'), 'databases'):
                print(f'{Fore.LIGHTYELLOW_EX}Successfully generated databases.py')
            else:
                print(
                    f'{Fore.LIGHTRED_EX}Failed to generate databases.py{Fore.RESET}')
                return

            if gt.generate_template(os.path.normpath('templates/config.txt'), 'config', isCog=True):
                print(f'{Fore.LIGHTYELLOW_EX}Successfully generated config.py')
            else:
                print(f'{Fore.LIGHTRED_EX}Failed to generate config.py{Fore.RESET}')
                return

            if gt.generate_template(os.path.normpath('templates/info.txt'), 'info', isCog=True):
                print(f'{Fore.LIGHTYELLOW_EX}Successfully generated info.py')
            else:
                print(f'{Fore.LIGHTRED_EX}Failed to generate info.py{Fore.RESET}')
                return

            if gt.generate_template(os.path.normpath('templates/nsfw.txt'), 'nsfw', isCog=True):
                print(f'{Fore.LIGHTYELLOW_EX}Successfully generated nsfw.py')
            else:
                print(f'{Fore.LIGHTRED_EX}Failed to generate nsfw.py{Fore.RESET}')
                return

            print(
                f'\n\n{Fore.LIGHTGREEN_EX}Generation complete!{Fore.RESET}\n\nEnter anything to exit: ', end='')
            input()
            exit(0)

    return


if __name__ == '__main__':
    main()
