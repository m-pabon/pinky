class Environment:
    def __init__(self, parent=None):
        self.vars = {}
        self.funcs = {}
        self.parent = parent

    def get_var(self, name):
        # Search the current environment and all parent environments for a variable name, return None if we don't find any
        value = self.vars.get(name)
        if not value and self.parent:
            value = self.parent.get_var(name)
        return value

    def set_var(self, name, value):
       # Store a value in the environment (dynamically updating an existing name or creating a new entry in the dictionary)
        original_environment = self
        while self:
            if name in self.vars:
                self.vars[name] = value
                return value
            self = self.parent
        original_environment.vars[name] = value

    def get_func(self, name):
        value = self.funcs.get(name)
        if not value and self.parent:
            value = self.parent.get_func(name)
        return value

    def set_func(self, name, value):
        self.funcs[name] = value
        
    def new_env(self):
        return Environment(parent=self)

    def set_local(self, name, value):
        self.vars[name] = value
