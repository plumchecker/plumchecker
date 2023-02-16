#!/usr/bin/python3
from io import BytesIO
from archives.base import Archive
from tarfile import TarFile

class TarArchive(Archive):
    def __init__(self, path) -> None:
        if type(path) is bytes:
            self.archive = TarFile(fileobj=BytesIO(path))
        else:
            self.archive = TarFile(path)
        
    def iter_dir(self, path=''):
        for file in self.archive.getmembers():
            yield file
    
    def read(self, path):
        return self.archive.extractfile(path).read()
    
    def is_dir(self, path) -> bool:
        return path.isdir()
    
    def name(self, file):
        return file.name