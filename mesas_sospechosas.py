import aiohttp
import asyncio
import json
import os
import base64
from concurrent.futures import ThreadPoolExecutor


async def download_image(mesa:str, session:aiohttp.ClientSession):
    url = f'https://resultados.gob.ar/backend-difu/scope/data/getTiff/{mesa}'
    print(url)
    async with session.get(url) as response:
        print(response.status)
        if response.status == 200:
            data:dict = await response.json()
            data:str = data.get('encodingBinary')
            image_data = base64.b64decode(data)
            with open(f'telegramas/{mesa}.tiff', 'wb') as f:
                f.write(image_data)
            return image_data
        else:
            print(f'Error {response.status}, retrying...')
            return None

def process_mesa(mesa:str):
    with open(f'mesas/{mesa}','r') as f:
        data:dict = json.load(f)
        suspected_values = []
        electores = data.get('electores')
        sobres = data.get('sobres')
        nulos = data.get('nulos')
        blancos = data.get('blancos')
        impugnado = data.get('impugnado')
        total = data.get('totalVotos')
        for partido in data.get('partidos'):
            if partido['code'] == '135':
                milei = partido
            elif partido['code'] == '134':
                massa = partido
        if milei['votos']==0 and massa['votos']!=0:
            print(f'{mesa} sospechosa')
            suspected_values.append(data["id"]["idAmbito"]["codigo"])
        return suspected_values
    


async def main():
    with ThreadPoolExecutor(max_workers=16) as executor:
        async with aiohttp.ClientSession() as session:
            loop = asyncio.get_event_loop()
            tasks = []
            for mesa in os.listdir('mesas'):
                task = loop.run_in_executor(executor, process_mesa, mesa)
                tasks.append(task)
            results = await asyncio.gather(*tasks)
            print('done')
            suspected_values = set([value for sublist in results for value in sublist])
            for value in suspected_values:
                await download_image(value, session)

            

if __name__ == '__main__':
    asyncio.run(main())
    