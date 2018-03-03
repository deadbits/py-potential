# Potentially Useful Python Functions
`potent.py` is meant to be a single library that contain many Python functions I would end up using on a regular basis and across multiple projects. There were so many times that I would re-write the same functions every {day|week|month}, I figured this might be a better solution: do it once, import, repeat.

There are multiple classes within potent.py and each function of within the classes are static methods so they aim to be more easily accessible. The classes are purely organizational.

This is obviously by no means meant to be all-inclusive and is more tailored towards use-cases I've encountered during my personal and professional projects, but this repo is glad to accept Pull Requests and Issues :D

***

Take a quick look at the following example that checks if a certain process is running and kill any of it's child processes using the built-in threading support:

```
from potent import System
from potent import threaded

@threaded
def kill_child_procs(process_id):    
    System.kill_process(process_id)

def my_func(arg):    
    if System.is_running(args):        
        children = System.get_children(arg)        
        results = []        
        for proc in children:            
            results.append(kill_child_procs(proc))        
            print results
```  

### Batteries Included
- threading decorator
- System class    
    - check if PID is running    
    - check if PID has threads and return them    
    - check if PID has children and return them      
    - kill those children    
    - safely execute a system command        
        - maybe wrap this the threading decorator, eh? ;-)    
    - get random n bytes from /dev/urandom    
    - get random n bytes from /dev/random
- Validate class    
     - verify string is acceptable for filenames and HTML display    
     - verify URL    
     - verify IPv4 address
     - validate Yara rule syntax **not yet implemented**
- Time   
    - UTC timestamp as string    
    - UTC timestamp as object    
    - get duration of a thing you run **not yet implemented**
- Encode    
    - XOR        
        - single byte        
        - four byte        
        - rolling    
    - RC4 encrypt & decrypt    
    - base64 encode    
    - base64 decode    
    - get digest of HMA SHA256 from data and key  **not yet implemented**
    - base64 encode and zlib compress data    **not yet implemented**
    - base64 decode and zlib decompress data    **not yet implemented**
    - convert hex to integer    **not yet implemented**
    - convert integer to hex **not yet implemented**
- Files    
    - get entropy of file or buffer    
    - check if file is valid (path exists, is not a directory, and size is greater than 0)    
    - write data to a file    
    - read data from a file        
        - optionally split data lines and return as list    
    - get size of file    
    - get basename of file path    
    - get Magic MIME type from file path or buffer    
    - run Yara {directory|file} signature against {file|buffer}  **not yet implemented**
    - create temporary directory   **not yet implemented** 
    - create temporary file    **not yet implemented**
    - write a JSON object or instance of object to file as dictionary **not yet implemented**
- Network  **not yet implemented**
    - make DNS request and get all response data  
    - open a listening TCP socket on port {whatever}  
    - connect to a listening TCP socket  
    - initialize a SOCKS5 proxy to a {host:port} of your choosing  - execute a command on a remote SSH server
