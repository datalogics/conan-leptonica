#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os
import shutil


class LeptonicaConan(ConanFile):
    name = "leptonica"
    version = "1.75.1"
    url = "https://github.com/bincrafters/conan-leptonica"
    website = "http://leptonica.org"
    description = "Library containing software that is broadly useful for image processing and image analysis applications."
    license = "BSD 2-Clause"

    exports = ["LICENSE.md"]
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"

    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False],
               "with_gif": [True, False],
               "with_jpeg": [True, False],
               "with_png": [True, False],
               "with_tiff": [True, False]
              }
    default_options = ("shared=False",
                       "with_gif=False",
                       "with_jpeg=True",
                       "with_png=True",
                       "with_tiff=True")

    source_subfolder = "source_subfolder"

    def requirements(self):
        self.requires.add("zlib/[~=1.2]@conan/stable")
        if self.options.with_gif:
            self.requires.add("giflib/[>=5.1.3]@bincrafters/testing")
        if self.options.with_jpeg:
            self.requires.add("libjpeg/9b@bincrafters/stable")
        if self.options.with_png:
            self.requires.add("libpng/[>=1.6.34]@bincrafters/stable")
        if self.options.with_tiff:
            self.requires.add("libtiff/[>=4.0.8]@bincrafters/stable")

    def source(self):
        source_url = "https://github.com/DanBloomberg/leptonica"
        tools.get("{0}/archive/{1}.tar.gz".format(source_url, self.version))
        extracted_dir = self.name + "-" + self.version

        os.rename(extracted_dir, self.source_subfolder)
        os.rename(os.path.join(self.source_subfolder, "CMakeLists.txt"),
                  os.path.join(self.source_subfolder, "CMakeListsOriginal.txt"))
        shutil.copy("CMakeLists.txt",
                    os.path.join(self.source_subfolder, "CMakeLists.txt"))

    def build(self):
        cmake = CMake(self)
        cmake.definitions['STATIC'] = not self.options.shared
        cmake.definitions['BUILD_PROG'] = False
        # avoid finding system libs
        cmake.definitions['CMAKE_DISABLE_FIND_PACKAGE_GIF'] = not self.options.with_gif
        cmake.definitions['CMAKE_DISABLE_FIND_PACKAGE_PNG'] = not self.options.with_png
        cmake.definitions['CMAKE_DISABLE_FIND_PACKAGE_TIFF'] = not self.options.with_tiff
        cmake.definitions['CMAKE_DISABLE_FIND_PACKAGE_JPEG'] = not self.options.with_jpeg
        # disable pkgconfig to avoid finding JP2K and WEBP
        cmake.definitions['CMAKE_DISABLE_FIND_PACKAGE_PkgConfig'] = True
        cmake.configure(source_folder=self.source_subfolder)
        cmake.build()
        cmake.install()

    def package(self):
        self.copy(pattern="leptonica-license.txt", dst="license", src=self.source_subfolder)
        #self.copy(pattern="*.dll", dst="bin", keep_path=False)
        #self.copy(pattern="*.lib", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
