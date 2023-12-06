def read_lines(file_name: str, data_dir_path: str = "./data", test = False):
    file_name = f"test/{file_name}" if test else file_name
    file_path: str = f"{data_dir_path}/{file_name}"
    
    lines: [str] = []
    with open(file_path, 'r') as f:
        lines = [line.removesuffix('\n').strip() for line in f.readlines()]
    return lines
