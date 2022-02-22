import venv
from tempfile import mkdtemp
from os.path import join
import sys
import subprocess
import shutil

temp_path = mkdtemp()
venv.create(temp_path, with_pip = True)
subprocess.run([join(temp_path, 'bin', 'pip'), 'install', 'pyfiglet'])
subprocess.run([join(temp_path, 'bin', 'python'), '-m', 'figdate', *sys.argv[1:]])
shutil.rmtree(temp_path)
