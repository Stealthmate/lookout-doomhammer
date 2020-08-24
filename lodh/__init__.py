import asyncio
import websockets
import psutil
import json
from time import sleep
from metrics.memory import memory_metrics
from metrics.cpu import cpu_metrics

def _top_users(n=3):
    ps = list(psutil.process_iter(['pid', 'name', 'memory_info']))
    ps = sorted(ps, key=lambda x: -x.info['memory_info'].rss)[:n]
    return [
        {
            'pid': p.info['pid'],
            'name': p.info['name'],
            'rss': p.info['memory_info'].rss
        }
        for p in ps
    ]

async def serve(websocket, path):
    t = 40
    while True:
        ps = list(psutil.process_iter(['pid', 'name', 'memory_info', 'cpu_percent']))

        ps_mem = sorted(ps, key=lambda x: -x.info['memory_info'].rss)[:3]
        ps_cpu = sorted(ps, key=lambda x: -x.info['cpu_percent'])[:3]

        await websocket.send(json.dumps({
            'memory': {
                **memory_metrics(),
                'topUsers': [
                    {
                        'pid': p.info['pid'],
                        'name': p.info['name'],
                        'rss': p.info['memory_info'].rss
                    } for p in ps_mem
                ]
            },
            'cpu': {
                **cpu_metrics(),
                'topUsers': [
                    {
                        'pid': p.info['pid'],
                        'name': p.info['name'],
                        'cpu': p.info['cpu_percent']
                    } for p in ps_cpu
                ],
            }
        }))

        sleep(0.5)

def run(host="localhost", port=8765):
    start_server = websockets.serve(serve, host, port)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
