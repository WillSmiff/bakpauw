### Generation helper for index.html

from .. import file as util_file
from .. import csv as util_csv
import shutil


def generate(templatedir, destinationdir, templateFilename):
    """Main generation function for index.html generation helper.

    templatedir -- the relative path of the template html file's directory\n
    destinationpath -- the directory where index.html should be generated\n
    templateFilename -- the filename of the index template (always index.html)\n
    """

    # Copy template to appropriate directory
    shutil.copy(f"{templatedir}/{templateFilename}", destinationdir)

    # Read categories and config csv files
    idName = "tk_category_dashname"
    categories = util_csv.dictReaderMultiRow("../csv/categories.csv", idName)
    runs = util_csv.dictReaderMultiRow("../csv/runs.csv", "tk_run_id")
    config = util_csv.dictReaderFirstRow("../csv/config.csv")

    # Replace config tk placeholders with values
    for key in config.keys():
        util_file.replaceTextInFile(f"{destinationdir}/index.html", key, config[key])

    # lk_categories handler
    tk_category_dashname = "tk_category_dashname"
    tk_category_name = "tk_category_name"
    for category in categories:
        util_file.replaceTextInFile(
            f"{destinationdir}/index.html",
            "lk_categories",
            f'<a class="categoryLink" href="categories/{categories[category][tk_category_dashname]}">{categories[category][tk_category_name]}</a>lk_categories',
        )
    util_file.replaceTextInFile(f"{destinationdir}/index.html", "lk_categories", "")

    # lk_bapaos_eaten handler
    bapaos_eaten = sum(
        4 if run["tk_run_category_dashname"] == "BoC" else 2
        for run in runs.values()
    )
    util_file.replaceTextInFile(
        f"{destinationdir}/index.html",
        "lk_bapaos_eaten",
        f"Aantal bapao's gegeten: <strong>{bapaos_eaten}</strong>",
    )

    # lk_poultry_eaten handler
    poultry = sum(
        100.8 if run["tk_run_category_dashname"] == "BoC" else 50.4
        for run in runs.values()
    ) / 1000
    poultry_eaten = "{:.3f}".format(poultry)
    util_file.replaceTextInFile(
        f"{destinationdir}/index.html",
        "lk_poultry_eaten",
        f"Hoeveelheid slachtafval gegeten: <strong>{poultry_eaten} kg</strong>",
    ) 