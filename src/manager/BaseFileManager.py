#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   BaseFileManager.py
@Author  :   Billy Zhou
@Time    :   2021/08/20
@Desc    :   None
'''


import sys
from pathlib import Path
cwdPath = Path(__file__).parents[2]
sys.path.append(str(cwdPath))

from src.manager.Logger import logger  # noqa: E402
log = logger.get_logger(__name__)

import yaml
from src.basic.input_check import input_checking_list  # noqa: E402


class BaseFileManager:
    """manage the operation on conf_file"""
    def __init__(self, conf_path: Path = cwdPath.joinpath('conf'), conf_filename: str = 'settings.yaml'):
        self._conf_path = Path(conf_path)
        self._conf_filename = conf_filename
        self._conf_file = Path(self._conf_path).joinpath(self._conf_filename)
        self.conf_dict = {}

        self._cwd = Path(__file__).parents[2]
        self._default_path = {
            'path': {
                'confpath': str(self._cwd),
            },
        }

        # check conf_path and check conf_file
        self._check_conffile()

        # Update according to conf_dict
        self._write_conf()

        log.debug('BaseFileManager inited')

    def _check_path(self, uncheck_path: Path) -> Path:
        checked_path = uncheck_path
        # check inputed path and is_dir() and exists()
        log.debug("conf_path before checked: %s", checked_path)
        if checked_path == Path('') or str(checked_path) == '.':
            checked_path = self._cwd
            log.debug('Blank inputed path. Using the default path[{0}]'.format(self._cwd))
        if not Path(checked_path).exists():
            Path(checked_path).mkdir(parents=True)
            log.warning("The path[{0}] not existed. Creating.".format(checked_path))
        log.debug("conf_path after checked: %s", checked_path)
        return Path(checked_path)

    def _check_conffile(self) -> None:
        # check _conf_file exists or not
        if not self._conf_file.exists():
            # check conf_path and update confpath in conf_dict
            self._conf_path = self._check_path(self._conf_path)
            self._conf_file = self._conf_path.joinpath(self._conf_filename)
        # check _conf_file exists or not after checked
        if not self._conf_file.exists():
            # still missing
            if not self.conf_dict.get('path'):
                self.conf_dict['path'] = {}
                log.info('The configuration missing the session[part]')
                log.info('Adding with the blank value')
            self.conf_dict['path']['confpath'] = str(self._conf_path)
        else:
            # read conf_dict and check the path in conf_dict
            self.conf_dict = self.read_conf()
            if not self.conf_dict.get('path'):
                self.conf_dict['path'] = {}
                log.info('The configuration missing the session[part]')
                log.info('Adding with the blank value')
            for key, value in self._default_path['path'].items():
                if not self.conf_dict['path'].get(key):
                    self.conf_dict['path'][key] = value
                    log.info('The configuration missing the part[{0}]'.format(key))
                    log.info('Adding with the default value[{0}]'.format(value))
                else:
                    if key == 'confpath':
                        if self._conf_path == Path('') or str(self._conf_path) == '.':
                            self._conf_path = self._cwd
                            log.debug('Blank inputed path. Using the default path[{0}]'.format(self._conf_path))
                        if Path(self.conf_dict['path']['confpath']) != Path(self._conf_path):
                            self.conf_dict['path']['confpath'] = str(Path(self._conf_path))

    def _write_conf(self) -> None:
        with open(str(self._conf_file), 'w') as configfile:
            yaml.dump(self.conf_dict, configfile)

    def read_conf(self) -> dict:
        converted = BaseFileManager.read_conf_from_file(self._conf_file)
        self.conf_dict = converted if converted else {}
        return self.conf_dict

    def run(self, inputed_code: str, operated_object: str) -> dict or None:
        """operation flow according to inputed_code pass by BaseFileManagerUI.

        Args:
            inputed_code: str
                the relation between inputed_code and object:
                    need existing object: 'READ', 'UPDATE', 'DELETE', 'RENAME'
                    need non-existing object: 'ADD'
            operated_object: str

        Returns:
            return none or a dict when readed.
        """
        # rewrite this function according to your program
        # better to create a flowchart before write your code

        # inputed_code in ['READ', 'ADD', 'UPDATE', 'DELETE', 'RENAME']
        if inputed_code == 'READ':
            pass
        elif inputed_code == 'ADD':
            pass
        elif inputed_code == 'UPDATE':
            pass
        elif inputed_code == 'DELETE':
            pass
        elif inputed_code == 'RENAME':
            pass

    @staticmethod
    def get_cwdPath(to_str=False) -> Path or str:
        "return Path(BaseFileManager.py).parents[2] as cwdPath"
        return cwdPath if not to_str else cwdPath.resolve()

    @staticmethod
    def read_conf_from_file(filepath: Path, encoding: str = '') -> dict or list:
        """read config from file"""
        if Path(filepath).exists() and Path(filepath).is_file():
            if encoding:
                with open(str(filepath), encoding=encoding) as configfile:
                    data = yaml.load(configfile, Loader=yaml.Loader)
                return data
            else:
                with open(str(filepath)) as configfile:
                    data = yaml.load(configfile, Loader=yaml.Loader)
                return data
        else:
            log.error('Error. Invaild filepath[{}] to read conf.'.format(filepath))
            return {}

    @property
    def conf_path(self):
        return self._conf_path

    @conf_path.setter
    def conf_path(self, new_path: Path or str):
        old_path = self._conf_path
        self._conf_path = self._check_path(new_path)
        if str(old_path) != str(self._conf_path):
            log.info("""The default path of conffile changed.
            From old_path: {0}
            to new_path: {1}""".format(str(old_path), str(self._conf_path)))

            # update self._conf_file and check and update
            self._conf_file = Path(self._conf_path).joinpath(self._conf_filename)
            self._check_conffile()
            self._write_conf()

    @property
    def conf_filename(self):
        return self._conf_filename

    @conf_filename.setter
    def conf_filename(self, new_name: str):
        if not isinstance(new_name, str):
            raise TypeError('Expected a string')
        old_name = self._conf_filename
        self._conf_filename = str(new_name)
        if str(old_name) != str(self._conf_filename):
            log.info("""The filename of conffile changed.
            From old_name: {0}
            to new_name: {1}""".format(str(old_name), str(new_name)))

            # update self._conf_file and check and update
            self._conf_file = Path(self._conf_path).joinpath(self._conf_filename)
            self._check_conffile()
            self._write_conf()


class BaseFileManagerUI:
    # manage the operation between user input and conf_file
    def __init__(self, file_manager: BaseFileManager):
        self._support_code = ['READ', 'UPDATE', 'DELETE', 'RENAME', 'ADD', 'CLEAR']
        self._handling_code = ''  # the code that present the running status
        self.fmgr = file_manager

        log.debug('BaseFileManagerUI inited')

    def _check_handle(self, inputed_code) -> None:
        """check inputed code in _upport_code or not, if not, reinput until True."""
        if inputed_code.upper() not in self._support_code:
            log.error('Invaild code[{}] inputed.'.format(inputed_code))
            self._handling_code = input_checking_list(
                self._support_code, 'Please choose your operation.')
        else:
            self._handling_code = inputed_code.upper()

    def run(self, inputed_code: str = '', operated_object: str = '') -> dict or None:
        """operation flow according to inputed_code.

        Args:
            inputed_code: str
                the relation between inputed_code and object:
                    need existing object: 'READ', 'UPDATE', 'DELETE', 'RENAME'
                    need non-existing object: 'ADD'
                    not need object: 'CLEAR'
            operated_object: str

        Returns:
            return none or a dict when readed.
        """
        # rewrite this function according to your program
        # better to create a flowchart before write your code

        if not inputed_code:
            inputed_code = input_checking_list(
                self._support_code, case_sens=False,
                tip_words='Please choose your operation.'
            )
        # check inputed code in _support_code or not, if not, reinput until True.
        self._check_handle(inputed_code)

        # here is a simple flow, without additional input and redirect
        if self._handling_code == 'READ':
            self._code_read(operated_object)
        elif self._handling_code == 'UPDATE':
            self._code_update(operated_object)
        elif self._handling_code == 'DELETE':
            self._code_delete(operated_object)
        elif self._handling_code == 'RENAME':
            self._code_rename(operated_object)
        elif self._handling_code == 'ADD':
            self._code_add(operated_object)
        elif self._handling_code == 'CLEAR':
            self._code_clear()
        log.info('ManagaerUI run over.')

    def _code_read(self, operated_object) -> dict:
        # rewrite this function according to your program
        log.info('Object[{}] readed.'.format(operated_object))
        return self.fmgr.run('READ', operated_object)

    def _code_update(self, operated_object) -> None:
        # rewrite this function according to your program
        self.fmgr.run('UPDATE', operated_object)
        log.info('Object[{}] updated.'.format(operated_object))

    def _code_rename(self, operated_object) -> None:
        # rewrite this function according to your program
        self.fmgr.run('RENAME', operated_object)
        log.info('Object[{}] renamed.'.format(operated_object))

    def _code_delete(self, operated_object) -> None:
        # rewrite this function according to your program
        self.fmgr.run('DELETE', operated_object)
        log.info('Object[{}] deleted.'.format(operated_object))

    def _code_add(self, operated_object) -> None:
        # rewrite this function according to your program
        self.fmgr.run('ADD', operated_object)
        log.info('Object[{}] added.' .format(operated_object))

    def _code_clear(self) -> None:
        # rewrite this function according to your program
        # self._objects_list should be readed in self.__init__()
        self._objects_list = []
        for i in self._objects_list:
            self.fmgr.run('DELETE', i)

    @property
    def handling_code(self):
        return self._handling_code

    @handling_code.setter
    def handling_code(self, new_code: str):
        self._check_handle(new_code)
        self._handling_code = new_code


if __name__ == '__main__':
    file_manager = BaseFileManager()
    manager = BaseFileManagerUI(file_manager)
    log.info('file_manager.get_cwdPath(): %s', file_manager.get_cwdPath())
    log.info('manager.run(): %s', manager.run())
