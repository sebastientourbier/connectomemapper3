#!/usr/bin/env python

"""`Setup.py` for Connectome Mapper 3 Graphical User Inerface (BIDS App Manager)."""

import os
import pkg_resources
import sys
import setuptools
from setuptools.command.install import install
from setuptools.command.develop import develop

from datalad.api import get, drop

from cmp.info import __version__


def get_cmtklib_data_content():
    """ Get file content of datalad dataset stored in cmtklib/data."""
    cmtklib_data_dir = pkg_resources.resource_filename(
            'cmtklib',
            'data/'
    )
    # Get file content managed by datalad/git-annex
    get(cmtklib_data_dir, dataset=cmtklib_data_dir, recursive=True)


def drop_cmtklib_data_content():
    """ Drop file content of datalad dataset stored in cmtklib/data."""
    cmtklib_data_dir = pkg_resources.resource_filename(
            'cmtklib',
            'data/'
    )
    # Get file content managed by datalad/git-annex
    drop(cmtklib_data_dir, dataset=cmtklib_data_dir, recursive=True)


class PreDevelopCommand(develop):
    """Post-installation for development mode."""
    def run(self):
        # PRE-INSTALL
        print('[PRE-INSTALL] Handle datalad resources...')
        get_cmtklib_data_content()
        # INSTALL
        install.run(self)
        # POST-INSTALL
        print('[POST-INSTALL] Clean datalad resources...')
        drop_cmtklib_data_content()


class PreInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        # PRE-INSTALL
        print('[PRE-INSTALL] Handle datalad resources...')
        get_cmtklib_data_content()
        # INSTALL
        install.run(self)
        # POST-INSTALL
        print('[POST-INSTALL] Clean datalad resources...')
        drop_cmtklib_data_content()


class VerifyVersionCommand(install):
    """Custom command to verify that the git tag matches our version"""
    description = 'verify that the git tag matches our version'

    def run(self):
        tag = os.getenv('CIRCLE_TAG')
        version = f'{__version__}'

        if tag != version:
            info = f'Git tag: {tag} does not match the version of this app: {version}'
            sys.exit(info)


# Get directory where this file is located
directory = os.path.abspath(os.path.dirname(__file__))

# Remove any MANIFEST of a previous installation
if os.path.exists('MANIFEST'):
    os.remove('MANIFEST')

# Define the packages to be installed
packages = ["cmp",
            "cmp.cli",
            "cmp.stages",
            "cmp.stages.preprocessing",
            "cmp.stages.segmentation",
            "cmp.stages.parcellation",
            "cmp.stages.registration",
            "cmp.stages.diffusion",
            "cmp.stages.functional",
            "cmp.stages.connectome",
            "cmp.pipelines",
            "cmp.pipelines.anatomical",
            "cmp.pipelines.diffusion",
            "cmp.pipelines.functional",
            "cmp.bidsappmanager",
            "cmp.bidsappmanager.stages",
            "cmp.bidsappmanager.stages.preprocessing",
            "cmp.bidsappmanager.stages.segmentation",
            "cmp.bidsappmanager.stages.parcellation",
            "cmp.bidsappmanager.stages.registration",
            "cmp.bidsappmanager.stages.diffusion",
            "cmp.bidsappmanager.stages.functional",
            "cmp.bidsappmanager.stages.connectome",
            "cmp.bidsappmanager.pipelines",
            "cmp.bidsappmanager.pipelines.anatomical",
            "cmp.bidsappmanager.pipelines.diffusion",
            "cmp.bidsappmanager.pipelines.functional",
            "cmtklib",
            "cmtklib.bids",
            "cmtklib.interfaces",
            "resources"]

# Define the package data to be installed
package_data = {'cmp':
                ['cmp3_icon.png'],
                'cmp.bidsappmanager':
                ['images/*.png',
                 'pipelines/anatomical/*.png',
                 'pipelines/diffusion/*.png',
                 'pipelines/functional/*.png'],
                'resources':
                ['buttons/*.png',
                 'icons/*png'],
                'cmtklib':
                ['data/parcellation/lausanne2008/*/*.*',
                 'data/parcellation/lausanne2018/*.*',
                 'data/parcellation/lausanne2018/*/*.*',
                 'data/segmentation/ants_template_IXI/*/*.*',
                 'data/segmentation/ants_template_IXI/*.*',
                 'data/segmentation/ants_MICCAI2012_multi-atlas_challenge_data/*/*.*',
                 'data/segmentation/ants_MICCAI2012_multi-atlas_challenge_data/*.*',
                 'data/parcellation/nativefreesurfer/*/*.*',
                 'data/colortable_and_gcs/*.*',
                 'data/colortable_and_gcs/my_atlas_gcs/*.*',
                 'data/diffusion/odf_directions/*.*',
                 'data/diffusion/gradient_tables/*.*',
                 'data/segmentation/thalamus2018/*.*']
                }

# Extract package requirements from Conda environment.yml
include_conda_pip_dependencies = True
install_requires = []
dependency_links = []
if include_conda_pip_dependencies:
    path = os.path.join(directory, 'environment.yml')
    with open(path) as read_file:
        state = "PREAMBLE"
        for line in read_file:
            # Strip white space for right and left side
            line = line.rstrip().lstrip(" -")
            # Determine if we are in the list of conda or PIP dependencies
            if line == "dependencies:":
                state = "CONDA_DEPS"
            elif line == "pip:":
                state = "PIP_DEPS"
            # Add PIP dependencies to list of required dependencies
            if state == "PIP_DEPS" and "pip" not in line:
                # line = line.split('==')[0]
                # Appends to dependency links
                dependency_links.append(line)
                # Adds package name to dependencies
                install_requires.append(line)
print(f'Install requires: {install_requires}')
print(f'Dependency links: {dependency_links}')


# Read the contents of your README file
with open(os.path.join(directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


def main():
    """Main function of CMP3 ``setup.py``"""
    # Setup configuration
    setuptools.setup(
        name='cmp',
        version=__version__.split('v')[-1],
        description='Connectome Mapper 3: A software pipeline for multi-scale connectome mapping of multimodal data',
        long_description=long_description,
        author='Sebastien Tourbier',
        author_email='sebastien.tourbier@alumni.epfl.ch',
        url='https://github.com/connectomicslab/connectomemapper3',
        entry_points={
            "console_scripts": [
                'connectomemapper3 = cmp.cli.connectomemapper3:main',
                'cmpbidsappmanager = cmp.cli.cmpbidsappmanager:main',
                'showmatrix_gpickle = cmp.cli.showmatrix_gpickle:main'
            ]
        },
        license='BSD-3-Clause',
        classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Intended Audience :: Science/Research',
            'Intended Audience :: Developers',
            'License :: OSI Approved',
            'Programming Language :: Python',
            'Topic :: Software Development',
            'Topic :: Scientific/Engineering',
            'Operating System :: POSIX',
            'Operating System :: Unix',
            'Operating System :: MacOS',
            'Programming Language :: Python :: 3.7',
        ],
        maintainer='Connectomics Lab, CHUV',
        maintainer_email='info@connectomics.org',
        packages=packages,
        include_package_data=True,
        package_data=package_data,
        # requires=["numpy (>=1.18)", "nipype (>=1.5.0)", "pybids (>=0.10.2)"],
        install_requires=install_requires,
        dependency_links=dependency_links,
        python_requires='>=3.7',
        cmdclass={
                'verify': VerifyVersionCommand,
                'develop': PreDevelopCommand,
                'install': PreInstallCommand
        }
        )


if __name__ == "__main__":
    main()
