from setuptools import setup

with open('requirements.txt') as f:
    install_requires = f.read().splitlines()

setup(
  name='discordBot',
  packages=['discordBot'],
  version='0.1.0',
  #author='...',
  #description='...',
  install_requires=install_requires,
  py_modules=["modules.Bot","modules.Citation","modules.ErrorHandler","modules.Music","modules.Song","modules.SongQueue","modules.VoiceState","modules.YTDLSource" ],
  entry_points={
    # example: file some_module.py -> function main
    #'console_scripts': ['someprogram=some_module:main']
  },
)