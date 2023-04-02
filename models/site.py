from sql_alchemy import banco
class SiteModel(banco.Model):
    __tablename__ = 'sites'

    site_id = banco.Column(banco.Integer, primary_key=True)
    url = banco.Column(banco.String(80))
    name = banco.Column(banco.String(50))
    hoteis = banco.relationship("HotelModel")


    def __init__(self, name, url):
        self.name = name
        self.url = url

    def json(self):
        return {
            "site_id": self.site_id,
            "url": self.url,
            "name": self.name,
            "hoteis": [hotel.json() for hotel in self.hoteis]
        }
    
    @classmethod
    def find_site(cls, name):
        site = cls.query.filter_by(name=name).first()
        if site: 
            return site
        return None
    
    def save_site(self):
        banco.session.add(self)
        banco.session.commit()

    def update_site(self, url, name):
        self.url = url
        self.name = name

    def delete_site(self):
        [hotel.delete_hotel() for hotel in self.hoteis]
        banco.session.delete(self)
        banco.session.commit()
    
