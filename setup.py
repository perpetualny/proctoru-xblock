"""Setup for proctoru XBlock."""

import os
from setuptools import setup


def package_data(pkg, roots):
    """Generic function to find package_data.

    All of the files under each of the `roots` will be declared as package
    data for package `pkg`.

    """
    data = []
    for root in roots:
        for dirname, _, files in os.walk(os.path.join(pkg, root)):
            for fname in files:
                data.append(os.path.relpath(os.path.join(dirname, fname), pkg))

    return {pkg: data}


setup(
    name='proctoru-xblock',
    version='1.0.0',
    description='ProctorU is an online proctoring company that allows a candidate to take their exam from home',
    packages=[
        'proctoru',
	'proctoru.templatetags',
    ],
    install_requires=[
        'XBlock',
    ],
    entry_points={
        'xblock.v1': [
            'proctoru = proctoru.proctoru:ProctorUXBlock',
        ]
    },
    package_data=package_data("proctoru", ["static", "public"]),
)
