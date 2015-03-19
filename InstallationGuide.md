# Installation Guide #

**NOTE**: fileprocessor **only supports Python 3.0.0+**. There is **no** Python 2 support!

Like many Python libraries, installing fileprocessor package is achieved by running a Python installation script. After downloading fileprocessor, open a terminal and navigate to the **root** directory of the project. This directory should contain  a script called `setup.py`. Run the command:

```
python setup.py install
```

to install fileprocessor on your existing Python installation. Note that you may need administrator/root access for this.

After running the script, the fileprocessor package can be used by your other Python scripts and projects. To ensure the installation was successful, open an interaction Python session by calling `python` in a terminal and writing:

```
import fileprocessor
```

If no error is thrown, then the installation was successful.