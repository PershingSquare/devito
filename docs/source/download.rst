===========================
Download and Install Devito
===========================

There are three main approaches to installing Devito.

For those looking for a quick “out-of-the-box” way to try Devito, we recommend
the route of `Docker installation`_.
For those looking to use Devito alongside other packages as part of a project, we support
`pip installation`_. When developing for Devito, you might benefit from
following the `conda installation`_ .


Docker installation
-------------------

You can install and run Devito via Docker_:

.. _Docker: https://www.docker.com/  

There are several "tags" for the devito docker images. We provide `Docker for CPUs`_
and `Docker for GPUs`_ depending on the platform you want to deploy Devito. These are:

Docker for CPUs
```````````````
Available images:

- cpu-dev: for the latest development version (current github master)
- cpu-latest: for the latest github release
- cpu-vX.X.X: for a specific release (Release tags: https://github.com/devitocodes/devito/tags)

.. code-block:: shell

   # NOTE (admin-sudo access may be needed) for some steps

   # 1. Pull Devito image
   docker pull devitocodes/devito:cpu-latest

   # 2. (Optional but recommended) Run the tests
   docker run --rm --name testrun 'devitocodes/devito:cpu-latest' pytest tests/test_operator.py

   # 3. Start a bash shell with Devito
   docker run --rm -it devitocodes/devito:cpu-latest /bin/bash

   # 4. Start a Jupyter notebook server on port 8888
   docker run --rm -it -p 8888:8888 devitocodes/devito:cpu-latest

These sample commands above have only been included as illustrations of typical
uses of Devito inside a container. They are not required to be run in that order.
Please also review these commands within the dockerfile itself:
`Dockerfile <https://github.com/devitocodes/devito/blob/master/docker/Dockerfile>`_


Docker for GPUs
```````````````
The GPU image differs from the CPU image regarding the additional compilers and toolkits necessary to run on GPUs. It contains the same installation and usage of Devito as the CPU image.

Available images:

- gpu-dev: for the latest development version (current github master)
- gpu-latest: for the latest github release
- gpu-vX.X.X: for a specific release (Release tags: https://github.com/devitocodes/devito/tags)

Tags for several devito releases can be found here: https://github.com/devitocodes/devito/tags

NOTE: To run the GPU version docker it is necessary to first install the `Nvidia container toolkit <https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html#setting-up-nvidia-container-toolkit>`_.

.. code-block:: shell

   # NOTE (admin-sudo access may be needed) for some steps
   # 1. Pull Devito image
   docker pull devitocodes/devito:gpu-latest

   # 2. (Optional but recommended) Run the tests
   docker run --gpus all --rm --name testrun 'devitocodes/devito:gpu-latest' pytest tests/test_gpu_openacc.py

   # 3. Start a bash shell with Devito
   docker run --gpus all --rm -it devitocodes/devito:gpu-latest /bin/bash

These sample commands above have only been included as illustrations of typical
uses of Devito inside a container. They are not required to be run in that order.

1. Command 1 pulls the docker image of Devito in your machine.

2. Command 2 above runs the unit tests included with Devito to check whether the 
installation succeeded. Testing is not necessary but a handy first thing to try running.

3. Command 3 above starts a bash (command-line) shell with Devito loaded into the
environment. Essentially, it means that any python code run after this command will
see devito when doing imports like `from devito import Function`. Any code using
Devito can be executed using this method.

4. Command 4 starts a Jupyter_ notebook server inside the Docker
container and forwards the port to `http://localhost:8888`.
After running this command, you can copy-paste the complete URL from the terminal window where
the command was run - to a browser to open a jupyter session to try out the included
tutorials. Alternatively, you may simply point your browser to `http://localhost:8888`
and, if prompted for a password, copy-paste the authentication token from the command
window. Once successfully in the Jupyter notebook session, proceed to run the tutorials
provided in the `examples` folder or create your own notebooks. 

.. _Jupyter: https://jupyter.org/

pip installation
----------------

This is the recommended method when setting up Devito as part of a larger project
that uses Devito among other python packages. To install Devito using `pip`, simply
do:


.. code-block:: shell

   pip install --user git+https://github.com/devitocodes/devito.git

Devito is also available as a `pip package`_ in PyPI.
To install Devito (without the tutorials and examples), follow:

.. code-block:: shell

   pip install devito

You may also install additional/optional packages via:

- extras : optional dependencies for Jupyter noetbooks, plotting, benhmarking
- mpi : optional dependencies for MPI (mpi4py)
- nvidia : optional dependencies for targetting GPU deployment

.. code-block:: shell

   pip install devito[extras,mpi,nvidia]


.. _pip package: https://pypi.org/project/devito/

Note that you do not need to get the code via `git clone` in this method. 
Depending on your needs, this might also be the recommended setup for using Devito
in a production-like environment. However, since some components need to be
compiled before use, this approach may be sensitive to the C/C++ compilers present
on your system and the related environment, including what other packages you might
have installed.

conda installation
------------------

If your objective is to contribute to and develop for Devito, the recommended way would
be to use the included conda environment that also installs an appropriate C compiler
along with all the bells and whistles we felt were necessary when developing for Devito.
Please install either Anaconda_ or Miniconda_ using the instructions provided at the
download links. Devito requires Python3 (3.6 to 3.10 currently supported).

To install Devito, including examples, tests and tutorial notebooks,
follow these:

.. code-block:: shell

   git clone https://github.com/devitocodes/devito.git
   cd devito
   conda env create -f environment-dev.yml
   source activate devito
   pip install -e .


Facing issues?
--------------

If you are facing any issues, we are happy to help on Slack_. Also, have a look at our
list of known installation issues_.

.. _issues: https://github.com/devitocodes/devito/wiki/Installation-Issues

.. _Slack: https://join.slack.com/t/devitocodes/shared_invite/zt-gtd2yxj9-Y31YKk_7lr9AwfXeL2iMFg

.. _Anaconda: https://www.continuum.io/downloads

.. _Miniconda: https://conda.io/miniconda.html
