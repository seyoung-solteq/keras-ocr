import tensorflow as tf
from . import nvidia_utils

class GPUNotFoundError(Exception):
    '''Raise when TF cannot locate a GPU.
    '''    

class OutOfVRAMError(Exception):
    '''Raise when user inquires too much VRAM.
    '''    

def set_gpu_memory_dynamic_growth():
    '''Tell TF to use only the required amount of VRAM.

    Without this, TF will occupy as much VRAM as possible.
    
    - https://www.tensorflow.org/guide/gpu#limiting_gpu_memory_growth
    '''
    gpus = tf.config.experimental.list_physical_devices('GPU')
    if not gpus:
        raise GPUNotFoundError(f'Tensorflow cannot find a GPU.')

    try:
        # Currently, memory growth needs to be the same across GPUs
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)

        logical_gpus = tf.config.experimental.list_logical_devices('GPU')
        print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPUs")
    except RuntimeError as e:
        # Memory growth must be set before GPUs have been initialized
        print(e)
    


def set_gpu_memory_limit(memory_limit: int):
    free_vram: int = nvidia_utils.get_free_vram()
    if free_vram < memory_limit:
        raise OutOfVRAMError(f'Inquired too much VRAM: {memory_limit} MiB. Available: {free_vram} MiB')
        
    gpus = tf.config.list_physical_devices('GPU')
    if not gpus:
        raise GPUNotFoundError(f'Tensorflow cannot find a GPU.')
    tf.config.experimental.set_virtual_device_configuration(
        gpus[0],
        [tf.config.experimental.VirtualDeviceConfiguration(memory_limit=memory_limit)]
    )