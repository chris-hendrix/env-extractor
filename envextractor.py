import os
import yaml
from datetime import date
import shutil


FILE_TYPES = ['.env', 'settings.yaml']


def get_settings(settings_yaml):
    with open(settings_yaml, "r") as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            return


def is_env_file(filename):
    for ft in FILE_TYPES:
        if filename.endswith(ft):
            return True
    return False


def get_env_files(dir, max_depth=5, depth=0, env_files=[]):

    if depth > max_depth:
        return

    for f in os.scandir(dir):
        if f.is_dir():
            if f.path.endswith('node_modules'):
                continue
            get_env_files(f.path, max_depth, depth+1, env_files)
        elif f.is_file():
            if is_env_file(f.name):
                env_files.append(f.path)
    return env_files


def copy_env_files(env_files, root_dir, out_dir):
    for env_file in env_files:
        src_file = os.path.abspath(env_file)
        copy_file = env_file.replace(root_dir, '')
        copy_file = os.path.join(out_dir, copy_file)
        copy_dir = os.path.dirname(copy_file)
        print(src_file)
        print(copy_dir)
        if not os.path.exists(copy_dir):
            os.makedirs(copy_dir)
        shutil.copyfile(src_file, copy_file)


if __name__ == "__main__":
    settings = get_settings('settings.yaml')
    root_dir = settings['root_dir']
    out_dir = settings['out_dir']
    env_files = get_env_files(root_dir)
    out_dir = os.path.join(out_dir, str(date.today()))
    copy_env_files(env_files, root_dir, out_dir)
