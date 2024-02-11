import os

current_dir = os.path.dirname(__file__)
direction_data = os.path.join(current_dir, 'data')
part_filename = r'TEST_AUCHAN(.*?)\.txt'
filename = 'TEST_AUCHAN_success{}.txt'
data_pattern = r"\d+-\d+|\d+"
folder_pattern = r'/data/TEST_Folder'
startswith_filename = 'TEST_'
