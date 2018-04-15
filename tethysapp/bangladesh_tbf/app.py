from tethys_sdk.base import TethysAppBase, url_map_maker
from tethys_sdk.app_settings import SpatialDatasetServiceSetting

class BangladeshTbf(TethysAppBase):
    """
    Tethys app class for Bangladesh Tbf.
    """
    name = 'Streamflow Prediction for Bangladesh'
    index = 'bangladesh_tbf:home'
    icon = 'bangladesh_tbf/images/ICIMOD_Logo_White.gif'
    package = 'bangladesh_tbf'
    root_url = 'bangladesh-tbf'
    color = '#6E362A'
    description = 'Place a brief description of your app here.'
    tags = ''
    enable_feedback = False
    feedback_emails = []

    def url_maps(self):
        """
        Add controllers
        """
        UrlMap = url_map_maker(self.root_url)

        url_maps = (
            UrlMap(
                name='home',
                url=r'bangladesh-tbf/',
                controller='bangladesh_tbf.controllers.home'),
            UrlMap(
                name='plotMap',
                url=r'bangladesh-tbf/plotMap',
                controller='bangladesh_tbf.controllers.plotMap'),
            UrlMap(name='Ganges',
                   url=r'^bangladesh-tbf/Ganges/',
                   controller='bangladesh_tbf.controllers.ganges'),
        )

        return url_maps

    def spatial_dataset_service_settings(self):
        """
        Example spatial_dataset_service_settings method.
        """
        sds_settings = (
            SpatialDatasetServiceSetting(
                name='mainGeoserver',
                description='spatial dataset service for app to use',
                engine=SpatialDatasetServiceSetting.GEOSERVER,
                required=True,
            ),
        )

        return sds_settings

