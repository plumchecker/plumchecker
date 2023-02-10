This is an official repository of Plumchecker-cli - one of the *best* leaked password data viewer out there!
# Install
Project was written with Python 3.10; Older versions were not tested for compatibility - feel free to tell us if they work correctly or not.
## External packages
- filetype

Install with requirements.txt:

```bash
# With pip3
pip3 install -r requirements.txt
# With python3
python3 -m pip install -r requirements.txt
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
