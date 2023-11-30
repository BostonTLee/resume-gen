import datetime
import yaml
#import toml
import pprint
import os
import subprocess
import argparse

from pylatex import Document, Section, Subsection
from pylatex import utils


from schema import Resume
from latex_visitor import LatexVisitor


def fill_document(doc: Document):
    """Add a section, a subsection and some text to the document.

    :param doc: the document
    :type doc: :class:`pylatex.document.Document` instance
    """
    with doc.create(Section('A section')):
        doc.append('Some regular text and some ')
        doc.append(utils.italic('italic text. '))

        with doc.create(Subsection('A subsection')):
            doc.append('Also some crazy characters: $&#{}')


if __name__ == "__main__":
    CV_DATA_FILEPATH = "cv.yaml"
    LATEX_DOCUMENT_DIR = "./documents"


    with open('cv.yaml', 'r') as file:
        resume_raw = yaml.safe_load(file)
        print(resume_raw)
        resume = Resume.model_validate(resume_raw)
        latex_visitor = LatexVisitor("basic_pdf_example")
        latex_visitor.visitResume(resume)