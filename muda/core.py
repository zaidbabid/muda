#!/usr/bin/env python
# -*- coding: utf-8 -*-
# CREATED:2015-02-01 19:25:59 by Brian McFee <brian.mcfee@nyu.edu>
'''Core functionality for muda'''

import jams
import librosa

from .base import *
import warnings


def jam_pack(jam, **kwargs):
    '''Pack data into a jams sandbox.

    Parameters
    ----------
    jam : jams.JAMS
        A JAMS object

    Examples
    --------

    >>> y, sr = librosa.load(librosa.util.example_audio_file())
    >>> jam = jams.JAMS()
    >>> muda.jam_pack(jam, y=y, sr=sr)
    >>> print muda
    '''

    if not hasattr(jam.sandbox, 'muda'):
        jam.sandbox.muda = dict(history=[], state=[])

    jam.sandbox.muda.update(kwargs)

    return jam


def jam_pop(jam, *keys):
    '''Remove specified keys from the jams muda sandbox.

    Parameters
    ----------
    keys : one or more positional arguments
        Keys to be purged from the sandbox

    Returns
    -------
    values : dict
        Dictionary containing the popped values
    '''

    if not hasattr(jam.sandbox, 'muda'):
        warnings.warn('No muda sandbox found in jam')
        return

    output = {}

    for key in keys:
        output[key] = jam.sandbox.muda.pop(key)

    return output


def load_jam_audio(jam_in, audio_file, **kwargs):
    '''Load a jam and pack it with audio.

    Parameters
    ----------
    jam_in : str or jams.JAMS
        JAM filename to load

    audio_file : str
        Audio filename to load

    kwargs : additional keyword arguments
        See `librosa.load`

    Returns
    -------
    jam : jams.JAMS
        A jams object with audio data in the top-level sandbox

    '''

    if isinstance(jam_in, six.string_types):
        jam = jams.load(jam_in)
    elif isinstance(jam_in, jams.JAMS):
        jam = jam_in
    else:
        raise TypeError('Invalid input type: ' + type(jam_in))

    y, sr = librosa.load(audio_file, **kwargs)

    return jam_pack(jam, y=y, sr=sr)
