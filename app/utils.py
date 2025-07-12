# app/utils.py

def get_file_bytesio(files):
    file_objs = []
    for f in files:
        f.seek(0)
        file_objs.append({"name": f.name, "bytes": f.read()})
    return file_objs
