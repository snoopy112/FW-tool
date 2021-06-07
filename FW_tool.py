try:
    from PyQt5 import QtCore, QtWidgets
    from PyQt5.QtGui import QColor
    from os import mkdir, chdir, remove, rename, system, listdir, walk, stat
    from os.path import join, isdir
    from sys import exit, argv
    import re
    from hashlib import md5
    from shutil import rmtree, copyfile, copytree, make_archive

except Exception as e:
    print('Error:', e)
    system("pause")
    exit()


PATH_TO_FW = ''  # path by default

PLAYERS = {
    "AGPTEK Rocker / Benjie T6": "agptek",
    "Cayin N3": "ap",
    "Fiio M3 Pro": "m3pro",
    "Fiio M3K": "m3k",
    "Fiio M5": "m5",
    "HiBy R3": "r3",
    "HiBy R3 Pro": "r3pro",
    "Hidizs AP60 / AP80": "ap",
    "Shanling M0": "m0",
    "Shanling M1": "m1",
    "Shanling M2s": "m2s",
    "Shanling M2x": "m2x",
    "Shanling M3s": "m3s",
    "Shanling M5s": "m5s",
    "xDuoo X3 II": "x3ii",
    "xDuoo X20": "x20"
}

MODES = {
    "1. Unpacking": "unpack",
    "2. Optimizing": "optimize",
    "3. Packing": "repack",
}

RED = 250, 20, 20
GREEN = 20, 120, 20
BLUE = 20, 20, 180
CYAN = 20, 160, 160
GRAY = 120, 120, 120


class Ui_Form(object):

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(500, 500)

        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")


        self.horizontalLayout_1 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_1.setObjectName("horizontalLayout_1")

        self.mode = QtWidgets.QLabel(Form)
        self.mode.setObjectName("Mode")
        self.mode.setMinimumSize(QtCore.QSize(100, 0))

        self.modeComboBox = QtWidgets.QComboBox(Form)
        self.modeComboBox.setObjectName("modeComboBox")
        for _ in range(len(MODES)):
            self.modeComboBox.addItem("")
        self.verticalLayout.addWidget(self.modeComboBox)

        self.horizontalLayout_1.addWidget(self.mode)
        self.horizontalLayout_1.addWidget(self.modeComboBox)
        self.horizontalLayout_1.setAlignment(QtCore.Qt.AlignLeft)

        self.verticalLayout.addLayout(self.horizontalLayout_1)

        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")

        self.playerLabel = QtWidgets.QLabel(Form)
        self.playerLabel.setObjectName("Player")
        self.playerLabel.setMinimumSize(QtCore.QSize(100, 0))

        self.playerComboBox = QtWidgets.QComboBox(Form)
        self.playerComboBox.setObjectName("playerComboBox")
        for _ in range(len(PLAYERS)):
            self.playerComboBox.addItem("")
        self.verticalLayout.addWidget(self.playerComboBox)

        self.horizontalLayout_2.addWidget(self.playerLabel)
        self.horizontalLayout_2.addWidget(self.playerComboBox)
        self.horizontalLayout_2.setAlignment(QtCore.Qt.AlignLeft)

        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")

        self.pathToFW = QtWidgets.QLabel(Form)
        self.pathToFW.setObjectName("Path")
        self.pathToFW.setMinimumSize(QtCore.QSize(100, 0))

        self.pathToFWFolder = QtWidgets.QLineEdit(Form)
        self.pathToFWFolder.setObjectName("pathToFWFolder")
        self.pathToFWFolder.setPlaceholderText('Path to FW file')

        self.horizontalLayout_3.addWidget(self.pathToFW)
        self.horizontalLayout_3.addWidget(self.pathToFWFolder)
        self.horizontalLayout_3.setAlignment(QtCore.Qt.AlignLeft)

        self.verticalLayout.addLayout(self.horizontalLayout_3)


        self.textBrowser = QtWidgets.QTextBrowser(Form)
        self.textBrowser.setObjectName("textBrowser")
        self.verticalLayout.addWidget(self.textBrowser)

        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")

        spacerItem = QtWidgets.QSpacerItem(0, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)

        self.pushButtonInfo = QtWidgets.QPushButton(Form)
        self.pushButtonInfo.setObjectName("pushButton")
        self.horizontalLayout_4.addWidget(self.pushButtonInfo)

        self.pushButtonStart = QtWidgets.QPushButton(Form)
        self.pushButtonStart.setObjectName("pushButton")
        self.horizontalLayout_4.addWidget(self.pushButtonStart)

        self.pushButtonClear = QtWidgets.QPushButton(Form)
        self.pushButtonClear.setObjectName("pushButtonClear")
        self.horizontalLayout_4.addWidget(self.pushButtonClear)

        self.horizontalLayout_4.addItem(spacerItem)

        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "FW Tool"))
        self.mode.setText(_translate("Form", "Mode:"))
        for i, mode in enumerate(sorted(MODES.keys(), reverse=False)):
            self.modeComboBox.setItemText(i, _translate("Form", mode))

        self.playerLabel.setText(_translate("Form", "Player:"))
        for i, player in enumerate(sorted(PLAYERS.keys())):
            self.playerComboBox.setItemText(i, _translate("Form", player))

        self.pathToFW.setText(_translate("Form", "Path to FW file:"))

        self.pathToFWFolder.setText(_translate("Form", PATH_TO_FW))

        self.pushButtonInfo.setText(_translate("Form", "Info"))
        self.pushButtonStart.setText(_translate("Form", "Start"))
        self.pushButtonClear.setText(_translate("Form", "Clear"))


