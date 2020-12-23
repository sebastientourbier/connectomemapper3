# Copyright (C) 2017-2019, Brain Communication Pathways Sinergia Consortium, Switzerland
# All rights reserved.
#
#  This software is distributed under the open-source license Modified BSD.

"""Connectome Mapper 3 Commandline Parser."""

import argparse

from .info import __version__
from .info import __release_date__


def get():
    """Return the argparse parser of the BIDS App.

    Returns
    -------
    p : object
       Instance of :class:`argparse.ArgumentParser` class
    """

    p = argparse.ArgumentParser(
        description='Entrypoint script of the BIDS-App Connectome Mapper version {}'.format(__version__))
    p.add_argument('bids_dir', help='The directory with the input dataset '
                                    'formatted according to the BIDS standard.')
    p.add_argument('output_dir', help='The directory where the output files '
                                      'should be stored. If you are running group level analysis '
                                      'this folder should be prepopulated with the results of the '
                                      'participant level analysis.')
    p.add_argument('analysis_level', help='Level of the analysis that will be performed. '
                                          'Multiple participant level analyses can be run independently '
                                          '(in parallel) using the same output_dir.',
                   choices=['participant', 'group'])
    p.add_argument('--participant_label', help='The label(s) of the participant(s) that should be analyzed. The label '
                                               'corresponds to sub-<participant_label> from the BIDS spec '
                                               '(so it does not include "sub-"). If this parameter is not '
                                               'provided all subjects should be analyzed. Multiple '
                                               'participants can be specified with a space separated list.',
                   nargs="+")

    p.add_argument("--session_label", help="""The label(s) of the session that should be analyzed.
                                            The label corresponds to ses-<session_label> from the
                                            BIDS spec (so it does not include "ses-"). If this
                                            parameter is not provided all sessions should be
                                            analyzed. Multiple sessions can be specified
                                            with a space separated list.""",
                   nargs="+")

    p.add_argument('--anat_pipeline_config',
                   help='Configuration .txt file for processing stages of the anatomical MRI processing pipeline')
    p.add_argument('--dwi_pipeline_config',
                   help='Configuration .txt file for processing stages of the diffusion MRI processing pipeline')
    p.add_argument('--func_pipeline_config',
                   help='Configuration .txt file for processing stages of the fMRI processing pipeline')

    p.add_argument('--number_of_threads',
                   type=int,
                   help='The number of OpenMP threads used for multi-threading by '
                        'Freesurfer, FSL, MRtrix3, Dipy, AFNI '
                        '(Set to [Number of available CPUs -1] by default).')

    p.add_argument('--number_of_participants_processed_in_parallel',
                   type=int,
                   help='The number of subjects to be processed in parallel (One by default).')

    p.add_argument('--set_mrtrix_rng_seed',
                   type=int,
                   help='Fix MRtrix3 random number generator seed')

    p.add_argument('--set_ants_random_seed',
                   type=int,
                   help='Fix ANTS random number generator seed ')

    p.add_argument('--set_itk_global_default_number_of_threads',
                   default=1,
                   type=int,
                   help='Fix number of threads used by ANTs')

    p.add_argument('--set_mkl_num_threads',
                   type=int,
                   default=1,
                   help='Fix number of MKL threads')

    p.add_argument('--fs_license', help='Freesurfer license.txt')

    p.add_argument('--coverage', help='Run connectomemapper3 with coverage', action='store_true')

    p.add_argument('--notrack', help='Do not send event to Google analytics to report BIDS App execution, which is enabled by default.', action='store_true')

    # p.add_argument('--skip_bids_validator', help='Whether or not to perform BIDS dataset validation',
    #                    action='store_true')
    p.add_argument('-v', '--version', action='version',
                   version='BIDS-App Connectome Mapper version {} \nRelease date: {}'.format(__version__, __release_date__))
    return p
