import setuptools
from setuptools import Extension
from setuptools.command.build_ext import build_ext

class CMakeExtension(Extension):
    """
    An extension to run the cmake build

    This simply overrides the base extension class so that setuptools
    doesn't try to build your sources for you
    """

    def __init__(self, name, sources=[]):

        super().__init__(name = name, sources = sources)

class BuildCMakeExt(build_ext):
    """
    Builds using cmake instead of the python setuptools implicit build
    """

    def run(self):
        """
        Perform build_cmake before doing the 'normal' stuff
        """

        for extension in self.extensions:

            if extension.name == 'example_extension':

                self.build_cmake(extension)

        super().run()

    def build_cmake(self, extension: Extension):
        """
        The steps required to build the extension
        """

        self.announce("Preparing the build environment", level=3)

        # build_dir = pathlib.Path(self.build_temp)

        # extension_path = pathlib.Path(self.get_ext_fullpath(extension.name))

        # os.makedirs(build_dir, exist_ok=True)
        # os.makedirs(extension_path.parent.absolute(), exist_ok=True)

        # # Now that the necessary directories are created, build

        # self.announce("Configuring cmake project", level=3)

        # Change your cmake arguments below as necessary
        # Below is just an example set of arguments for building Blender as a Python module

        self.spawn(['pwd'])
        self.spawn(['cmake', 'CMakeLists.txt'])

        self.announce("Building binaries", level=3)
        self.spawn(['make', '-j', '4'])

        # Build finished, now copy the files into the copy directory
        # The copy directory is the parent directory of the extension (.pyd)

        # self.announce("Moving built python module", level=3)

        # bin_dir = os.path.join(build_dir, 'bin', 'Release')
        # self.distribution.bin_dir = bin_dir

        # pyd_path = [os.path.join(bin_dir, _pyd) for _pyd in
        #             os.listdir(bin_dir) if
        #             os.path.isfile(os.path.join(bin_dir, _pyd)) and
        #             os.path.splitext(_pyd)[0].startswith(PACKAGE_NAME) and
        #             os.path.splitext(_pyd)[1] in [".pyd", ".so"]][0]

        # shutil.move(pyd_path, extension_path)

        # After build_ext is run, the following commands will run:
        # 
        # install_lib
        # install_scripts
        # 
        # These commands are subclassed above to avoid pitfalls that
        # setuptools tries to impose when installing these, as it usually
        # wants to build those libs and scripts as well or move them to a
        # different place. See comments above for additional information



with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="demo-pypi-package", # Replace with your own username
    version="0.0.2",
    author="Example Author",
    author_email="author@example.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/quepas/demo-pypi-package",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    ext_modules=[CMakeExtension('example_extension')],
    cmdclass={'build_ext': BuildCMakeExt}
)
