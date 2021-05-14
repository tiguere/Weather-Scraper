"""
scraping project - part 2
CLI parser module
"""
import click
import config as cfg
import logging


class ClickParser:
    def __init__(self):
        print("ClickParser instantiated")
        logging.info("ClickParser instantiated")

    @click.command()
    @click.option('--days', default=14, type=click.IntRange(0, 14), help='Number of Days')
    @click.option('--filename', default=cfg.FILENAME)
    @click.option('--search_type',
                  type=click.Choice(['forecast', 'historical'], case_sensitive=False),
                  multiple=True,
                  default=('forecast', 'historical'))
    def get_arguments(self, days, filename, search_type):
        """
        receives CLI arguments and returns a dictionary with their keys and values
        """
        arguments_dict = {'days': days, 'filename': filename, 'search_type': search_type}
        return arguments_dict
