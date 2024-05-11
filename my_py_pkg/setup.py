import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'my_py_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share',package_name,'launch'),glob(os.path.join('launch','*launch.[pxy][yma]*')))
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='pi',
    maintainer_email='pi@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
		"py_node = my_py_pkg.my_first_node:main",
		#"py_oop_node = my_py_pkg.my_first_oop_node:main",
		"py_pub_node = my_py_pkg.py_simple_pub:main",
		"py_sub_node = my_py_pkg.py_simple_sub:main",
		"service = my_py_pkg.service_member_function:main",
        	"client = my_py_pkg.client_member_function:main",
		"py_gui_node = my_py_pkg.gui:main",
		"py_action_node = my_py_pkg.action:main",
		"py_control_node = my_py_pkg.control:main",
		"py_ai_follow_node = my_py_pkg.AIFollow:main",
		"py_ai_pos_node = my_py_pkg.AIPos2:main",
		"lifecycle_test = my_py_pkg.lifecycle_test:main",
		"py_sound_control_node = my_py_pkg.sound_control:main",
		"py_ai_sayhi_node = my_py_pkg.AISayHi:main",
        ],
    },
)
