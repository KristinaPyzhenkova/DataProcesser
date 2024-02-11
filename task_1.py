import os
import re

from helpers import exceptions_decorator, logger
import const


class DataProcessor:
    def __init__(self, filename, dir_input_path):
        self.filename = filename
        self.dir_input_path = dir_input_path
        self.file_path = os.path.join(self.dir_input_path, self.filename)
        self.dir_output_path = os.path.join(const.current_dir, 'data', 'Result')

    @exceptions_decorator
    def read_file(self):
        with open(self.file_path, 'r') as file:
            data = file.read()
        return data

    @exceptions_decorator
    def write_file(self, data):
        part_filename = re.search(const.part_filename, self.filename)
        filename_output = const.filename.format(part_filename.group(1))
        path_output = os.path.join(self.dir_output_path, filename_output)
        os.makedirs(os.path.dirname(path_output), exist_ok=True)
        with open(path_output, 'w') as file:
            file.write(data)
        logger.info(f'Task completed for {filename_output}!')

    @exceptions_decorator
    def execute(self):
        logger.info(f'Processing file: {self.filename}')
        data = self.read_file()
        if data is None:
            return
        data = self.process_data(data)
        self.write_file(data)

    @staticmethod
    @exceptions_decorator
    def process_data(data):
        data = re.findall(const.data_pattern, data)
        result = ''
        for val in data:
            if '-' in val:
                start_val, end_val = map(int, val.split('-'))
                result += '\n'.join(str(i) for i in range(start_val, end_val + 1))
            else:
                result += str(int(val))
            result += '\n'
        return result


@exceptions_decorator
def main():
    for root, _, files in os.walk(const.direction_data):
        if not re.search(const.folder_pattern, root):
            continue
        for file_name in files:
            if not file_name.startswith(const.startswith_filename):
                continue
            processor = DataProcessor(file_name, root)
            processor.execute()


if __name__ == "__main__":
    main()
