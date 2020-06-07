from arknights_farmer.utils.logger import Logger

Logger.log(f'this is info with fstring {2+2}')
Logger.log('this is info')
Logger.log('this is warning', 'warn')
Logger.log('this is error', 'error')

Logger.log_debug('this is debug')