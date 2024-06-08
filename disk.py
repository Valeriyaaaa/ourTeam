import yadisk

class YandexDisk:
    def __init__(self, token):
        self.disk = yadisk.YaDisk(token=token)

    def check_new_files(self, folder_path):
        # Проверка новых файлов в указанной папке
        files = list(self.disk.listdir(folder_path))
        return files
