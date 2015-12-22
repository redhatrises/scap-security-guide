#!/usr/bin/python

import os
import re
import sys
import shutil
import fileinput
from distutils.util import strtobool
from optparse import OptionParser, OptionGroup

SSGTOPDIR = "../../"
SSG_BUILD = "../build_templates"

input_list = ['auxiliary', 'intro', 'profiles']
oval_list = ['platform', 'oval_5.11']
remediations_list = ['bash']
xccdf_list = ['services', 'system', 'system/accounts', 'system/accounts/restrictions',
             'xccdf/system/network', 'system/permissions', 'system/software']

input_dir = {'input': input_list,
             'input/oval': oval_list,
             'input/remediations': remediations_list,
             'input/xccdf': xccdf_list}
other_dirs = ['transforms', 'utils']
additional_dirs = ['tests', 'kickstart']


python_templates = {'transforms': 'cce_extract.py,splitchecks.py,xccdf2csv-stig.py',
                    'utils': 'sync-alt-titles.py,verify-cce.py,verify-input-sanity.py',
                    'input/oval': 'testcheck.py',
                    'input/oval/oval_5.11': 'testcheck.py'}

readme_templates = {'README_utils': ['utils', 'README'],
                    'README_auxiliary': ['input/auxiliary', 'README'],
                    'README_bash': ['input/remediations/bash', 'README']}

makefile_templates = {'Makefile_new': 'Makefile'}

xslt_templates = {'input': 'guide.xslt'}
xml_templates = {'input': 'guide.xml',
                 'input/profiles': 'common.xml',
                 'input/intro': 'intro.xml',
                 'input/oval/platform': 'cpe-dictionary.xml'}


def create_directies(new_product, product, aux_dirs):
    product_list = []

    for key, value in input_dir.iteritems():
        for dirs in value:
            product_list.append(new_product + '/' + key + '/' + dirs)

    for other in other_dirs:
        product_list.append(new_product + '/' + other)

    for aux in aux_dirs:
        product_list.append(new_product + '/' + aux)

    for listing in product_list:
        if not os.path.exists(listing):
            print("    Creating %s" % listing)
            os.makedirs(listing, 0755)


def copy_file(template, file_to_copy, mode=False):
    try:
        shutil.copyfile(template, file_to_copy)
    except shutil.Error as e:
        if re.match('.*the same file', str(e)):
            pass

    if not mode:
        pass
    else:
        os.chmod(file_to_copy, mode)


def update_to_product(template_file, find, replace):
    for line in fileinput.input(template_file, inplace=True):
        print(line.replace(find, replace).rstrip('\n'))


def add_templates(new_product, version, product):
        # Add Makefiles to new product tree
        for makefiles in makefile_templates:
            for makefile in makefile_templates[makefiles].split(","):
                makefile_copy_file =  new_product + '/' + makefile
                makefile_template = SSG_BUILD + '/' + makefiles

                print("    Setting up %s" % makefile_copy_file)
                copy_file(makefile_template, makefile_copy_file, 0644)
                update_to_product(makefile_copy_file, 'SSG_NEW_PRODUCT', product + version)

        # Add python scripts to new product tree
        for python_scripts in python_templates:
            for python_script in python_templates[python_scripts].split(","):
                python_copy_file = new_product + '/' + python_scripts + '/' + python_script
                python_template = SSG_BUILD + '/' + python_script

                print("    Setting up %s" % python_copy_file)
                copy_file(python_template, python_copy_file, 0755)

        # Add readme files to new product tree
        for readmes in readme_templates:
            directory = new_product + '/' + readme_templates[readmes][0]
            readme_file = readme_templates[readmes][1]
            readme = directory + '/' + readme_file
            if os.path.exists(directory):
                readme_template = SSG_BUILD + '/' + readmes
                print("    Setting up %s" % readme)
                copy_file(readme_template, readme, 0644)

        # Add xslt transforms to new product tree
        for xslt_transforms in xslt_templates:
            for xslt in xslt_templates[xslt_transforms].split(","):
                xslt_file_copy = new_product + '/' + xslt_transforms + '/' + xslt
                xslt_template = SSG_BUILD + '/' + xslt

                print("    Setting up %s" % xslt_file_copy)
                copy_file(xslt_template, xslt_file_copy, 0644)

        # Add xml files to new product tree
        for xml_files in xml_templates:
            for xml in xml_templates[xml_files].split(","):
                xml_template = SSG_BUILD + '/' + xml

                if 'cpe-dictionary' in xml:
                    xml = product + version + '-' + xml

                xml_file_copy = new_product + '/' + xml_files + '/' + xml

                print("    Setting up %s" % xml_file_copy)
                copy_file(xml_template, xml_file_copy, 0644)


