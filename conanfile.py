from conans import ConanFile, tools
import os
import shutil

class ArmGccConan(ConanFile):
    name = "arm-gcc"
    version = "9.2-2019.12"
    author = "kistyuk.alex@gmail.com"
    homepage = "https://developer.arm.com/tools-and-software/open-source-software/developer-tools/gnu-toolchain/gnu-a"
    description = "The GNU Toolchain for the Cortex-A Family is a ready-to-use, open source suite of tools for C,\
                   C++ and Assembly programming. This toolchain targets processors from the Arm Cortex-A family \
                   and implements the Arm A-profile architecture."
    short_paths = True
    no_copy_source = True
    settings = {"os_build": ["Windows", "Linux"],
                "arch_build": ["x86_64"],
                "compiler": ["gcc"],
                "os": ["Linux"],
                "arch": ["armv7hf"]}

    def configure(self):
        if self.settings.compiler.version != "9":
            raise ConanInvalidConfiguration("only gcc 9 is supported")

    def source(self):
        url = "https://developer.arm.com/-/media/Files/downloads/gnu-a/{0}/binrel/".format(self.version)
        archive_name = "gcc-arm-{0}-{1}-arm-none-linux-gnueabihf.tar.xz".format(self.version, self._platform)
        source_url = url + archive_name
        tools.get(source_url)

    def package(self):
        toolchain = "gcc-arm-{0}-{1}-arm-none-linux-gnueabihf".format(self.version, self._platform)
        self.copy(pattern="*", dst=".", src=toolchain, keep_path=True, symlinks=True)

    def package_id(self):
        self.info.include_build_settings()
        del self.info.settings.os
        del self.info.settings.arch
        del self.info.settings.compiler

    def package_info(self):
        self.env_info.CC = self._define_tool_var('CC', 'gcc')
        self.env_info.CXX = self._define_tool_var('CXX', 'g++')
        self.env_info.LD = self._define_tool_var('LD', 'ld')
        self.env_info.AR = self._define_tool_var('AR', 'ar')
        self.env_info.AS = self._define_tool_var('AS', 'as')
        self.env_info.RANLIB = self._define_tool_var('RANLIB', 'ranlib')
        self.env_info.STRIP = self._define_tool_var('STRIP', 'strip')
        self.env_info.ADDR2LINE = self._define_tool_var('ADDR2LINE', 'addr2line')
        self.env_info.NM = self._define_tool_var('NM', 'nm')
        self.env_info.OBJCOPY = self._define_tool_var('OBJCOPY', 'objcopy')
        self.env_info.OBJDUMP = self._define_tool_var('OBJDUMP', 'objdump')
        self.env_info.READELF = self._define_tool_var('READELF', 'readelf')
        self.env_info.ELFEDIT = self._define_tool_var('ELFEDIT', 'elfedit')
        self.env_info.CMAKE_FIND_ROOT_PATH_MODE_PROGRAM = "BOTH"
        self.env_info.CMAKE_FIND_ROOT_PATH_MODE_LIBRARY = "BOTH"
        self.env_info.CMAKE_FIND_ROOT_PATH_MODE_INCLUDE = "BOTH"
        self.env_info.CMAKE_FIND_ROOT_PATH_MODE_PACKAGE = "BOTH"

    @property
    def _platform(self):
        return {"Windows": "mingw-w64-i686",
                "Linux": "x86_64"}.get(str(self.settings.os_build))

    def _tool_name(self, tool):
        suffix = '.exe' if self.settings.os_build == 'Windows' else ''
        return '%s-%s%s' % ("arm-none-linux-gnueabihf", tool, suffix)

    def _define_tool_var(self, name, value):
        toolchain_bin = os.path.join(self.package_folder, 'bin')
        path = os.path.join(toolchain_bin, self._tool_name(value))
        self.output.info('Creating %s environment variable: %s' % (name, path))
        return path