class BrowserHandler(QtCore.QObject):

    newTextAndColor = QtCore.pyqtSignal(str, object)

    def info(self, **kwargs):
        self.newTextAndColor.emit('Tool for unpack, optimize and repack firmware for music', QColor(*GRAY))
        self.newTextAndColor.emit('players based on Hiby OS, MTouch and Fiio system (non-Android)\n', QColor(*GRAY))
        self.newTextAndColor.emit('Supported players:', QColor(*GRAY))
        self.newTextAndColor.emit('- AGPTEK Rocker / Benjie T6', QColor(*GRAY))
        self.newTextAndColor.emit('- Cayin N3', QColor(*GRAY))
        self.newTextAndColor.emit('- Fiio M3 Pro (not tested)', QColor(*GRAY))
        self.newTextAndColor.emit('- Fiio M3K (not tested)', QColor(*GRAY))
        self.newTextAndColor.emit('- Fiio M5 (not tested)', QColor(*GRAY))
        self.newTextAndColor.emit('- HiBy R3', QColor(*GRAY))
        self.newTextAndColor.emit('- HiBy R3 Pro', QColor(*GRAY))
        self.newTextAndColor.emit('- Hidizs AP60 / AP80', QColor(*GRAY))
        self.newTextAndColor.emit('- Shanling M0 (not tested)', QColor(*GRAY))
        self.newTextAndColor.emit('- Shanling M1', QColor(*GRAY))
        self.newTextAndColor.emit('- Shanling M2s', QColor(*GRAY))
        self.newTextAndColor.emit('- Shanling M2x (not tested)', QColor(*GRAY))
        self.newTextAndColor.emit('- Shanling M3s', QColor(*GRAY))
        self.newTextAndColor.emit('- Shanling M5s (not tested)', QColor(*GRAY))
        self.newTextAndColor.emit('- xDuoo X3 II', QColor(*GRAY))
        self.newTextAndColor.emit('- xDuoo X20\n', QColor(*GRAY))
        self.newTextAndColor.emit('WARNING:', QColor(*GRAY))
        self.newTextAndColor.emit('All modifications are use at your own risk. I can\'t be', QColor(*GRAY))
        self.newTextAndColor.emit('sure the modified FW will not brick your device,', QColor(*GRAY))
        self.newTextAndColor.emit('especially the players marked as "not tested".\n', QColor(*GRAY))
        self.newTextAndColor.emit('NOTE:', QColor(*GRAY))
        self.newTextAndColor.emit('First of all you should to choose your player model, path', QColor(*GRAY))
        self.newTextAndColor.emit('to *.upt, *.bin or *.fw update file and mode in the head', QColor(*GRAY))
        self.newTextAndColor.emit('of program.\n', QColor(*GRAY))
        self.newTextAndColor.emit('DEPENDENCIES:', QColor(*GRAY))
        self.newTextAndColor.emit('Linux-based system', QColor(*GRAY))
        self.newTextAndColor.emit('Python >= 3.5', QColor(*GRAY))
        self.newTextAndColor.emit('Install modules with bash:', QColor(*GRAY))
        self.newTextAndColor.emit('# sudo apt-get install liblzo2-dev', QColor(*GRAY))
        self.newTextAndColor.emit('# sudo apt-get install optipng', QColor(*GRAY))
        self.newTextAndColor.emit('# sudo apt-get install gcc-mipsel-linux-gnu', QColor(*GRAY))
        self.newTextAndColor.emit('# sudo apt install mtd-utils', QColor(*GRAY))
        self.newTextAndColor.emit('# pip3 install pycdlib', QColor(*GRAY))
        self.newTextAndColor.emit('# pip3 install python-lzo', QColor(*GRAY))
        self.newTextAndColor.emit('# pip3 install ubi_reader\n', QColor(*GRAY))

    def unpack(self, player_name: str, path_to_fw: str):
        '''
        Unpack *.upt or *.bin file from /Firmware folder
        to /system and /player folders

        Make sure the PyCdlib, UBI Reader and dependencies have been installed:
        # pip3 install pycdlib
        # sudo apt-get install liblzo2-dev
        # pip3 install python-lzo
        # pip3 install ubi_reader
        '''
        self.newTextAndColor.emit(self.unpack.__doc__, QColor(*GRAY))

        try:
            from ubireader.ubifs import ubifs
            from ubireader.ubi_io import ubi_file
            from ubireader.ubifs.output import extract_files
        except:
            self.newTextAndColor.emit('[ERROR]: Please install UBI Reader and dependencies to use this mode:', QColor(*RED))
            #self.newTextAndColor.emit('[INFO]: For Windows try to install python-lzo from https://www.lfd.uci.edu/~gohlke/pythonlibs/#python-lzo', QColor(*BLUE))
            self.newTextAndColor.emit('[ERROR]: # sudo apt-get install liblzo2-dev', QColor(*RED))
            self.newTextAndColor.emit('[ERROR]: # pip3 install python-lzo', QColor(*RED))
            self.newTextAndColor.emit('[ERROR]: # pip3 install ubi_reader', QColor(*RED))
            return

        if isdir(path_to_fw):
            try:
                rmtree(join(path_to_fw, 'system'))
                rmtree(join(path_to_fw, player_name))
                mkdir(join(path_to_fw, player_name))
                mkdir(join(path_to_fw, 'system'))
            except OSError:
                mkdir(join(path_to_fw, player_name))
                mkdir(join(path_to_fw, 'system'))
        else:
            self.newTextAndColor.emit('[ERROR]: Selected path doesn\'t exist...', QColor(*RED))
            return

        if player_name in ('agptek', 'ap', 'm1', 'm2s', 'm3s', 'n3', 'r3', 'r3pro', 'x3ii', 'x20'):
            if player_name in ('r3', 'r3pro'):
                upt_file = '{}.upt'.format(player_name)
            else:
                upt_file = 'update.upt'

            try:
                import pycdlib
            except:
                self.newTextAndColor.emit('[ERROR]: Please install PyCdlib to use this mode:', QColor(*RED))
                self.newTextAndColor.emit('[ERROR]: # pip3 install pycdlib', QColor(*RED))
                return

            try:
                iso = pycdlib.PyCdlib()
                iso.open(join(path_to_fw, upt_file))
                self.newTextAndColor.emit('[INFO]: Extracting {} file:'.format(upt_file), QColor(*BLUE))
            except FileNotFoundError:
                self.newTextAndColor.emit('[ERROR]: Can\'t find {} file'.format(upt_file), QColor(*RED))
                return

            for child in iso.list_children(iso_path='/'):
                if child.is_file():
                    iso_file = join(path_to_fw, player_name, child.file_identifier().decode('UTF-8')[:-2])
                    self.newTextAndColor.emit(iso_file, QColor(*GREEN))
                    iso.get_file_from_iso(iso_path='/'+child.file_identifier().decode('UTF-8'), local_path=join(path_to_fw, player_name, iso_file))
                else:
                    continue

            iso.close()

            self.newTextAndColor.emit('[INFO]: Info about SYSTEM.UBI file:', QColor(*BLUE))
            block_size = 0
            ufile_obj = ubi_file(join(path_to_fw, player_name, 'SYSTEM.UBI'), block_size)
            ubifs_obj = ubifs(ufile_obj)

            self.newTextAndColor.emit(ubifs_obj.display(), QColor(*GREEN))
            self.newTextAndColor.emit(ubifs_obj.superblock_node.display('\t')[:301], QColor(*GREEN))

            self.newTextAndColor.emit('[INFO]: Extracting SYSTEM.UBI file to /system folder', QColor(*BLUE))
            extract_files(ubifs_obj, join(path_to_fw, 'system'), '-k')

            self.newTextAndColor.emit('[INFO]: Rename original update file to: {}_orig.upt'.format(upt_file), QColor(*BLUE))
            rename(join(path_to_fw, upt_file), join(path_to_fw, '{}_orig.{}'.format(upt_file.split('.')[0], upt_file.split('.')[1])))


        elif player_name in ('m0', 'm2x', 'm5s', 'm3k', 'm3pro', 'm5'):
            if player_name in ('m0', 'm3k', 'm3pro', 'm5'):
                system_file_prefix = ''
            else:
                system_file_prefix = player_name

            try:
                from zipfile import ZipFile
            except:
                self.newTextAndColor.emit('[ERROR]: Can\'t import zipfile module...', QColor(*RED))
                return

            try:
                from tarfile import TarFile
            except:
                self.newTextAndColor.emit('[ERROR]: Can\'t import tarfile module...', QColor(*RED))
                return

            try:
                rmtree(join(path_to_fw, player_name, 'ubi'))
                mkdir(join(path_to_fw, player_name, 'ubi'))
            except OSError:
                mkdir(join(path_to_fw, player_name, 'ubi'))

            if player_name in ('m0', 'm2x', 'm5s'):
                upt_file = 'update.bin'

                try:
                    with TarFile(join(path_to_fw, upt_file), 'r') as tar:
                        self.newTextAndColor.emit('[INFO]: Extracting {} file'.format(upt_file), QColor(*BLUE))
                        # self.newTextAndColor.emit(tar.getnames(), QColor(*GREEN))
                        tar.extractall(path=join(path_to_fw, player_name))
                except FileNotFoundError:
                    self.newTextAndColor.emit('[ERROR]: Can\'t find {} file'.format(upt_file), QColor(*RED))
                    return


                self.newTextAndColor.emit('[INFO]: Extracting firmware_v0.tar.gz', QColor(*BLUE))
                with TarFile(join(path_to_fw, player_name, 'firmware_v0.tar.gz'), 'r') as tar:
                    # self.newTextAndColor.emit(tar.getnames(), QColor(*GREEN))
                    tar.extractall(path=join(path_to_fw, player_name))

            else:
                if player_name in ('m3k'):
                    upt_file = 'M3K.fw'
                elif player_name in ('m3pro'):
                    upt_file = 'M3Pro.zip'
                elif player_name in ('m5'):
                    upt_file = 'M5.zip'
                else:
                    pass

                try:
                    with ZipFile(join(path_to_fw, upt_file)) as z:
                        self.newTextAndColor.emit('[INFO]: Extracting {} file'.format(upt_file), QColor(*BLUE))
                        z.extractall(path=join(path_to_fw, player_name))
                except FileNotFoundError:
                    self.newTextAndColor.emit('[ERROR]: Can\'t find or extract {} file'.format(upt_file), QColor(*RED))
                    return


            zip_files_len = len(listdir(join(path_to_fw, player_name, 'recovery-update', 'nand')))
            # self.newTextAndColor.emit(zip_files_len, QColor(*GREEN))

            self.newTextAndColor.emit('[INFO]: Extracting update.xml file from /recovery-update to /ubi', QColor(*BLUE))
            with ZipFile(join(path_to_fw, player_name, 'recovery-update', 'nand', 'update000.zip'), 'r') as z:
                # self.newTextAndColor.emit(z.printdir(), QColor(*GREEN))
                z.extract('update000/update.xml', path=join(path_to_fw, player_name, 'ubi'))

            rename(join(path_to_fw, player_name, 'ubi', 'update000', 'update.xml'), join(path_to_fw, player_name, 'ubi', 'update.xml'))
            rmtree(join(path_to_fw, player_name, 'ubi', 'update000'))

            self.newTextAndColor.emit('[INFO]: Extracting {}system.ubi_### parts files from /recovery-update to /ubi:'.format(system_file_prefix), QColor(*BLUE))
            unzip = 1
            for i in range(1, zip_files_len):
                with ZipFile(join(path_to_fw, player_name, 'recovery-update', 'nand', 'update{0:0>3}.zip'.format(str(i))), 'r') as z:
                    # self.newTextAndColor.emit(z.printdir(), QColor(*GREEN))
                    if 'update{0:0>3}/{2}system.ubi_{1:0>3}'.format(str(i), str(unzip), system_file_prefix) in z.namelist():
                        self.newTextAndColor.emit(join(path_to_fw, player_name, 'ubi', '{1}system.ubi_{0:0>3}'.format(str(unzip), system_file_prefix)), QColor(*GREEN))
                        z.extract('update{0:0>3}/{2}system.ubi_{1:0>3}'.format(str(i), str(unzip), system_file_prefix), path=join(path_to_fw, player_name, 'ubi'))

                        rename(join(path_to_fw, player_name, 'ubi', 'update{0:0>3}'.format(str(i)), '{1}system.ubi_{0:0>3}'.format(str(unzip), system_file_prefix)), join(path_to_fw, player_name, 'ubi', '{1}system.ubi_{0:0>3}'.format(str(unzip), system_file_prefix)))
                        rmtree(join(path_to_fw, player_name, 'ubi', 'update{0:0>3}'.format(str(i))))
                        unzip += 1


            ubi_list_paths = []
            for root, dirs, files in walk(join(path_to_fw, player_name, 'ubi')):
                for file in files:
                    if file.startswith('{}system.ubi_'.format(system_file_prefix)):
                        ubi_list_paths.append(join(root, file))

            # self.newTextAndColor.emit(ubi_list_paths, QColor(*GREEN))

            self.newTextAndColor.emit('[INFO]: Concatenate all {0}system.ubi_* files to {0}system.ubi'.format(system_file_prefix), QColor(*BLUE))
            out_data = b''
            for fn in sorted(ubi_list_paths):
                with open(str(fn), 'rb') as fp:
                    out_data += fp.read()
            with open(join(path_to_fw, player_name, '{}system.ubi'.format(system_file_prefix)), 'wb') as fp:
                fp.write(out_data)

            self.newTextAndColor.emit('[INFO]: Info about {}system.ubi file:'.format(system_file_prefix), QColor(*BLUE))
            block_size = 0
            ufile_obj = ubi_file(join(path_to_fw, player_name, '{}system.ubi'.format(system_file_prefix)), block_size)
            ubifs_obj = ubifs(ufile_obj)

            self.newTextAndColor.emit(ubifs_obj.display(), QColor(*GREEN))
            self.newTextAndColor.emit(ubifs_obj.superblock_node.display('\t')[:301], QColor(*GREEN))

            self.newTextAndColor.emit('[INFO]: Extracting {}system.ubi file to /system folder'.format(system_file_prefix), QColor(*BLUE))
            extract_files(ubifs_obj, join(path_to_fw, 'system'), '-k')

            self.newTextAndColor.emit('[INFO]: Rename original update file', QColor(*BLUE))
            rename(join(path_to_fw, upt_file), join(path_to_fw, '{}_orig.{}'.format(upt_file.split('.')[0], upt_file.split('.')[1])))


        else:
            self.newTextAndColor.emit('[ERROR]: Unknown player name: {}'.format(player_name), QColor(*RED))
            return

        self.newTextAndColor.emit('[INFO]: Firmware unpacked. Done!', QColor(*BLUE))


    def optimize(self, path_to_fw: str, **kwargs):
        '''
        Optimize binary (strip) and *.png files in system folder

        Make sure the OptiPNG and GNU toolchain for the MIPS architecture have been installed:
        # sudo apt-get install optipng
        # sudo apt-get install gcc-mipsel-linux-gnu
        '''
        self.newTextAndColor.emit(self.optimize.__doc__, QColor(*GRAY))

        if isdir(join(path_to_fw, 'system')):
            self.newTextAndColor.emit('[INFO]: Start optimizing all *.png files', QColor(*BLUE))
            command = 'find "{}" -name "*.png" -print0 | xargs -0 optipng -o2 -strip all -force'.format(join(path_to_fw, 'system'))
            # print(command)
            system(command)

            self.newTextAndColor.emit('[INFO]: Start striping all binary files', QColor(*BLUE))
            command = 'find "{}" -type f -exec mipsel-linux-gnu-strip --strip-unneeded {{}} \;'.format(join(path_to_fw, 'system'))
            # print(command)
            system(command)

            self.newTextAndColor.emit('[INFO]: Optimization finished. Done!', QColor(*BLUE))
        else:
            self.newTextAndColor.emit('[ERROR]: Can\'t find system folder...', QColor(*RED))


    def repack(self, player_name: str, path_to_fw: str):
        '''
        Repack system folder to *.upt or *.bin firmware update file.

        Make sure the MTD Utilities has been installed:
        # sudo apt install mtd-utils
        '''
        self.newTextAndColor.emit(self.repack.__doc__, QColor(*GRAY))

        if player_name in ('agptek', 'ap', 'm1', 'm2s', 'm3s', 'n3', 'r3', 'r3pro', 'x3ii', 'x20'):
            if player_name in ('r3', 'r3pro'):
                upt_file = '{}.upt'.format(player_name)
                LEB = 126976
                PEB = 2048
                MAX_LEB_CNT = 480
            else:
                upt_file = 'update.upt'
                LEB = 126976
                PEB = 2048
                MAX_LEB_CNT = 1024

            try:
                import pycdlib
            except:
                self.newTextAndColor.emit('[ERROR]: Please install PyCdlib to use this mode:', QColor(*RED))
                self.newTextAndColor.emit('[ERROR]: # pip3 install pycdlib', QColor(*RED))
                return

            def create_upt_file(player_name, path_to_fw, upt_file):
                iso = pycdlib.PyCdlib()
                iso.new()

                for (dirpath, dirnames, filenames) in walk(join(path_to_fw, player_name)):
                    for name in filenames:
                        self.newTextAndColor.emit(join(dirpath, name), QColor(*GREEN))
                        iso.add_file(join(path_to_fw, player_name, name), '/{};1'.format(name))

                iso.write(join(path_to_fw, upt_file))
                iso.close()

            self.newTextAndColor.emit('[INFO]: Packing /system folder to SYSTEM.UBI file', QColor(*BLUE))
            bash_command = 'mkfs.ubifs -r "{0}" -m {1} -e {2} -c {3} -o "{4}"'.format(join(path_to_fw, 'system'), PEB, LEB, MAX_LEB_CNT, join(path_to_fw, player_name, 'SYSTEM.UBI'))
            # print(bash_command)
            system(bash_command)

            try:
                with open(join(path_to_fw, player_name, 'SYSTEM.UBI'), 'rb') as system_ubi:
                    md5_sum = md5(system_ubi.read()).hexdigest()
                self.newTextAndColor.emit('[INFO]: MD5 = {}'.format(md5_sum), QColor(*BLUE))
            except FileNotFoundError:
                self.newTextAndColor.emit('[ERROR]: Can\'t find SYSTEM.UBI file', QColor(*RED))
                return

            self.newTextAndColor.emit('[INFO]: Edit MD5 in UPDATE.TXT file', QColor(*BLUE))
            try:
                with open(join(path_to_fw, player_name, 'UPDATE.TXT'), 'r') as update_read:
                    update_text = update_read.read()
                    find_md5 = re.search(r'rootfs={.+md5=([0-9a-zA-Z]+).+}', update_text, flags=re.DOTALL)
                    update_text = re.sub(find_md5.group(1), md5_sum, update_text)
                    self.newTextAndColor.emit(update_text, QColor(*GREEN))
                with open(join(path_to_fw, player_name, 'UPDATE.TXT'), 'w') as update_write:
                    update_write.write(update_text)
            except FileNotFoundError:
                self.newTextAndColor.emit('[ERROR]: Can\'t find or rewrite UPDATE.TXT file', QColor(*RED))
                return

            if player_name == 'r3':
                self.newTextAndColor.emit('[INFO]: Change version of firmware to International', QColor(*BLUE))
                with open(join(path_to_fw, player_name, 'VERSION.TXT'), 'r') as version_read:
                    version_text = version_read.read()
                    version_text = version_text.replace('r3_cn', 'r3')
                    self.newTextAndColor.emit(version_text, QColor(*GREEN))
                with open(join(path_to_fw, player_name, 'VERSION.TXT'), 'w') as version_write:
                    version_write.write(version_text)

                self.newTextAndColor.emit('[INFO]: Packing firmware update files to {}'.format(upt_file), QColor(*BLUE))
                create_upt_file(player_name, path_to_fw, upt_file)

                self.newTextAndColor.emit('[INFO]: Change version of firmware to China', QColor(*BLUE))
                with open(join(path_to_fw, player_name, 'VERSION.TXT'), 'r') as version_read:
                    version_text = version_read.read()
                    version_text = version_text.replace('r3', 'r3_cn')
                    self.newTextAndColor.emit(version_text, QColor(*GREEN))
                with open(join(path_to_fw, player_name, 'VERSION.TXT'), 'w') as version_write:
                    version_write.write(version_text)

                upt_file = '{}_cn.upt'.format(upt_file.split('.')[0])
                self.newTextAndColor.emit('[INFO]: Packing firmware update files to {}'.format(upt_file), QColor(*BLUE))
                create_upt_file(player_name, path_to_fw, upt_file)
            else:
                self.newTextAndColor.emit('[INFO]: Packing firmware update files to {}'.format(upt_file), QColor(*BLUE))
                create_upt_file(player_name, path_to_fw, upt_file)


        elif player_name in ('m0', 'm2x', 'm5s', 'm3k', 'm3pro', 'm5'):
            if player_name in ('m0', 'm2x', 'm5s'):
                LEB = 126976
                PEB = 2048
                MAX_LEB_CNT = 720
            elif player_name in ('m3k', 'm3pro', 'm5'):
                LEB = 126976
                PEB = 2048
                MAX_LEB_CNT = 2048
            else:
                pass

            if player_name in ('m0', 'm2x', 'm5s'):
                upt_file = 'update.bin'
            elif player_name in ('m3k'):
                upt_file = 'M3K.fw'
            elif player_name in ('m3pro'):
                upt_file = 'M3Pro.zip'
            elif player_name in ('m5'):
                upt_file = 'M5.zip'
            else:
                pass

            if player_name in ('m0', 'm3k', 'm3pro', 'm5'):
                system_file_prefix = ''
            else:
                system_file_prefix = player_name

            try:
                from zipfile import ZipFile, ZIP_DEFLATED
            except:
                self.newTextAndColor.emit('[ERROR]: Can\'t import zipfile module...', QColor(*RED))
                return

            try:
                from tarfile import TarFile
            except:
                self.newTextAndColor.emit('[ERROR]: Can\'t import tarfile module...', QColor(*RED))
                return

            try:
                mkdir(join(path_to_fw, player_name, 'ubi_temp'))
            except :
                self.newTextAndColor.emit('[ERROR]: Can\'t find path folder', QColor(*RED))
                return

            copyfile(join(path_to_fw, player_name, 'ubi', 'update.xml'), (join(path_to_fw, player_name, 'ubi_temp', 'update.xml')))
            copytree(join(path_to_fw, player_name, 'recovery-update'), join(path_to_fw, player_name, 'recovery-update_temp'))

            self.newTextAndColor.emit('[INFO]: Packing /system folder to {}system.ubi file'.format(system_file_prefix), QColor(*BLUE))
            bash_command = 'mkfs.ubifs -r "{0}" -m {1} -e {2} -c {3} -o "{4}"'.format(join(path_to_fw, 'system'), PEB, LEB, MAX_LEB_CNT, join(path_to_fw, player_name, '{}system.ubi'.format(system_file_prefix)))
            # print(bash_command)
            system(bash_command)

            self.newTextAndColor.emit('[INFO]: Split {0}system.ubi into {0}system.ubi_* files to /ubi_temp folder'.format(system_file_prefix), QColor(*BLUE))
            PART_SIZE = 1015808
            file_number = 1

            with open(join(path_to_fw, player_name, '{}system.ubi'.format(system_file_prefix)), 'rb') as system_ubi:
                part = system_ubi.read(PART_SIZE)
                while part:
                    with open(join(path_to_fw, player_name, 'ubi_temp', '{1}system.ubi_{0:0>3}'.format(str(file_number), system_file_prefix)), 'wb') as system_part:
                        system_part.write(part)
                        file_number += 1
                        part = system_ubi.read(PART_SIZE)

            md5_sum = md5(open(join(path_to_fw, player_name, '{}system.ubi'.format(system_file_prefix)), 'rb').read()).hexdigest()
            self.newTextAndColor.emit('[INFO]: MD5 = {}'.format(md5_sum), QColor(*BLUE))

            update_size = stat(join(path_to_fw, player_name, '{}system.ubi'.format(system_file_prefix))).st_size
            self.newTextAndColor.emit('[INFO]: Size of UBI file = {} bytes'. format(str(update_size)), QColor(*BLUE))

            zip_files_len = len(listdir(join(path_to_fw, player_name, 'ubi_temp'))) - 1
            self.newTextAndColor.emit('[INFO]: Number of UBI parts = {}'.format(str(zip_files_len)), QColor(*BLUE))

            self.newTextAndColor.emit('[INFO]: Edit size of {}system.ubi and number of parts in update.xml file'.format(system_file_prefix), QColor(*BLUE))
            with open(join(path_to_fw, player_name, 'ubi_temp', 'update.xml'), 'r') as update_read:
                update_text = update_read.read()
                find_size = re.search(r'<image><name type="opaque">{}system.ubi</name>.+<size>([0-9]+)</size>'.format(system_file_prefix), update_text)
                update_text = re.sub(find_size.group(1), str(update_size), update_text)
                find_ubi_parts = re.search('{}.+<chunkcount type="integer">([0-9]+)</chunkcount>'.format(str(update_size)), update_text)
                update_text = re.sub(find_ubi_parts.group(1), str(zip_files_len), update_text)
                # self.newTextAndColor.emit(update_text, QColor(*GREEN))

            with open(join(path_to_fw, player_name, 'ubi_temp', 'update.xml'), 'w') as update_write:
                update_write.write(update_text)

            if player_name in ('m0', 'm2x', 'm5s'):
                self.newTextAndColor.emit('[INFO]: Edit MD5 in firmware_v0.info file', QColor(*BLUE))
                with open(join(path_to_fw, player_name, 'firmware_v0.info'), 'r') as update_read:
                    update_text = update_read.read()
                    find_md5 = re.search(r'([a-zA-Z0-9]{32})', update_text)
                    update_text = re.sub(find_md5.group(1), md5_sum, update_text)
                    # self.newTextAndColor.emit(update_text, QColor(*GREEN))

                with open(join(path_to_fw, player_name, 'firmware_v0.info'), 'w') as update_write:
                    update_write.write(update_text)


            self.newTextAndColor.emit('[INFO]: Updating update###.zip parts files:', QColor(*BLUE))
            unzip_count = 1
            for i in range(1, len(listdir(join(path_to_fw, player_name, 'recovery-update_temp', 'nand')))):
                with ZipFile(join(path_to_fw, player_name, 'recovery-update_temp', 'nand', 'update{0:0>3}.zip'.format(str(i))), 'r') as z:
                    # self.newTextAndColor.emit(z.printdir(), QColor(*GREEN))
                    if 'update{0:0>3}/{2}system.ubi_{1:0>3}'.format(str(i), str(unzip_count), system_file_prefix) in z.namelist():
                        self.newTextAndColor.emit(join(path_to_fw, player_name, 'recovery-update_temp', 'nand', 'update{0:0>3}.zip'.format(str(i))), QColor(*GREEN))
                        z.extractall(join(path_to_fw, player_name, 'recovery-update_temp', 'nand', 'update'))
                        remove(join(path_to_fw, player_name, 'recovery-update_temp', 'nand', 'update', 'update{0:0>3}'.format(str(i)), '{1}system.ubi_{0:0>3}'.format(str(unzip_count), system_file_prefix)))
                        try:
                            copyfile(join(path_to_fw, player_name, 'ubi_temp', '{1}system.ubi_{0:0>3}'.format(str(unzip_count), system_file_prefix)), join(path_to_fw, player_name, 'recovery-update_temp', 'nand', 'update', 'update{0:0>3}'.format(str(i)), '{1}system.ubi_{0:0>3}'.format(str(unzip_count), system_file_prefix)))

                            chdir(join(path_to_fw, player_name, 'recovery-update_temp', 'nand'))
                            make_archive('update{0:0>3}'.format(str(i)), 'zip', join(path_to_fw, player_name, 'recovery-update_temp', 'nand', 'update'))
                            rmtree(join(path_to_fw, player_name, 'recovery-update_temp', 'nand', 'update'))
                        except IOError:
                            remove(join(path_to_fw, player_name, 'recovery-update_temp', 'nand', 'update{0:0>3}.zip'.format(str(i))))
                            rmtree(join(path_to_fw, player_name, 'recovery-update_temp', 'nand', 'update'))
                        unzip_count += 1
                    else:
                        #self.newTextAndColor.emit('Nothing to change...', QColor(*GREEN))
                        pass

            with ZipFile(join(path_to_fw, player_name, 'recovery-update_temp', 'nand', 'update000.zip'), 'r') as z:
                # self.newTextAndColor.emit(z.printdir(), QColor(*GREEN))
                self.newTextAndColor.emit('[INFO]: Change update.xml file', QColor(*BLUE))
                z.extractall(join(path_to_fw, player_name, 'recovery-update_temp', 'nand', 'update'))
                remove(join(path_to_fw, player_name, 'recovery-update_temp', 'nand', 'update', 'update000', 'update.xml'))
                copyfile(join(path_to_fw, player_name, 'ubi_temp', 'update.xml'), join(path_to_fw, player_name, 'recovery-update_temp', 'nand', 'update', 'update000', 'update.xml'))

            chdir(join(path_to_fw, player_name, 'recovery-update_temp', 'nand'))
            make_archive('update000', 'zip', join(path_to_fw, player_name, 'recovery-update_temp', 'nand', 'update'))
            rmtree(join(path_to_fw, player_name, 'recovery-update_temp', 'nand', 'update'))

            if player_name in ('m0', 'm2x', 'm5s'):
                self.newTextAndColor.emit('[INFO]: Packing /recovery-update_temp folder to firmware_v0.tar.gz', QColor(*BLUE))
                with TarFile.open(join(path_to_fw, player_name, 'firmware_v0.tar.gz'), 'w') as tar:
                    tar.add(join(path_to_fw, player_name, 'recovery-update_temp'), arcname='recovery-update')

                self.newTextAndColor.emit('[INFO]: Packing firmware update files to update.bin', QColor(*BLUE))
                with TarFile.open(join(path_to_fw, upt_file), 'w') as tar:
                    tar.add(join(path_to_fw, player_name, 'firmware_v0.info'), arcname='firmware_v0.info')
                    tar.add(join(path_to_fw, player_name, 'firmware_v0.tar.gz'), arcname='firmware_v0.tar.gz')

            elif player_name in ('m3k', 'm3pro', 'm5'):
                chdir(join(path_to_fw, player_name))
                with ZipFile(join(path_to_fw, upt_file), 'w', ZIP_DEFLATED) as z:
                    for dirname, _, files in walk('recovery-update_temp'):
                        for filename in files:
                            z.write(join(dirname, filename), arcname=join('recovery-update', dirname[len('recovery-update_temp')+1:], filename))

            else:
                pass

            self.newTextAndColor.emit('[INFO]: Delete temporary folders', QColor(*BLUE))
            rmtree(join(path_to_fw, player_name, 'recovery-update_temp'))
            rmtree(join(path_to_fw, player_name, 'ubi_temp'))

            self.newTextAndColor.emit('[ATTENTION]: The created firmware file is not signed and may cause the player failure!', QColor(*RED))

        else:
            self.newTextAndColor.emit('[ERROR]: Sorry, this mode for this player is under development...', QColor(*RED))
            return

        self.newTextAndColor.emit('[INFO]: Firmware repacked. Done!', QColor(*BLUE))


    def run(self):
        self.newTextAndColor.emit('---Start---', QColor(*CYAN))

        mode = window.ui.modeComboBox.currentText()
        # mode_ind = window.ui.modeComboBox.currentIndex()
        player = window.ui.playerComboBox.currentText()
        # player_ind = window.ui.playerComboBox.currentIndex()
        path = window.ui.pathToFWFolder.displayText()

        player = PLAYERS[player]

        while path.endswith(('\\', '/', ' ')):
            path = path[:-1]

        mode = MODES[mode]
        func = getattr(self, mode)
        func(player_name=player, path_to_fw=path)

        self.newTextAndColor.emit('----End----', QColor(*CYAN))


class MyWindow(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.thread = QtCore.QThread()

        self.browserHandler = BrowserHandler()
        self.browserHandler.moveToThread(self.thread)
        self.browserHandler.newTextAndColor.connect(self.addNewTextAndColor)

        self.ui.pushButtonInfo.clicked.connect(self.browserHandler.info)
        self.ui.pushButtonStart.clicked.connect(self.browserHandler.run)
        self.ui.pushButtonClear.clicked.connect(self.clearBrowser)

        self.thread.start()

    @QtCore.pyqtSlot(str, object)
    def addNewTextAndColor(self, string, color):
        self.ui.textBrowser.setTextColor(color)
        self.ui.textBrowser.append(string)

    @QtCore.pyqtSlot()
    def clearBrowser(self):
        self.ui.textBrowser.clear()


if __name__ == '__main__':
    app = QtWidgets.QApplication(argv)
    window = MyWindow()
    window.show()
    exit(app.exec())
