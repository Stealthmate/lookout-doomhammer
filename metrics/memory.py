import psutil

def _ram():
    memory = psutil.virtual_memory()
    return {
        'available': memory.available,
        'used': memory.used
    }

def _swap():
    swap = psutil.swap_memory()
    return {
        'available': swap.free,
        'used': swap.used
    }

def memory_metrics():
    return {
        'ram': _ram(),
        'swap': _swap(),
    }
