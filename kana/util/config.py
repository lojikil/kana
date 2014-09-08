

def flat_config(cfg):
    """ Take a ConfigReader.SafeConfigReader and flatten it into a dict.
    This will also atempt to reify objects into their correct type; so
    the strings "True" and "False" will be converted into their Boolean
    representations, and integers will be converted into ints. It's not
    terribly smart at the moment, but should be enough for CTF purposes
    """
    res = {}
    for section in cfg.sections():
        for option in cfg.options(section):
            key = '{0}.{1}'.format(section, option)
            val = cfg.get(section, option)
            if val.lower() == "true":
                val = True
            elif val.lower() == 'false':
                val = False
            elif val.isdigit():
                val = int(val)
            res[key] = val
    return res
