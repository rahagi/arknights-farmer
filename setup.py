# -*- coding: utf-8 -*-
import setuptools
import arknights_farmer

LONG_DESC = open('README.md').read()
VERSION = arknights_farmer.__version__

setuptools.setup(
        name='arknights-farmer',
        version=VERSION,
        author='cytopz',
        author_email='cytopz@protonmail.com',
        description='Farming assistant for Arknights',
        long_description=LONG_DESC,
        long_description_content_type="text/markdown",
        url='https://github.com/cytopz/arknights-farmer',
        packages=setuptools.find_packages(),
        install_requires=['gacha-elper', 'urllib3', 'requests'],
        entry_points={'console_scripts': ['arknights-farmer=arknights_farmer.__main__:main']},
        classifiers=[
            "Development Status :: 3 - Alpha",
            "Programming Language :: Python :: 3 :: Only",
            "Operating System :: OS Independent",
            "Topic :: Games/Entertainment",
            "License :: OSI Approved :: MIT License"
        ],
        python_requires='>=3.7.4',
        license='MIT'
)
