import asyncio
import _asyncio
import config_validator
from datetime import datetime
import json

junction_data_open = open('bhel.json')
junction_data = json.load(junction_data_open)

async def main(junction_data) :
    value = await config_validator.validation_manager(junction_data)
    print(value)
    


asyncio.run(main(junction_data))
