from gettext import install
from setuptools import setup,find_packages
import mycart
setup(
      name='mycart',
      version=1.2,
      packages=find_packages(),
      install_requires=[],
      entry_points={
            'console_scripts':[
                  'mycart =mycart:cli'
            ]
      },
)