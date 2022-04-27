#!/usr/bin/env python
from __future__ import print_function
import pefile
import os
import sys


def get_dependency(filename):
    deps = []
    pe = pefile.PE(filename.lower())
    try:
        for imp in pe.DIRECTORY_ENTRY_IMPORT:
            deps.append(imp.dll.decode())
    except AttributeError:
        pass
    return deps


def dep_tree(root, prefix=None):
    if not prefix:
        arch, bits = get_arch(root)
        prefix = '/usr/lib{}/wine/{}-windows'.format(bits, arch)
    dep_dlls = dict()

    def dep_tree_impl(root, prefix):
        root_path = os.path.dirname(os.path.abspath(root))
        for dll in get_dependency(root):
            dll = dll.lower()
            if dll in dep_dlls:
                continue
            local_path = os.path.join(root_path, dll)
            full_path = os.path.join(prefix, dll)

            if os.path.exists(local_path):
                dep_dlls[dll] = local_path
                dep_tree_impl(local_path, prefix=prefix)
            elif os.path.exists(full_path):
                dep_dlls[dll] = full_path
                dep_tree_impl(full_path, prefix=prefix)
            else:
                dep_dlls[dll] = 'not found'

    dep_tree_impl(root, prefix)
    return (dep_dlls)


def get_arch(filename):
    type2arch = {pefile.OPTIONAL_HEADER_MAGIC_PE: 'i386',
                 pefile.OPTIONAL_HEADER_MAGIC_PE_PLUS: 'x86_64'}
    type2bits = {pefile.OPTIONAL_HEADER_MAGIC_PE: '32',
                 pefile.OPTIONAL_HEADER_MAGIC_PE_PLUS: ''}
    pe = pefile.PE(filename)
    try:
        return (type2arch[pe.PE_TYPE], type2bits[pe.PE_TYPE])
    except KeyError:
        sys.stderr.write('Error: unknown architecture')
        sys.exit(1)


if __name__ == '__main__':
    filename = sys.argv[1]
    for dll, full_path in dep_tree(filename).items():
        print(' ' * 7, dll, '=>', full_path)
