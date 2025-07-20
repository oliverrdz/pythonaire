from setuptools import setup, find_packages

setup(
    name='pythonaire',
    version='0.2.0',
    description='A personal finance tracker using SQLite and Python.',
    author='Oliver Rodriguez',
    author_email='oliver.rdz@softpotato.xyz',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
