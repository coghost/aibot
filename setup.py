from setuptools import setup, find_packages
from aibot import VERSION

setup(
    name='aibot',
    version=VERSION,
    include_package_data=True,
    package_data={
        '': ['README.md'],
        'aibot': ['data/*.yaml'],
    },
    packages=find_packages(),
    author='lihe',
    author_email='imanux@sina.com',
    url='https://github.com/coghost/aibot',
    description='aibot do encapsulation of selenium',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    license='GPL',
    install_requires=[
        'selenium'
    ],
    project_urls={
        'Bug Reports': 'https://github.com/coghost/aibot/issues',
        'Source': 'https://github.com/coghost/aibot',
    },
    python_requires='>=3.8',
    classifiers=[
        'Programming Language :: Python :: 3.8',
    ],
    keywords=['selenium', 'aibot', 'crawler']
)
