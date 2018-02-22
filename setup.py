from setuptools import setup

setup(
    name='ygg_scraping',
    version='0.2',
    packages=['db', 'services', 'settings', '.'],
    url='https://github.com/girardNicolas/ygg_scraping',
    license='',
    author='Banchaos, Lulububu',
    author_email='',
    description='',
    install_requires=['requests', 'flask_cors', 'flask', 'bs4'],
    package_data={'db': ['sql/*.sql']},
    bdist="zip"
)
