def set_transformation(self, attr_name, attr_value):
    setattr(getattr(self.PD, attr_name), 'Value', attr_value)
    
def get_transformation(self, attr_name):
    return getattr(getattr(self.PD, attr_name), 'Value')
