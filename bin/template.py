#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   template.py
@Author  :   Billy Zhou
@Time    :   2021/08/06
@Version :   0.0.0
@Desc    :   None
'''


import sys
from pathlib import Path
cwdPath = Path(__file__).parents[1]
sys.path.append(str(cwdPath))

from src.manager.Logger import logger  # noqa: E402
log = logger.get_logger(__name__)


if __name__ == '__main__':
    from src.manager.ConfManager import ConfManager  # noqa: E402
    conf = ConfManager()
    log.info('conf.read_conf(): %s', conf.read_conf())
    log.info('conf.get_cwdPath(): %s', conf.get_cwdPath())
