#!/usr/bin/python3
import logging

from network import QueryType, QueryParams, send_file, send_query
from config import Config
from archives import ArchiveFactory, Archive
from filetype import (is_archive, get_type, guess as guess_type, guess_extension)
from argparse import ArgumentParser, Namespace
from pathlib import Path
from typing import Iterable
from os import remove

def add_file(filename: str or bytes, recursive_archives: bool, config: Config) -> None:
    # init logger
    logger: logging.Logger = logging.getLogger("Add.file")
    
    is_an_archive: bool = is_archive(filename)
    if is_an_archive:
        extension = guess_type(filename)
        known_extensions = [get_type(ext = "gz"), 
                            get_type(ext = "tar"), 
                            get_type(ext = "zip")]
        if not extension in known_extensions:
            raise NotImplementedError(f"We don't know how to process archive type {extension.extension} for file {filename}")
        archive: Archive = ArchiveFactory().openArchive(filename)
        # replace filename if bytes were passed
        if type(filename) is bytes:
            filename = "archive.tar"
        paths = [Path('')]
        while len(paths) > 0:
            directory = paths.pop()
            for item in archive.iter_dir(directory):
                if archive.is_dir(item) and recursive_archives:
                    paths.append(directory / item)
                elif not archive.is_dir(item):
                    # check if there is a tar
                    file = archive.read(item)
                    if guess_extension(file) == "tar":
                        logger.info(f".tar file detected inside {filename}! Parsing it as well...")
                        add_file(file, recursive_archives, config)
                    else:
                        logger.info(f"Adding file {archive.name(item)} from archive {filename}")
                        send_file(file, config)
    else:
        # TODO: Add file processing
        pass

def add_data(args: Namespace, config: Config):
    # init logger
    logger: logging.Logger = logging.getLogger("Add")
    # check if it's a real folder/file
    path = Path(args.path)
    if path.is_dir():
        folder_files: Iterable[Path] = []
        if args.recursive_folders:
            folder_files = path.glob("**/*")
        else:
            folder_files = set(path.glob("*")) - set(path.glob("**"))
        for file in folder_files:
            try:
                logger.info(f"Adding {str(file)}...")
                add_file(file, args.recursive_archives, config)
            except NotImplementedError as e:
                logger.error(f"\tUnable to add file {str(file)} because\n\t\t{str(e)}")
        try:
            remove('from_archive.txt')
        except FileNotFoundError:
            pass # It's okay
    elif path.is_file():
        logger.info(f"Adding {str(args.path)}...")
        add_file(args.path, args.recursive_archives, config)
    else:
        logger.warning(f"Nothing found at path {str(path)}. Please check your input.")
        

def query_data(args: Namespace, config: Config):
    query_args = QueryParams(args.field, " ".join(args.keyword), not args.all, args.page)
    send_query(query_args, config)

def main():
    # setup logging first
    logging_handler = logging.StreamHandler()
    logging_formatter = logging.Formatter("[%(levelname)s][%(name)s][%(asctime)s] %(message)s")
    logging_handler.setFormatter(logging_formatter)
    logging.Logger.root.addHandler(logging_handler)
    # open config
    config = Config()
    
    parser = ArgumentParser(prog = 'Plumchecker',
                            description = 'Parse and query leaked password DB\'s')
    parser.add_argument('--verbosity', '-v', 
                        type = int,
                        default = 2,
                        help = '''how verbose should output be. Levels: \
                                4 - Error, \
                                3 - Warning, \
                                2 - Info, \
                                1 - Debug.''',
                        metavar = "LEVEL")
    subparser = parser.add_subparsers(title = 'Subcommands', 
                                      description = 'Available commands: add, query', 
                                      required = True)
    
    # define params for 'add' command
    parser_add = subparser.add_parser('add', 
                        description = 'Add leaked data to the plumchecker database')
    parser_add.add_argument('path',
                            help = 'path to a folder, a text file (.txt or .csv) or an archive (.zip/.tar/.gz)',
                            nargs = '?',
                            default = './')
    parser_add.add_argument('--recursive-folders', '-rf',  
                            action = 'store_true',
                            help = "Whether to look for files in folders recursively.")
    parser_add.add_argument('--recursive-archives', '-ra',  
                            action = 'store_true',
                            help = "Whether to look for files in archives recursively.")
    parser_add.set_defaults(func = add_data)
    
    # define params for 'query' command
    parser_query = subparser.add_parser('query', 
                        description = 'Query leaked data from the plumchecker database')
    parser_query.add_argument('--field', '-f',
                              choices = [QueryType.DOMAIN, QueryType.PASS, QueryType.LOGIN],
                              type = QueryType,
                              default = QueryType.LOGIN,
                              help = 'field to filter',
                              metavar = 'NAME')
    parser_query.add_argument('keyword',
                              nargs='+')
    parser_query.add_argument('--all', '-a',
                              action = 'store_true',
                              help = 'do not use pagination and receive all output there is')
    parser_query.add_argument('--page', '-p',
                              type = int,
                              default = 1,
                              help = 'what page to output. Default - 1',
                              metavar = 'NUMBER')
    parser_query.set_defaults(func = query_data)
    
    args = parser.parse_args()
    logging.Logger.root.setLevel(args.verbosity * 10)
    try:
        args.func(args, config)
    except NotImplementedError as e:
        logging.getLogger("D'oh").critical(f"Something went wrong: \n{str(e)}\nWe're sorry!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nThank you for using plumchecker! Exiting...")