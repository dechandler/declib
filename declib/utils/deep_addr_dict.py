

class DeepAddressableDictlike:
    """
    Frontend object for a nested dict that can address and interact
    with  its subdicts

    Only dicts are resolved - list items are not addressable

    """
    def __init__(self):

        self._object_dict = {}

        # Plug various dict methods from _object_dict into the class
        # Maybe I should just be inheriting dict? seems maybe bad practice
        for method in ['keys', 'values', 'items']:
            self.__setattr__(
                method, self._object_dict.__getattribute__(method)
            )

    def __getitem__(self, dict_path):
        """
        Key is period-delimited address path

        """
        return self.get(dict_path)

    def __setitem__(self, dict_path, value):
        """
        Key is period-delimited address path

        """
        self.set(dict_path, value)

    def __iter__(self):
        for key, value in self._object_dict.items():
            yield key, value


    def get(self, dict_path, default=None):
        """
        
        dict_path can be list or dot-delimited string

        """
        if type(dict_path) == str:
            dict_path = dict_path.split('.')

        return self._deep_get(self._object_dict, dict_path, default)

    def set(self, dict_path, value):
        """
        
        dict_path can be list or dot-delimited string

        """
        if type(dict_path) == str:
            dict_path = dict_path.split('.')

        return self._deep_set(self._object_dict, dict_path, value)

    def update(self, update_dict):
        """
        update_dict can also be a list of tuple pairs
        """
        update_dict_deep_items = self._deep_items(dict(update_dict))
        for dict_path, value in update_dict_deep_items:
            self._deep_set(self._object_dict, dict_path, value)



    def _deep_get(self, this_dict, dict_path, default):

        if not dict_path:
            return this_dict
        
        key = dict_path.pop(0)
        try:
            return self._deep_get(this_dict[key], dict_path, default)
        except KeyError:
            return default

    def _deep_set(self, this_dict, dict_path, value):

        key = dict_path.pop(0)

        if not dict_path:
            this_dict[key] = value
            return

        if key not in this_dict:
            this_dict[key] = {}

        self._deep_set(this_dict[key], dict_path, value)

    def _deep_items(this_dict, parent_dict_path):

        subitems = []
        for key, value in this_dict.items():
            dict_path = parent_dict_path + [key]
            if type(value) is not dict:
                subitems.append([dict_path, value])
                continue
            subitems.extend(self._deep_items(value, dict_path))
        return subitems
