from setuptools import setup

setup(
    name='milo',
    version='0.1.3',
    description="Useful Python code, primarily intented for the author's use.",
    packages=['milo', 'milo.redis_utils'],
    license='BSD',
    url='https://github.com/ShawnMilo/milo',
    author='Shawn Milochik',
    author_email='shawn@milochik.com',
    zip_safe=False,
    keywords='milo stuff',
    install_requires=['redis>=2.7.2'],
    #test_suite="milo.tests",
)
