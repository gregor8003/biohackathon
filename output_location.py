import collections
import os
import shutil


class OutputLocationManager:

    def __init__(self, input_path=None, output_path=None, backup_path=None,
                 preferred_extensions=('.bam', '.bam.bai', '.vcf', '.vcf.gz'),
                 input_filelist=None):
        if input_path is not None:
            self.input_path = input_path
        if output_path is not None:
            self.output_path = output_path
        if backup_path is not None:
            self.backup_path = backup_path
        if input_filelist is not None:
            self.input_filelist = input_filelist
        else:
            self.input_filelist = self._list_input_files()
        self.number_of_samples = None
        self.preferred_extensions = preferred_extensions
        self._init_subdirs()

    def _init_subdirs(self):
        self.input_filelist = self._list_input_files()
        self._subdirs = self._identify_output_subdirs()

    def _identify_output_subdirs(self):
        subdirs = collections.defaultdict(list)
        for input_file_path in self.input_filelist:
            _, path_basename, extension = self._splitext_path_with_dots(input_file_path)
            if extension in self.preferred_extensions:
                subdirs[path_basename].append((input_file_path, extension))
        self.number_of_samples = len(subdirs)
        return subdirs

    def set_input_path(self, input_path):
        if input_path is not None:
            self.input_path = input_path
            self._init_subdirs()

    def set_output_path(self, output_path):
        if output_path is not None:
            self.output_path = output_path

    def set_backup_path(self, backup_path):
        if backup_path is not None:
            self.backup_path = backup_path

    def make_output_files(self):
        for subdir_basename, subdir_extensions in self._subdirs.items():
            subdir_output_path_prefix = os.path.join(self.output_path, subdir_basename)
            if not os.path.exists(subdir_output_path_prefix):
                os.makedirs(subdir_output_path_prefix)
            for input_path, subdir_extension in subdir_extensions:
                subdir_output_path = os.path.join(
                    subdir_output_path_prefix,
                    '{}{}'.format(subdir_basename, subdir_extension)
                )
                print('Creating', subdir_output_path, '... ', end='')
                self.copy_output_file(input_path, subdir_output_path)
                print('done')

    def make_backup_files(self):
        for input_file_path in self.input_filelist:
            _, backup_file_base = os.path.split(input_file_path)
            backup_file_path = os.path.join(self.backup_path, backup_file_base)
            print('Creating', backup_file_path, '... ', end='')
            self.copy_output_file(input_file_path, backup_file_path)
            print('done')

    def copy_output_file(self, file_input_path, file_output_path):
        # shutil.copy2(file_input_path, file_output_path)
        #
        # TODO: stub
        with open(file_output_path, 'w') as wf:
            pass
        # TODO: stub

    def _list_input_files(self):
        return [os.path.join(self.input_path, p) for p in os.listdir(self.input_path)]

    def _splitext_path_with_dots(self, path):
        # https://stackoverflow.com/questions/5930036/separating-file-extensions-using-python-os-path-module
        """splitext for paths with directories that may contain dots."""
        path_without_extensions = os.path.join(
            os.path.dirname(path), os.path.basename(path).split(os.extsep)[0]
        )
        path_basename = os.path.basename(path_without_extensions)
        extensions = os.path.basename(path).split(os.extsep)[1:]
        return (path_without_extensions, path_basename, '.'+'.'.join(extensions))


if __name__ == '__main__':
    olm = OutputLocationManager(
        input_path='C:\\Users\\Public\\Documents\\incoming\\bio-related\\biohackathon_input_path',
        output_path='C:\\Users\\Public\\Documents\\incoming\\bio-related\\biohackathon_output_path',
        backup_path='C:\\Users\\Public\\Documents\\incoming\\bio-related\\biohackathon_backup_path',
#         input_path='C:\\Users\\Public\\Documents\\incoming\\bio-related\\biohackathon_input_path_1',
#         output_path='C:\\Users\\Public\\Documents\\incoming\\bio-related\\biohackathon_output_path_1',
#         backup_path='C:\\Users\\Public\\Documents\\incoming\\bio-related\\biohackathon_backup_path_1',
    )
    print('Number of samples')
    print(olm.number_of_samples)
    print('Creating output')
    olm.make_output_files()
    print('Creating backup')
    olm.make_backup_files()
    print('Number of samples')
    print(olm.number_of_samples)
    print('Preferred extensions:', olm.preferred_extensions)

    print('New path')

    olm.set_input_path('C:\\Users\\Public\\Documents\\incoming\\bio-related\\biohackathon_input_path_1')
    olm.set_output_path('C:\\Users\\Public\\Documents\\incoming\\bio-related\\biohackathon_output_path_1')
    olm.set_backup_path('C:\\Users\\Public\\Documents\\incoming\\bio-related\\biohackathon_backup_path_1')
    print('Number of samples')
    print(olm.number_of_samples)
    print('Creating output')
    olm.make_output_files()
    print('Creating backup')
    olm.make_backup_files()
    print('Number of samples')
    print(olm.number_of_samples)
    print('Preferred extensions:', olm.preferred_extensions)
