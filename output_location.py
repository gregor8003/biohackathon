from datetime import datetime
from zipfile import ZipFile
import collections
import os
import shutil
import zipfile


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

    def set_preferred_extensions(self, preferred_extensions):
        self.preferred_extensions = preferred_extensions
        self._init_subdirs()

    def make_output_files(self):
        print('in output')
        for subdir_basename, subdir_extensions in self._subdirs.items():
            subdir_output_path_prefix = os.path.join(self.output_path, subdir_basename)
            if not os.path.exists(subdir_output_path_prefix):
                os.makedirs(subdir_output_path_prefix)
            for input_path, subdir_extension in subdir_extensions:
                subdir_output_path = os.path.join(
                    subdir_output_path_prefix,
                    '{}{}'.format(subdir_basename, subdir_extension)
                )
                # print('Creating', subdir_output_path, '... ', end='')
                self.copy_output_file(input_path, subdir_output_path)
                print('done')

    def make_backup_input_files(self):
        backup_file_base, backup_file_path = (
            self._get_backup_archive_path(mode_suffix='input')
        )
        backup_file_dir, _ = os.path.splitext(backup_file_base)
        print('Creating backup file', backup_file_path)
        zipf = ZipFile(
            backup_file_path, 'w', compression=zipfile.ZIP_DEFLATED, allowZip64=True
        )
        for input_path in self.input_filelist:
            _, input_path_basename = os.path.split(input_path)
            arch_file_path = os.path.join(backup_file_dir, input_path_basename)
            # print('Adding', arch_file_path, '... ', end='')
            self.add_arch_file(zipf, input_path, arch_file_path)
            print('done')
        zipf.close()

    def make_backup_output_files(self):
        _, backup_file_path = self._get_backup_archive_path(mode_suffix='output')
        print('Creating output backup file', backup_file_path)
        zipf = ZipFile(
            backup_file_path, 'w', compression=zipfile.ZIP_DEFLATED, allowZip64=True
        )
        for subdir_basename, subdir_extensions in self._subdirs.items():
            for input_path, subdir_extension in subdir_extensions:
                arch_file_path = os.path.join(
                    subdir_basename, 
                    '{}{}'.format(subdir_basename, subdir_extension)
                )
                # print('Adding', arch_file_path, '... ', end='')
                self.add_arch_file(zipf, input_path, arch_file_path)
                print('done')
        zipf.close()

    def copy_output_file(self, file_input_path, file_output_path):
        # shutil.copy2(file_input_path, file_output_path)
        #
        # TODO: stub
        with open(file_output_path, 'w') as wf:
            pass
        # TODO: stub


    def add_arch_file(self, zipfile, input_path, arch_file_path):
        zipfile.write(input_path, arch_file_path)


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

    def _get_backup_archive_path(self, mode_suffix='input'):
        os.stat_float_times(False)
        input_create_time_ts = os.stat(self.input_filelist[0]).st_ctime
        input_create_time = datetime.fromtimestamp(input_create_time_ts).strftime("%d_%m_%Y_%H_%M_%S")
        backup_file_base = 'run_{}_{}.zip'.format(input_create_time, mode_suffix)
        backup_file_path = os.path.join(self.backup_path, backup_file_base)
        return backup_file_base, backup_file_path

if __name__ == '__main__':
    olm = OutputLocationManager(
        input_path='C:\\Users\\Public\\Documents\\incoming\\bio-related\\biohackathon_input_path',
        output_path='C:\\Users\\Public\\Documents\\incoming\\bio-related\\biohackathon_output_path',
        backup_path='C:\\Users\\Public\\Documents\\incoming\\bio-related\\biohackathon_backup_path',
#         input_path='C:\\Users\\Public\\Documents\\incoming\\bio-related\\biohackathon_input_path_1',
#         output_path='C:\\Users\\Public\\Documents\\incoming\\bio-related\\biohackathon_output_path_1',
#         backup_path='C:\\Users\\Public\\Documents\\incoming\\bio-related\\biohackathon_backup_path_1',
    )
#     print('Number of samples')
#     print(olm.number_of_samples)
#     print('Creating output')
#     olm.make_output_files()
#     print('Creating backup')
#     olm.make_backup_output_files()
#     print('Number of samples')
#     print(olm.number_of_samples)
#     print('Preferred extensions:', olm.preferred_extensions)

#     print('New path')
# 
#     olm.set_input_path('C:\\Users\\Public\\Documents\\incoming\\bio-related\\biohackathon_input_path_1')
#     olm.set_output_path('C:\\Users\\Public\\Documents\\incoming\\bio-related\\biohackathon_output_path_1')
#     olm.set_backup_path('C:\\Users\\Public\\Documents\\incoming\\bio-related\\biohackathon_backup_path_1')
#     print('Number of samples')
#     print(olm.number_of_samples)
#     print('Creating output')
#     olm.make_output_files()
#     print('Creating backup')
#     olm.make_backup_output_files()
#     print('Number of samples')
#     print(olm.number_of_samples)
#     print('Preferred extensions:', olm.preferred_extensions)

    print('Creating backup')
    olm.make_backup_input_files()
