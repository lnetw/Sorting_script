# Для работы данного скрипта необходимо воспользоваться функцией укзания пути либо до ZIP архива либо просто папки
# Затем воспользоваться функцией сортировки файлов из полученного пути в соотествии с тем нужен ли ZIP файл
# или просто папка. В результате получится примерно так:
#   исходная папка
#       icons/tree2015.jpg
#   результирующая папка
#       sort/2015/05/tree2015.jpg

import os, time, shutil, zipfile


class SortPhoto:

    def __init__(self):
        self.source_path = None
        self.out_path = None
        self.cur_file = None
        self.file_time = None
        self.cur_path = None

    def in_dir(self, in_path, final_path):
        self.source_path = os.path.normpath(in_path)
        self.out_path = os.path.normpath(final_path)

    def in_zip(self, in_path, final_path):
        self.source_path = zipfile.ZipFile(in_path, 'r')
        self.out_path = os.path.normpath(final_path)

    def sort_by_data_zip(self):
        for self.file in self.source_path.namelist():
            if os.path.isfile(self.file):
                self.file_time = self.source_path.getinfo(self.file).date_time
                self.cur_path = os.path.join(self.out_path, str(self.file_time[0]),
                                             "{:>02}".format(str(self.file_time[1])))
                if os.path.exists(self.cur_path):
                    self.source_path.extract(self.file, self.cur_path)
                else:
                    os.makedirs(self.cur_path)
                    self.source_path.extract(self.file, self.cur_path)

    def sort_by_data_dir(self):
        for self.dirpath, self.dirname, self.filename in os.walk(self.source_path):
            for self.file in self.filename:
                self.cur_file = os.path.join(self.dirpath, self.file)
                self.file_time = time.gmtime(os.path.getmtime(self.cur_file))
                self.cur_path = os.path.join(self.out_path, str(self.file_time[0]),
                                             "{:>02}".format(str(self.file_time[1])))
                if os.path.exists(self.cur_path):
                    shutil.copy2(self.cur_file, self.cur_path)
                else:
                    os.makedirs(self.cur_path)
                    shutil.copy2(self.cur_file, self.cur_path)


# Пример реализации работы скрипта
Photo = SortPhoto()
Photo.in_zip("C:\Test\icons.zip", "C:\Test\sort")
Photo.sort_by_data_zip()
