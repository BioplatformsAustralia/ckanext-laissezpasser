[![Tests](https://github.com/BioplatformsAustralia/ckanext-laissezpasser/workflows/Tests/badge.svg?branch=main)](https://github.com/BioplatformsAustralia/ckanext-laissezpasser/actions)

# ckanext-laissezpasser

This extension expands on the flexible resource permissioning provided by 
ckanext-initiatives
https://github.com/BioplatformsAustralia/ckanext-initiatives.
It enables systems administrators to be able to provide time limited 
access to particular users to download specific datasets irrespective 
of if they are members of the relevant project.

The extension intercepts the same authentication calls as 
ckanext-initiatives and is implemented as a chained auth function.

A frontend and API calls are implmented to view, add and remove passes.

The name of the extension is derived from the French

    laissez-passer

    noun

    a permit; pass, especially one issued in lieu of a passport.

## Requirements

Compatibility with core CKAN versions:

| CKAN version    | Compatible?   |
| --------------- | ------------- |
| 2.8 and earlier | not tested    |
| 2.9             | yes           |
| 2.10            | not yet       |
| 2.11            | not yet       |

It is strongly suggested to use this extension with

https://github.com/BioplatformsAustralia/ckanext-initiatives

## Installation

**TODO:** Add any additional install steps to the list below.
   For example installing any non-Python dependencies or adding any required
   config settings.

To install ckanext-laissezpasser:

1. Activate your CKAN virtual environment, for example:

     . /usr/lib/ckan/default/bin/activate

2. Clone the source and install it on the virtualenv

    git clone https://github.com/BioplatformsAustralia/ckanext-laissezpasser.git
    cd ckanext-laissezpasser
    pip install -e .
	pip install -r requirements.txt

3. Add `laissezpasser` to the `ckan.plugins` setting in your CKAN
   config file (by default the config file is located at
   `/etc/ckan/default/ckan.ini`).

4. Restart CKAN. For example if you've deployed CKAN with Apache on Ubuntu:

     sudo service apache2 reload

5. Create the necessary database tables

     ckan -c /etc/ckan/default/ckan.ini db upgrade -p laissezpasser



## Config settings

None at present

**TODO:** Document any optional config settings here. For example:

	# The minimum number of hours to wait before re-checking a resource
	# (optional, default: 24).
	ckanext.laissezpasser.some_setting = some_default_value


## Developer installation

To install ckanext-laissezpasser for development, activate your CKAN virtualenv and
do:

    git clone https://github.com/BioplatformsAustralia/ckanext-laissezpasser.git
    cd ckanext-laissezpasser
    python setup.py develop
    pip install -r dev-requirements.txt


## Tests

To run the tests, do:

    pytest --ckan-ini=test.ini


## Releasing a new version of ckanext-laissezpasser

If ckanext-laissezpasser should be available on PyPI you can follow these steps to publish a new version:

1. Update the version number in the `setup.py` file. See [PEP 440](http://legacy.python.org/dev/peps/pep-0440/#public-version-identifiers) for how to choose version numbers.

2. Make sure you have the latest version of necessary packages:

    pip install --upgrade setuptools wheel twine

3. Create a source and binary distributions of the new version:

       python setup.py sdist bdist_wheel && twine check dist/*

   Fix any errors you get.

4. Upload the source distribution to PyPI:

       twine upload dist/*

5. Commit any outstanding changes:

       git commit -a
       git push

6. Tag the new release of the project on GitHub with the version number from
   the `setup.py` file. For example if the version number in `setup.py` is
   0.0.1 then do:

       git tag 0.0.1
       git push --tags

## License

[AGPL](https://www.gnu.org/licenses/agpl-3.0.en.html)
