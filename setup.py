from setuptools import setup,find_packages

with open('README.md', 'r') as reader:
    readme = reader.read()

requirements = [
    "PyYAML==6.0.1",
    "rich==13.7.0",
    "openai==1.3.5",
    "python-dotenv==1.0.0",
    "gitpython==3.1.40"
]

setup(
    author='Lizardwine',
    author_email='lizardwine@hotmail.com',
    name='litio',
    description='A simple tool for testing',
    long_description=readme,
    long_description_content_type='text/markdown',
    url='https://github.com/lizardwine/litio',
    project_urls={
        "Bug Tracker": "https://github.com/lizardwine/litio/issues",
    },
    license='GPL v3.0',
    version='1.5.2',
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
    install_requires=requirements,
    packages=find_packages(where="src"),
    python_requires=">=3.6",
)