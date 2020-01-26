from setuptools import setup

package_name = 'wiper'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='gbf',
    maintainer_email='gbf@advantec.com',
    description='Windshield wiper delay control',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'pulser = wiper.relays:main',
        ],
    },
)
