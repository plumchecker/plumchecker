#!/usr/bin/python3
from archives.base import Archive
from gzip import GzipFile, decompress

class GzipArchive(Archive):
    def __init__(self, path) -> None:
        super().__init__(path)
        self.archive = GzipFile(path)
        
    def iter_dir(self, path=''):
        return [""]
    
    def read(self, path):
        data = self.archive.read()
        return data
    
    def is_dir(self, path) -> bool:
        return super().is_dir(path)
    
    def name(self, path):
        return super().name(path)