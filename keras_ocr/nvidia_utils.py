#!/usr/bin/env python3
import re
from typing import *
from typing import Match
import subprocess

def _nvidia_smi() -> List[str]:
    '''
    Example:
        >>> nvidia_smi()
        ['Fri Feb 26 12:12:13 2021       ',
         '+-----------------------------------------------------------------------------+',
         '| NVIDIA-SMI 460.32.03    Driver Version: 460.32.03    CUDA Version: 11.2     |',
         '|-------------------------------+----------------------+----------------------+',
         '| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |',
         '| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |',
         '|                               |                      |               MIG M. |',
         '|===============================+======================+======================|',
         '|   0  Tesla K80           On   | 00000001:00:00.0 Off |                    0 |',
         '| N/A   70C    P0    62W / 149W |    266MiB / 11441MiB |      0%      Default |',
         '|                               |                      |                  N/A |',
         '+-------------------------------+----------------------+----------------------+',
         '                                                                               ',
         '+-----------------------------------------------------------------------------+',
         '| Processes:                                                                  |',
         '|  GPU   GI   CI        PID   Type   Process name                  GPU Memory |',
         '|        ID   ID                                                   Usage      |',
         '|=============================================================================|',
         '+-----------------------------------------------------------------------------+',
         '']
    '''
    return subprocess.check_output(['nvidia-smi'], universal_newlines=True).split('\n')

def _get_used_and_total_vram_from_match(match: Match[str]):
    '''
    Example:
        >>> match
        <_sre.SRE_Match object; span=(37, 54), match='266MiB / 11441MiB'>
        >>> get_used_and_total_from_match(match)
        (266, 11441)
    '''
    usage: Union[str, Tuple] = match.group()
    assert isinstance(usage, str), f'match has invalid form: {usage}'
    used, total = usage.split(' / ')
    used, total = int(used[:-3]), int(total[:-3])
    return used, total

def get_free_vram():
    '''Return free VRAM in megabytes'''
    lines: List[str] = _nvidia_smi()
    vram_lines: List[Union[Match, None]] = [
        re.search('[0-9]*MiB / [0-9]*MiB', l) for l in lines
    ]
    vram_lines = [l for l in vram_lines if l is not None]
    
    assert len(vram_lines) == 1, f'nvidia_smi is in invalid format. {lines}'
    
    used: int
    total: int
    used, total = _get_used_and_total_vram_from_match(vram_lines[0])
    return total - used
