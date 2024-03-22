from abc import ABC, abstractmethod

class BaseRepository(ABC):

    @abstractmethod
    def add(self, entity, commit = False):
        pass

    @abstractmethod
    def get_by_identifier(self, identifier):
        pass

    @abstractmethod
    def list(self):
        pass
    
    @abstractmethod
    def update(self,identifier, new_value, commit= False):
        pass

    @abstractmethod
    def remove(self, entity):
        pass
