import aiohttp
import asyncio
import json
import os
import base64
from concurrent.futures import ThreadPoolExecutor


async def download_image(mesa:str, session:aiohttp.ClientSession):
    url = f'https://resultados.gob.ar/backend-difu/scope/data/getTiff/{mesa}'
    try:
        async with session.get(url) as response:
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
    except aiohttp.client_exceptions.ContentTypeError:
        print(f'La mesa {mesa} no pudo ser descargada exitosamente')
        return mesa

def process_mesa(mesa:str):
    def sospechoso():
        print(f'{mesa} sospechoso')
        suspected_values.append(data["id"]["idAmbito"]["codigo"])
    with open(f'mesas/{mesa}','r') as f:
        
        data:dict = json.load(f)
        suspected_values = []
        electores = data.get('electores',0)
        sobres = data.get('sobres',0)
        nulos = data.get('nulos',0)
        blancos = data.get('blancos',0)
        impugnado = data.get('impugnado',0)
        votos = 0
        for partido in data.get('partidos'):
            votos += partido.get('votos',0)
       
        # si hay diferencia de mas de 5 electores y sobres se concidera sospechoso
        if electores - sobres > 5 or sobres - electores > 5:
            sospechoso()
        elif sobres == nulos + blancos+impugnado:
            sospechoso()
        
            
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
            print(len(suspected_values),'suspected values')
            mesas_malas = []
            for value in suspected_values:
                mesas_malas.append(await download_image(value, session))
            print(len(mesas_malas))
    with open('mesas_malas.txt','w') as f:
        f.write('\n'.join(mesas_malas))

            

if __name__ == '__main__':
    asyncio.run(main())
    