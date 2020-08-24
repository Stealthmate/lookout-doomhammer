import psutil

def cpu_metrics():
    return {
        'util': psutil.cpu_percent(interval=0.1, percpu=True),
        'temp': psutil.sensors_temperatures()['asus'][0].current
    }
