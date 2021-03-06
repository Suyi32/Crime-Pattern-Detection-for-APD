import ConfigParser

# Global Variables

class Config:
    
    def __init__(self, ini_path):
        self.ini_path = ini_path
        self.conf = ConfigParser.ConfigParser()
        self.conf.read(self.ini_path)

    def config_section_map(self, section):
        _dict = {}
        options = self.conf.options(section)
        for option in options:
            try:
                _dict[option] = self.conf.get(section, option)
                if _dict[option] == -1:
                    DebugPrint("skip: %s" % option)
            except:
                print("exception on %s!" % option)
                _dict[option] = None
        return _dict