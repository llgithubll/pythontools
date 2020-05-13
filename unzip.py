import os
import os.path
import tarfile


path = os.getcwd()
print(path)
d = os.listdir(path)


for name in d:
    if name.endswith('tar.gz'):
        print(name)
        tar = tarfile.open(os.path.join(path, name), 'r:gz')
        tar.extractall()
        tar.close()

d = os.listdir(path)
for name in d:
    if name.endswith('tar'):
        print(name)
        tar = tarfile.open(os.path.join(path, name), 'r:')
        tar.extractall()
        tar.close()