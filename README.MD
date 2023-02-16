This is an official repository of Plumchecker-cli - one of the *best* leaked password data viewer out there!
# Install
Project was written with Python 3.10; Older versions were not tested for compatibility - feel free to tell us if they work correctly or not.
It is recommended to clone the repository with `--recursive-submodules` option as it uses submodules to get necessary modules
## External packages
- filetype
- jsonschema

Install with requirements.txt:

```bash
# With pip3
pip3 install -r requirements.txt
# With python3
python3 -m pip install -r requirements.txt
```
# Configure
Configuration file is located in `config.json`. Make sure to set correct hostname and port for your storage module.
# Prepare
Plumchecker requires a working storage module in background. You can launch one locally (`go`, `docker` and `docker-compose` are reqired):
```bash
$ cd backend/storage
$ docker build -t plumchecker-storage .
$ docker-compose up [-d]
```
# Usage examples
## Add folder of files into database
```bash
python3 plumchecker.py add /path/to/folder/ [--recursive-folders]
```
## Add file into database
Supported file extensions: `.txt`, `.csv`
```bash
python3 plumchecker.py add /path/to/folder/file.txt
```
## Add archive with text files into database
Supported archive formats: `.zip`, `.tar`, `.gz`
```bash
python3 plumchecker.py add /path/to/folder/archive [--recursive-archives]
```
## Search for all mails with 'qwerty' as a password
```bash
python3 plumchecker.py query --all --field password qwerty
```
## Search for Gmail mails in a database 
```bash
python3 plumchecker.py query --field domain gmail.com [--page N]
```
