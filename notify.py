from typing import Literal
from plyer import notification

def notify(ntype: Literal['change','timeout','invalid']):
    if ntype=='change':
        notification.notify(
            title='Visual Change', message='Observer noticed change in pixel value', app_name='NotifyAnything'
        )
    elif ntype=='timeout':
        notification.notify(
            title='Timeout', message='Observer noticed no changes within timeout, increase timeout if needed', app_name='NotifyAnything'
        )
    elif ntype=='invalid':
        notification.notify(
            title='Invalid Region', message='Invalid region selected, select a larger region', app_name='NotifyAnything'
        )
