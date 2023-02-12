#!/usr/bin/python3
from archives.base import Archive
from zipfile import ZipFile, Path

class ZipArchive(Archive):
    def __init__(self, path) -> None:
        super().__init__(path)
        self.archive: ZipArchive = ZipFile(path)
        
    def iter_dir(self, path=''):
        path: Path = Path(self.archive, path)
        for file in path.iterdir():
            yield file
    
    def read(self, path):
        return self.archive.read(path)
    
    def is_dir(self, path) -> bool:
        return Path(self.archive, path).is_dir()
    
    def name(self, path):
        return path.name