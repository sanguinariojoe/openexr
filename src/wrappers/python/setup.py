from setuptools import setup, Extension
import os
import platform
import re


DESC = """Python bindings for the OpenEXR image file format.

This is a script to autobuild the wheels using github actions. Please, do not
use it manually

If you detect any problem, please feel free to report the issue on the GitHub
page:

https://github.com/AcademySoftwareFoundation/openexr/issues
"""

if os.path.isdir("./openexr.install"):
    # Probably we are on the github action building the wheels

    # Get the version and library suffix for both OpenEXR and Imath from
    # the .pc pkg-config file.

    def pkg_config(var, pkg):
        with open(f'./openexr.install/lib/pkgconfig/{pkg}.pc', 'r') as f:
            return re.search(f'{var}([^ \n]+)', f.read()).group(1)

    imath_libsuffix = pkg_config("libsuffix=", "Imath")
    openexr_libsuffix = pkg_config("libsuffix=", "OpenEXR")
    openexr_version = pkg_config("Version: ", "OpenEXR")
    openexr_version_major, openexr_version_minor, openexr_version_patch = openexr_version.split('.')

    include_dirs=['./openexr.install/include/OpenEXR',
                  './openexr.install/include/Imath',]
    library_dirs = []
    libs=[]
    libs_static=[f'OpenEXR{openexr_libsuffix}',
                 f'IlmThread{openexr_libsuffix}',
                 f'Iex{openexr_libsuffix}',
                 f'Imath{imath_libsuffix}',
                 f'OpenEXRCore{openexr_libsuffix}']
    libs_dir = "./openexr.install/lib/"
    if not os.path.isdir(libs_dir):
        libs_dir = "./openexr.install/lib64/"
    if platform.system() == "Windows":
        extra_link_args = [libs_dir + lib + ".lib"
                        for lib in libs_static]
        extra_link_args = extra_link_args + [
            "ws2_32.lib", "dbghelp.lib", "psapi.lib", "kernel32.lib", "user32.lib",
            "gdi32.lib", "winspool.lib", "shell32.lib", "ole32.lib",
            "oleaut32.lib", "uuid.lib", "comdlg32.lib", "advapi32.lib"]
    else:
        extra_link_args = [libs_dir + "lib" + lib + ".a"
                        for lib in libs_static]
else:
    # This is probably the sdist
    if platform.system() == "Windows":
        include_dirs = [
            "C:/Program Files (x86)/OpenEXR/include/Imath",
            "C:/Program Files (x86)/OpenEXR/include/OpenEXR",
        ]
        library_dirs = [
            "/usr/lib",
            "/usr/local/lib",
            "/opt/local/lib",
            "/opt/homebrew/opt/openexr/lib",
            "/opt/homebrew/opt/imath/lib",
        ]
    else:
        include_dirs = [
            "/usr/include/OpenEXR",
            "/usr/local/include/OpenEXR",
            "/opt/local/include/OpenEXR",
            "/usr/include/Imath",
            "/usr/local/include/Imath",
            "/opt/local/include/Imath",
            "/opt/homebrew/opt/openexr/include/OpenEXR",
            "/opt/homebrew/opt/imath/include/Imath",
        ]
        library_dirs = [
            "C:/Program Files (x86)/OpenEXR/lib",
            "C:/Program Files/zlib/lib",
        ]
    libs=['OpenEXR', 'IlmThread', 'Iex', 'Imath', 'OpenEXRCore']
    extra_link_args = []


extra_compile_args = []
if platform.system() == 'Darwin':
    extra_compile_args += ['-std=c++11',
                           '-Wc++11-extensions',
                           '-Wc++11-long-long']

setup(name='OpenEXR',
    long_description = DESC,
    ext_modules=[ 
        Extension('OpenEXR',
                  ['OpenEXR.cpp'],
                  language='c++',
                  include_dirs=include_dirs,
                  library_dirs=library_dirs,
                  libraries=libs,
                  extra_compile_args=extra_compile_args,
                  extra_link_args=extra_link_args,
                  )
    ],
    py_modules=['Imath'],
)
