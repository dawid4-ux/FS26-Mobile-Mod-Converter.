
import zipfile
import xml.etree.ElementTree as ET
import os
import json
import sys

MAX_SIZE = 500 * 1024 * 1024

def inspect_mod(path):
    report = {
        "file": os.path.basename(path),
        "status": "ANALYZED",
        "errors": [],
        "files_checked": 0,
        "xml_checked": 0,
        "i3d_checked": 0
    }

    if not os.path.isfile(path):
        report["errors"].append("File not found")
        return report

    if os.path.getsize(path) > MAX_SIZE:
        report["errors"].append("ZIP exceeds 500 MB")
        return report

    try:
        with zipfile.ZipFile(path, "r") as archive:
            for item in archive.infolist():
                if item.is_dir():
                    continue

                name = item.filename
                report["files_checked"] += 1

                if name.endswith((".xml", ".i3d")):
                    try:
                        data = archive.read(item)
                        ET.fromstring(data)

                        if name.endswith(".xml"):
                            report["xml_checked"] += 1
                        else:
                            report["i3d_checked"] += 1

                    except Exception as error:
                        report["errors"].append(
                            name + ": " + str(error)
                        )

            if report["errors"]:
                report["status"] = "ERRORS_FOUND"

    except zipfile.BadZipFile:
        report["status"] = "INVALID_ZIP"
        report["errors"].append("Invalid ZIP archive")

    return report


def main():
    if len(sys.argv) < 2:
        print("Usage: python converter.py mod.zip")
        return

    result = inspect_mod(sys.argv[1])

    print(json.dumps(result, indent=2))

    with open("conversion_report.json", "w") as file:
        json.dump(result, file, indent=2)


if __name__ == "__main__":
    main()
