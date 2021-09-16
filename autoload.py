import importlib

class autoload(object):
    def __init__(self, __name__):
        super(autoload, self).__init__()
        self.wrapped_name = __name__
        self.wrapped = sys.modules[__name__]

    def __getattr__(self, name):
        try:
            return getattr(self.wrapped, name)
        except AttributeError:

            class Modules:

                module_path = 'Modules'

                def __getattribute__(cls, name):
                    def g():
                        module = Modules.module_path+"."+name+".main"
                        module_dir = importlib.import_module(module)
                        module = getattr(module_dir, name)
                        return module
                    return g()

            return Modules()

if __name__ != "__main__":
    import sys
    sys.modules[__name__] = autoload(__name__)