import os
import time
import subprocess

def compile_translations():
    print("Compiling translations...")
    subprocess.run(['pybabel', 'compile', '-d', 'translations'])

def watch_translations():
    translation_files = []
    for root, dirs, files in os.walk('translations'):
        for file in files:
            if file.endswith('.po'):
                translation_files.append(os.path.join(root, file))

    last_modified_times = {file: os.path.getmtime(file) for file in translation_files}

    while True:
        time.sleep(1)
        for file in translation_files:
            current_time = os.path.getmtime(file)
            if current_time != last_modified_times[file]:
                last_modified_times[file] = current_time
                compile_translations()

if __name__ == '__main__':
    compile_translations()
    watch_translations()
