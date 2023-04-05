# -*- coding: utf-8 -*-
import asyncio

list_tasks = []

async def run(cmd):
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await proc.communicate()
    print(f'[{cmd!r} exited with {proc.returncode}]')
    if stdout:
        print(f'[stdout] {stdout.decode()}')
    if stderr:
        print(f'[stderr] {stderr.decode()}')

async def main():
    global list_tasks
    tasks=[]
    for arg in list_tasks:
        # создаем задачи
        task = run(*arg)
        # складываем задачи в список
        tasks.append(task)
    L = await asyncio.gather(*tasks)
    #print(L)

def async_resize_run(new_tasks):    
    global list_tasks
    list_tasks.clear()
    for task in new_tasks:
        list_tasks.append(task)
    asyncio.run(main())
