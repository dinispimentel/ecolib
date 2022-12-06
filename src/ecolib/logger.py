import logging as lg



lg.getLogger("requests").setLevel(lg.WARNING)
lg.basicConfig(filename='logging/filtering.log', format='%(asctime)s [%(levelname)s] %(message)s',
               datefmt='%m/%d/%Y %I:%M:%S %p', encoding='utf-8', level=lg.DEBUG)






