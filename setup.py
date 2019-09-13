from setuptools import setup, find_packages

setup(name='weodata',
      packages=find_packages(),
      package_dir={'weodata': './weodata'},
      version='0.1.0',
      description='Python package for downloading the IMF World Economic Outlook dataset.',
      author='Tetsu HARUYAMA',
      author_email='haruyama@econ.kobe-u.ac.jp',
      url='https://github.com/spring-haru/weodata',
      license='LICENSE.rst',
      install_requires=['pandas'],
      classifiers=['Intended Audience :: Education',
                   'Intended Audience :: Science/Research',
                   'License :: OSI Approved :: MIT License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   ]
      )
