# coding: utf-8

'''
Utilitários do projeto
'''

import os
import errno

def mkdir_p(path):
    '''Cria o path se ele não existir'''
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise
