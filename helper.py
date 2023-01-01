from pathlib import Path

def file_path_check(file_path):
    ''' check whether file and path exists
    

    :return: true of false
    '''
    if not Path(file_path).is_file():
        return False
    else:
        return True 

def path_create(path):
    
    Path.mkdir(path, exist_ok=True, parents=True)