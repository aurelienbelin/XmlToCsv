import getopt
import xml.etree.ElementTree as ET
import pandas as pd
import sys
import os.path


def usage():
    print("Usage: \r\n\t" + sys.argv[0] + " -s <sourceFile.xml> -t <targetFile.csv>")
    print()
    print("General options:")
    print("\t-h, --help\t\tShow help.")
    print("\t-s, --source=\t\tTo provide a source file XML to convert.")
    print("\t-t, --target=\t\tTo provide a target file name to store the conversion result in CSV.")
    print()


def show_help():
    print("Help")
    print("\tWith this tool, you can convert an XML file to a CSV one")
    print()
    usage()
    print()


def check_format(source, target):
    if not source.endswith(".xml"):
        print("Provided source file is not an XML file ; please provide an XML file as source to use this tool")
        sys.exit()

    if not target.endswith(".csv"):
        print("Provided target file is not a CSV file ; please provide an CSV file (or filename) as target to use "
              "this tool")
        sys.exit()


def check_source_existence(source):
    if not os.path.isfile(source):
        print("Error: provided source file " + source + " is not a file or does not exists")
        sys.exit()


def get_range(col):
    return range(len(col))


def main(argv):
    found_target = False
    found_source = False

    source = ""
    target = ""

    print()
    print("Welcome to this XML to CSV converter !")
    print()

    try:
        opts, args = getopt.getopt(argv, "hs:t:", ["help", "source=", "target="])
        if not opts:
            usage()
            sys.exit()
    except getopt.GetoptError:
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            show_help()
            sys.exit()
        elif opt in ("-s", "--source"):
            source = arg
            found_source = True
        elif opt in ("-t", "--target"):
            target = arg
            found_target = True

    if not found_source:
        print("No source file given ; please provide a source file with the option -s")
        sys.exit()

    if not found_target:
        print("No target file given ; please provide a target file with the option -t")
        sys.exit()

    check_format(source, target)

    check_source_existence(source)

    tree = ET.parse(source)
    root = tree.getroot()

    raw_data = [{r[i].tag: r[i].text for i in get_range(r)} for r in root]

    df = pd.DataFrame.from_dict(raw_data)
    df.to_csv(target)

    print("Result: source file " + source + " converted to CSV format and stored in " + target)
    print()


if __name__ == "__main__":
    main(sys.argv[1:])
