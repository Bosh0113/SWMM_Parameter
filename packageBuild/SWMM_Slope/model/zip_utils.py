# coding=utf-8
import os
import zipfile


def zip_dirs(dir_list, zip_filename):
    zip_file = zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED, allowZip64=True)
    for dir_path in dir_list:
        parent_dir = os.path.dirname(dir_path)
        for path, dir_list, file_list in os.walk(dir_path):
            # 去掉目标根路径，只对目标文件夹下边的文件及文件夹进行压缩
            file_path = path.replace(parent_dir, "")
            for filename in file_list:
                zip_file.write(os.path.join(path, filename), os.path.join(file_path, filename))
    zip_file.close()


def unzip_dir(zipfilename, unzipdirname):
    fullzipfilename = os.path.abspath(zipfilename)
    fullunzipdirname = os.path.abspath(unzipdirname)
    #Check input
    if not os.path.exists(fullzipfilename):
        return
    if not os.path.exists(fullunzipdirname):
        os.mkdir(fullunzipdirname)

    #Start extract files
    with  zipfile.ZipFile(fullzipfilename,'r') as myzip:
        myzip.extractall(fullunzipdirname)
        # myzip.extracting.close()