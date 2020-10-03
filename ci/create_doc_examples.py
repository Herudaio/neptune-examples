import os
from subprocess import call
import yaml

from ci.utils import clean_py_script

with open('config.yaml') as file:
    config = yaml.load(file)

DIRS = config['create_docs']['dirs']
EXCLUDED_PATHS = config['create_docs']['excluded_dirs']

CONVERT_TO_PYTHON = """jupyter nbconvert \
    --TagRemovePreprocessor.enabled=True \
    --TagRemovePreprocessor.remove_cell_tags="['remove_docs_script']" \
    --output-dir {} \
    --to python {}
    """

STRIP_CELLS = """jupyter nbconvert \
    --TagRemovePreprocessor.enabled=True \
    --TagRemovePreprocessor.remove_cell_tags="['remove_docs_colab']" \
    --output-dir {} \
    --to notebook {}
    """

for dir in DIRS:
    for root, dirs, files in os.walk(dir):
        for name in files:
            if any(p in root for p in EXCLUDED_PATHS):
                continue
            path = os.path.join(root, name)
            docs_dir = os.path.join(root, 'docs')
            os.makedirs(docs_dir, exist_ok=True)

            command = CONVERT_TO_PYTHON.format(docs_dir, path)
            call(command, shell=True)

            path_of_py_file = os.path.join(docs_dir, name).replace('.ipynb','.py')
            clean_py_script(path_of_py_file)

            command = STRIP_CELLS.format(docs_dir, path)
            call(command, shell=True)