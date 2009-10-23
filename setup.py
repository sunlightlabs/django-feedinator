from distutils.core import setup

long_description = ''#open('README.rst').read()

setup(
    name='django-feedinator',
    version="0.2.0",
    package_dir={'feedinator': 'feedinator'},
    packages=['feedinator', 'feedinator.templatetags'],
    package_data={'feedinator': ['templates/feedinator/*.html']},
    description='Django feedinator',
    author='Jeremy Carbaugh',
    author_email='jcarbaugh@sunlightfoundation.com',
    license='BSD License',
    url='http://github.com/sunlightlabs/django-feedinator/',
    long_description=long_description,
    platforms=["any"],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Environment :: Web Environment',
    ],
)
