from wwpdb.utils.config.ConfigInfo import getSiteId


def get_queue_name(site_id=None):
    if not site_id:
        site_id = getSiteId()
    queue_name = 'contentws_queue_{}'.format(site_id)
    return queue_name


def get_routing_key():
    return "contentws_requests"


def get_exchange_name():
    return 'biocurationws_exchange'


def get_exchange_topic():
    return "topic"
