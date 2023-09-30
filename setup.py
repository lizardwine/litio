from setuptools import setup,find_packages

with open('README.md', 'r') as reader:
    readme = reader.read()

setup(
    author='Lizard wine',
    author_email='lizardwine@hotmail.com',
    name='litio',
    description='A command line function tester',
    long_description=readme,
    url='https://github.com/lizardwine/litio',
    project_urls={
        "Bug Tracker": "https://github.com/lizardwine/litio/issues",
    },
    license='GPL v3.0',
    version='0.5.0.0',
    keywords=['testing', 'tester'],
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development'
    ],
    entry_points={
        'console_scripts': [
            'litio = litio.__main__:main'
        ]
    },
    package_dir={"": "src"},
    requires=['pyyaml','rich'],
    packages=find_packages(where="src"),
    python_requires=">=3.6",
)