def create_product(options):
    aux_remove = []
    create = ''

    if not options.product:
        product = raw_input("Enter the name of the product to add (e.g. Debian, RHEL, Openstack, etc.): ")
    else:
        product = options.product

    if not options.product_versions:
        versions = raw_input("Enter the product version(s) that will be targeted.\n"
                             "Use commas to separate if multiple versions (e.g. 6,7,8): ")
        versions = versions.split(",")
    else:
        versions = options.product_versions

    if not options.aux:
        for aux in additional_dirs:
            try:
                create = strtobool(raw_input("Do you want to create the '%s' directory? (Y/N): " % aux).lower())
            except ValueError as e:
                if re.match("invalid truth value ''", str(e)):
                    print("Skipping...")
            if not create:
                aux_remove.append(aux)
        aux_dirs = [n for n in additional_dirs if n not in aux_remove]
    else:
        aux_dirs = additional_dirs
    
    for version in versions:
        version = str(version)
        new_product = SSGTOPDIR + product + '/' + version
    
        print("\nCreating new directory structure for product '%s'" % product)    
        create_directies(new_product, product, aux_dirs)

        print("\nAdding project template files...\n")
        add_templates(new_product, version, product)

    print("\nComplete!\n")


def remove_product(options):
    versions = 0

    if not options.product:
        product = raw_input("Enter the name of the product to remove (e.g. Debian, RHEL, Openstack, etc.): ")
    else:
        product = options.product

    if options.product_versions:
        versions = options.product_versions

    if not versions or len(versions) < 2:
        product_path = SSGTOPDIR + product
        if not os.path.exists(product_path):
            sys.exit("\nThe '%s' product tree does not exist! Exiting..." % product)
        else:
            print("\nRemoving '%s' from the SSG development tree" % product)
            shutil.rmtree(product_path)
    else:
        for version in versions:
            
            product_path = SSGTOPDIR + product + "/" + str(version)
            if not os.path.exists(product_path):
                print("The '%s' product version '%s' does not exist! Skipping..." % (product, str(version)))
            else:
                remove = strtobool(raw_input("\nThis operation is IRREVERSIBLE! Are you sure you want to continue? (Y/N): ").lower())
                if not remove:
                    sys.exit(1)
                else:
                    print("Removing '%s' version %s from the SSG development tree" % (product, str(version)))
                    shutil.rmtree(product_path)


def parse_options():
    usage = "usage: %prog [OPTIONS]"
    parser = OptionParser(usage=usage)
    parser.add_option("-p", "--product", default=False,
                      action="store", dest="product",
                      help="name of new SSG product")
    parser.add_option("-v", "--product-version", default=[], metavar="product_version",
                      action="append", dest="product_versions", type="int",
                      help="version of new SSG product")
    
    create_group = OptionGroup(parser, "Create SSG Product")
    create_group.add_option("-c", "--create", default=False,
                      action="store_true", dest="create",
                      help="create new product in SSG development tree")
    create_group.add_option("-o", "--optional", dest="aux", action="store_true",
                      help="create 'tests' and 'kickstart' directories")
    parser.add_option_group(create_group)

    remove_group = OptionGroup(parser, "Remove SSG Product")
    remove_group.add_option("-d", "--delete", default=False,
                      action="store_true", dest="remove",
                      help="remove product from the SSG development tree")
    parser.add_option_group(remove_group)

    (options, args) = parser.parse_args()

    if options.create and options.remove:
        print("Cannot create a new product and delete at the same time!\n")
        sys.exit(parser.print_help())

    if options.create:
        create_product(options)
    if options.remove:
        remove_product(options)

    if len(sys.argv) < 2:
        create_product(options)

    return (options, args)


def main():
    (options, args) = parse_options()


if __name__ == "__main__":
    main()

