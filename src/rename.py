import os
import re
import pandas as pd
path = './dataset/Ethereum/'
regex = re.compile('\d{4}-\d{2}-\d{2}')
# for name in os.listdir(path):
#     try:
#         old_file = os.path.join(path,name)
#         new_name = regex.match(name).group() + ".csv"
#         new_file = os.path.join(path, new_name)
#         os.rename(old_file, new_file)
#     except:
#         pass