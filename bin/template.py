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
import logging
from pathlib import Path
sys.path.append(str(Path(__file__).parents[1]))


from src.manager.ConfManager import cwdPath  # noqa: E402
from src.manager.ConfManager import conf  # noqa: E402


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        # filename=os.path.basename(__file__) + '_' + time.strftime('%Y%m%d', time.localtime()) + '.log',
        # filemode='a',
        format='%(asctime)s %(name)s %(levelname)s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S')
    logging.debug('start DEBUG')
    logging.debug('==========================================================')

    print(cwdPath)
    print(type(cwdPath))
    print(conf.conf_dict)

    logging.debug('==========================================================')
    logging.debug('end DEBUG')
