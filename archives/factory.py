#!/usr/bin/python3
from filetype import guess_extension
from typing import Dict
from archives.base import Archive
from archives.zip import ZipArchive
from archives.gzip import GzipArchive
from archives.tar import TarArchive

class ArchiveFactory:
    def __init__(self):
        self.available_formats: Dict[Archive] = {"zip": ZipArchive,
                                                 "gz": GzipArchive,
                                                 "tar": TarArchive}
    
    def openArchive(self, path) -> Archive:
        extension = guess_extension(path)
        print(extension)
        # try:
        return self.available_formats.get(extension)(path)
        # except Exception as e:
        #     raise ValueError(f"Unknown extension led to error: {str(e)}")