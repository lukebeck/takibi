from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name='Takibi',
    version='0.4',
    description='CLI flashcard application',
    long_description=readme(),
    author='Luke Beck',
    url='https://github.com/lukebeck/takibi',
    py_modules=['takibi'],
    install_requires=[
    ],
    include_package_data=True,
    entry_points = {
        'console_scripts': ['takibi=takibi:main','takibi-path=takibi:takibiPath'],
    }
)
