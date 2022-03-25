import setuptools

setuptools.setup(
    name='shpg',
    version='0.0.1',
    description='A sort package to create simple reporting static html pages',
    author="Bastien Cagna",

    extras_require={
        "doc": ["sphinx>=" + '1.0'],
    }
)
