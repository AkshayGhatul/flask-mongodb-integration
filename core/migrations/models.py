from collections import OrderedDict

__MODEL_DICT__ = OrderedDict()

class Model:
    def __init_subclass__(cls, **kwargs):
        assert "name" in kwargs
        super().__init_subclass__()
        if kwargs["name"] in __MODEL_DICT__:
            raise ValueError("Name %s already registered!" % name)
        __MODEL_DICT__[kwargs["name"]] = cls