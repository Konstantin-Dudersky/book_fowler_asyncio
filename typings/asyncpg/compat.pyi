"""
This type stub file was generated by pyright.
"""

import pathlib

SYSTEM = ...
if SYSTEM == 'Windows':
    CSIDL_APPDATA = ...
    def get_pg_home_directory() -> pathlib.Path:
        ...
    
else:
    def get_pg_home_directory() -> pathlib.Path:
        ...
    
async def wait_closed(stream): # -> None:
    ...

async def wait_for(fut, timeout):
    ...
