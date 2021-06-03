import os
from datetime import datetime, timedelta


class Daemon:
    """Класс бота-клинера"""
    def __init__(self, path):
        self.deleted_files = 0
        self.deleted_files_list = []
        self.folder = path
        self.this_date = datetime.today()
        self.extensions = ['.log', '.root', '.doses']

    def check_folder(self):
        """Метод проверки файлов папки на совпадение с условиями"""
        for filename in os.listdir(self.folder):
            file_path = os.path.join(self.folder, filename)
            file, file_extension = os.path.splitext(filename)
            last_time_mod = datetime.fromtimestamp(os.path.getmtime(file_path))
            if file_extension in self.extensions and self.this_date - last_time_mod >= timedelta(days=30):
                self.delete_file(file_path, last_time_mod)
        self.create_log()

    def delete_file(self, filepath, last_time_mod):
        """Метод для удаления файлов"""
        if os.path.isfile(filepath):
            os.remove(filepath)
            self.deleted_files += 1
            self.deleted_files_list.append(filepath + " - last modification: " + str(last_time_mod.isoformat(' ', 'seconds')))

    def create_log(self):
        """Метод, записывающий лог-файл"""
        logs = {"Deleted files": self.deleted_files,
                "Date of last cleaning": self.this_date.isoformat(' ', 'seconds')}

        if self.deleted_files != 0:
            with open('cleaner_logs.txt', 'w') as out:
                for key, val in logs.items():
                    out.write('{}: {}\n'.format(key, val))

            with open('cleaner_logs.txt', 'a') as out_add:
                out_add.write('\nDeleted files list:\n')
                for _ in self.deleted_files_list:
                    out_add.write(_)
                    out_add.write('\n')


# путь к папке, которую будем чистить
folder_path = r'D:\testfolder'
Daemon(folder_path).check_folder()
