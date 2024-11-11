# -*- coding: UTF-8 -*-
import os
"""
Created on file content analysis
@author: <LMM>
"""


class FolderTool(object):
    def __init__(self, folder_path, suffix, subfolders=False):
        self.folder_path = folder_path
        self.suffix = suffix   # ['.ipynb', '.jpg', '.txt', ...]
        self.file_list = []
        if subfolders:
            self.work_folder()
        else:
            self.list_folder()

    # listdir
    def list_folder(self):
        for filename in os.listdir(self.folder_path):
            if filename.endswith(self.suffix):
                file_path = os.path.join(self.folder_path, filename)
                self.file_list.append(file_path)

    # walk
    def work_folder(self):
        for dirpath, dirnames, filenames in os.walk(self.folder_path):
            for filename in filenames:
                if filename.endswith(self.suffix):
                    file_path = os.path.join(dirpath, filename)
                    self.file_list.append(file_path)

    # ipynb 2 py
    def ipynb2py(self):
        from nbconvert import ScriptExporter
        exporter = ScriptExporter()
        for file_path in self.file_list:
            output, _ = exporter.from_filename(file_path)
            new_file_path = os.path.splitext(file_path)[0] + '.py'
            with open(new_file_path, 'w') as f:
                f.write(output)
                print(f"已将 {file_path} 转换为 {os.path.basename(new_file_path)}")

    def delete_file(self):
        for file_path in self.file_list:
            os.remove(file_path)
            print(f"已将 {file_path} 删除")


if __name__ == "__main__":
    folder_path = 'D:/PycharmProjects/Time-Series-Analysis'
    folder_tool = FolderTool(folder_path, '.py', subfolders=True)
    # folder_tool.ipynb2py()
    folder_tool.delete_file()