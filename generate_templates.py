import logging
import os

from settings import Settings

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S', filename='dpbg.log', filemode='w')


class GenerateTemplates:
    def __init__(self, settings=Settings):
        self.settings = settings
        return

    def generate_template(self, template_path=str, name=str, token='', isCog=False) -> bool:
        """
        Generate a template.
        """
        try:
            with open(template_path, 'r') as f:
                template = f.read()
                template = template.replace(
                    'DB_NAME', self.settings.read_val('database_name'))
                template = template.replace('TOKEN', token)
                template = template.replace(
                    'PREFIX', self.settings.read_val('prefix'))
                template = template.replace('STATUSES', str(
                    self.settings.read_val('status')))
                template = template.replace('CATEGORIES', str(
                    self.settings.read_val('categories')))
                template = template.replace(
                    'TITLE', self.settings.read_val('help_embed')['title'])
                template = template.replace(
                    'COLOR', self.settings.read_val('help_embed')['color'])
                template = template.replace(
                    'IMAGE', self.settings.read_val('help_embed')['image'])
                template = template.replace('FOOTER', self.settings.read_val(
                    'help_embed')['footer'])
                template = template.replace(
                    'LOG', self.settings.read_val('log_name'))
                template = template.replace(
                    'NSFW_COMMANDS', self.get_nsfw_commands())
                template = template.replace('FIELDS', self.get_fields())

                if isCog:
                    path = os.path.normpath(f'dist/cogs/{name}.py')
                else:
                    path = os.path.normpath(f'dist/{name}.py')

                with open(path, 'w') as f:
                    f.write(template)

            logging.info(f'Successfully generated template "{template_path}"')
            return True
        except Exception as e:
            logging.error(
                f'Failed to generate template "{template_path}": {e}')
            return False

    def get_nsfw_commands(self) -> str:
        """
        Get the NSFW commands.
        """
        nsfw_commands = ''
        categories = self.settings.read_val('categories')
        for category in categories.keys():
            nsfw_commands += f'''
    @commands.command(aliases={categories[category][1]})
    async def {category}(self, ctx) -> None:
        await self.bot.get_command('send_img').callback(self, ctx, '{category}')
        return
        '''
        return nsfw_commands

    def get_fields(self) -> str:
        """
        Get the help embed fields.
        """
        fields = ''
        categories = self.settings.read_val('categories')
        for category in categories.keys():
            fields += f'''embed.add_field(name='{category}', value='{categories[category][2]}')
        '''
        return fields
