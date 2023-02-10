#!/usr/bin/python3
import argparse
import filetype

from pathlib import Path
from typing import Iterable

def add_file(filename, recursive_archives):
    is_archive = filetype.is_archive(filename)
    if is_archive:
        extension = filetype.guess(filename)
        known_extensions = [filetype.get_type(ext = "gz"), 
                            filetype.get_type(ext = "tar"), 
                            filetype.get_type(ext = "zip")]
        if not extension in known_extensions:
            raise NotImplementedError(f"We don't know how to process archive type {extension.extension} for file {filename}")
        # TODO: Add in-archive file iteration
    else:
        # TODO: Add file processing
        pass

def add_data(args):
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
                print(f"Adding {str(file)}...")
                add_file(file, args.recursive_archives)
            except NotImplementedError as e:
                print(f"\tUnable to add file {str(file)} because\n\t\t{str(e)}")
        pass
    elif path.is_file():
        print(f"Adding {str(file)}...")
        add_file(args.path, args.recursive_archives)
    else:
        print(f"Nothing found at path {str(path)}. Please check your input.")
        

def query_data(args):
    # TODO: Add data querying
    pass

def main():
    parser = argparse.ArgumentParser(prog = 'Plumchecker',
                                     description = 'Parse and query leaked password DB\'s')
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
    parser_query.set_defaults(func = query_data)
    
    args = parser.parse_args()
    try:
        args.func(args)
    except NotImplementedError as e:
        print(f"Something went wrong: \n{str(e)}\nWe're sorry!")

if __name__ == "__main__":
    main()