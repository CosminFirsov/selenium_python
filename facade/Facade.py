from singleton_decorator import singleton

@singleton
class Facade():
    def test(self):
        print('Facade')