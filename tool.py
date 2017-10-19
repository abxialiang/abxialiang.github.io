#coding:utf8
def fordir_path(dirpath, subdir=True, ext_filtration=u'*'):
    # 使用for来遍历目录中的所有文件路径(不返回目录路径),包括子目录
    # subdir包含子目录, ext_filtration指定后缀名,ext_filtration='txt|flv|zip'
    import os
    assert not isinstance(dirpath, bytes), 'dirpath most be unicode string'
    assert not isinstance(ext_filtration, bytes), 'ext_filtration most be unicode string'
    assert os.path.exists(dirpath), 'dirpath dir not exist'
    assert os.path.isdir(dirpath), 'dirpath is file,not dir'

    ext_filtration = ext_filtration.lower().strip('|')
    if len(ext_filtration) > 5 and '|' not in ext_filtration:
        raise BaseException('ext_filtration set error.')

    if ext_filtration != '*':
        ext_filtration = ['.{}'.format(ext.strip().strip('.')).lower() for ext in ext_filtration.strip().split('|')]
    if subdir:
        for dirpath, dirnames, filenames in os.walk(dirpath):
            for filename in filenames:
                if ext_filtration != '*':
                    __, ext = os.path.splitext(filename)
                    if ext.lower() not in ext_filtration:
                        continue
                yield os.path.join(dirpath, filename).replace(u'\\', u'/')
    else:
        import glob
        for filepath in glob.glob(os.path.join(dirpath, '*')):
            if os.path.isfile(filepath):
                if ext_filtration != '*':
                    __, ext = os.path.splitext(filepath)
                    if ext.lower() not in ext_filtration:
                        continue
                yield filepath
