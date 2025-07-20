from setuptools import setup, find_packages

setup(
    name='pythonaire',
    version='0.2.1',
    package_dir={"": "src"},
    description='A personal finance tracker using SQLite and Python.',
    author='Oliver Rodriguez',
    author_email='oliver.rdz@softpotato.xyz',
    packages=find_packages(where="src"),
    entry_points={
        'console_scripts': [
            'pythonaire = pythonaire.cli:main',  # Optional: global CLI access
        ]
    },
    install_requires=[],
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
