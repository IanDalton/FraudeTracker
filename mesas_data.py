import json,asyncio,aiohttp,os,time


with open('mesas.txt','r') as f:
    mesas = f.readlines()
    mesas = [mesa.strip() for mesa in mesas]
    mesas = set(mesas)

with open('valid_proxies.txt','r') as f:
    proxies = f.readlines()
    proxies = [proxy.strip() for proxy in proxies]




def get_image(mesa:str, session:aiohttp.ClientSession):
    url = f'https://resultados.gob.ar/backend-difu/scope/data/getTiff/{mesa}'
    pass

# https://resultados.gob.ar/backend-difu/scope/data/getTiff/{mesa}

async def get_mesa_info(mesa:str, session:aiohttp.ClientSession, save:bool=True):
    url = f'https://resultados.gob.ar/backend-difu/scope/data/getScopeData/{mesa}/1'
    got_data = False
    while not got_data:
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    if save:
                        with open(f'mesas/{mesa}.json','w') as f:
                            json.dump(data,f)
                    return data
                elif response.status == 403:
                    print(f'IP suspended, waiting for 1 minute...')
                    time.sleep(60)
                else:
                    print(f'Error {response.status}, retrying...')
                    time.sleep(5)
        except aiohttp.client_exceptions.ContentTypeError:
            print(f'Unexpected content type, retrying...')
            time.sleep(60)

async def main():
    global mesas
    #if mesas folder does not exist, create it
    if not os.path.exists('mesas'):
        os.mkdir('mesas')
    #get all the mesas in mesas folder and remove the names that are on the set
    mesas_folder = os.listdir('mesas')
    mesas_folder = [mesa.split('.')[0] for mesa in mesas_folder]
    mesas = mesas.difference(set(mesas_folder))
    print(len(mesas),'remaining')
    
    async with aiohttp.ClientSession() as session:
        tasks = []
        for mesa in mesas:
            task = asyncio.create_task(get_mesa_info(mesa, session))
            tasks.append(task)
        results = await asyncio.gather(*tasks)
        print(results)
   
asyncio.run(main())