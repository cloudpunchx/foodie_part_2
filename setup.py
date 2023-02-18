from setuptools import setup

setup(
    name='foodie_back_end',
    packages=['app'],
    include_package_data=True,
    install_requires=[
        'flask',
    ],
)